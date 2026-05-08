
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.database import CalculationHistory, get_session

router = APIRouter(prefix="/history", tags=["history"])


class HistoryEntry(BaseModel):
    calc_type: str
    input_data: dict
    result: dict
    ovz: float | None = None
    vz: float | None = None
    pension_amount: float | None = None
    insurance_years: float | None = None
    note: str | None = None


class HistoryResponse(BaseModel):
    id: int
    calc_type: str
    input_data: dict
    result: dict
    ovz: float | None = None
    vz: float | None = None
    pension_amount: float | None = None
    insurance_years: float | None = None
    created_at: str
    client_ip: str | None = None
    note: str | None = None


@router.post("/", response_model=HistoryResponse, status_code=201)
async def save_calculation(entry: HistoryEntry, request: Request, session: AsyncSession = Depends(get_session)):
    record = CalculationHistory(
        calc_type=entry.calc_type,
        input_data=entry.input_data,
        result=entry.result,
        ovz=entry.ovz,
        vz=entry.vz,
        pension_amount=entry.pension_amount,
        insurance_years=entry.insurance_years,
        note=entry.note,
        client_ip=request.client.host if request.client else None,
    )
    session.add(record)
    await session.commit()
    await session.refresh(record)
    return record.to_dict()


@router.get("/", response_model=list[HistoryResponse])
async def list_history(
    calc_type: str | None = None,
    limit: int = 20,
    offset: int = 0,
    session: AsyncSession = Depends(get_session),
):
    query = select(CalculationHistory).order_by(desc(CalculationHistory.created_at))
    if calc_type:
        query = query.where(CalculationHistory.calc_type == calc_type)
    query = query.offset(offset).limit(limit)
    result = await session.execute(query)
    records = result.scalars().all()
    return [r.to_dict() for r in records]


@router.get("/{record_id}", response_model=HistoryResponse)
async def get_record(record_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(CalculationHistory).where(CalculationHistory.id == record_id))
    record = result.scalar_one_or_none()
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return record.to_dict()


@router.put("/{record_id}", response_model=HistoryResponse)
async def update_record(record_id: int, entry: HistoryEntry, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(CalculationHistory).where(CalculationHistory.id == record_id))
    record = result.scalar_one_or_none()
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    
    # Update fields
    for field in ["calc_type", "input_data", "result", "ovz", "vz", "pension_amount", "insurance_years", "note"]:
        if hasattr(entry, field):
            setattr(record, field, getattr(entry, field))
    
    await session.commit()
    await session.refresh(record)
    return record.to_dict()


@router.get("/export/csv")
async def export_csv(calc_type: str | None = None, session: AsyncSession = Depends(get_session)):
    import csv
    import io
    from fastapi.responses import StreamingResponse
    
    query = select(CalculationHistory).order_by(desc(CalculationHistory.created_at))
    if calc_type:
        query = query.where(CalculationHistory.calc_type == calc_type)
    
    result = await session.execute(query)
    records = result.scalars().all()
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        "ID", "Typ výpočtu", "Vstupní data", "Výsledek", "OVZ", "VZ", 
        "Částka důchodu", "Pojištění (roky)", "Vytvořeno", "IP adresa", "Poznámka"
    ])
    
    # Write data
    for record in records:
        writer.writerow([
            record.id,
            record.calc_type,
            str(record.input_data),
            str(record.result),
            record.ovz or "",
            record.vz or "",
            record.pension_amount or "",
            record.insurance_years or "",
            record.created_at.isoformat() if record.created_at else "",
            record.client_ip or "",
            record.note or "",
        ])
    
    output.seek(0)
    
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8')),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=historie_vypoctu.csv"}
    )


@router.get("/export/pdf")
async def export_pdf(calc_type: str | None = None, session: AsyncSession = Depends(get_session)):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from fastapi.responses import StreamingResponse
    import io
    
    query = select(CalculationHistory).order_by(desc(CalculationHistory.created_at))
    if calc_type:
        query = query.where(CalculationHistory.calc_type == calc_type)
    
    result = await session.execute(query)
    records = result.scalars().all()
    
    # Create PDF in memory
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []
    
    # Title
    elements.append(Paragraph("Historie výpočtů důchodů", styles['Heading1']))
    elements.append(Spacer(1, 12))
    
    # Table data
    data = [["ID", "Typ", "OVZ", "VZ", "Důchod", "Roky", "Vytvořeno"]]
    
    for record in records[:50]:  # Limit to 50 records for PDF
        data.append([
            str(record.id),
            record.calc_type,
            f"{record.ovz:.2f}" if record.ovz else "",
            f"{record.vz:.2f}" if record.vz else "",
            f"{record.pension_amount:.2f}" if record.pension_amount else "",
            str(record.insurance_years) if record.insurance_years else "",
            record.created_at.strftime("%d.%m.%Y %H:%M") if record.created_at else "",
        ])
    
    # Create table
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=historie_vypoctu.pdf"}
    )


@router.delete("/{record_id}")
async def delete_record(record_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(CalculationHistory).where(CalculationHistory.id == record_id))
    record = result.scalar_one_or_none()
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    
    await session.delete(record)
    await session.commit()
    return {"message": "Record deleted successfully"}
