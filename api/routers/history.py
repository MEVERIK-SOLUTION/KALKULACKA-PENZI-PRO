
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


@router.delete("/{record_id}", status_code=204)
async def delete_record(record_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(CalculationHistory).where(CalculationHistory.id == record_id))
    record = result.scalar_one_or_none()
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    await session.delete(record)
    await session.commit()
