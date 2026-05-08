from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Float, Integer, String, Text

from .config import Base


class CalculationHistory(Base):
    __tablename__ = "calculation_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    calc_type = Column(String(50), nullable=False, index=True)
    input_data = Column(JSON, nullable=False)
    result = Column(JSON, nullable=False)
    ovz = Column(Float, nullable=True)
    vz = Column(Float, nullable=True)
    pension_amount = Column(Float, nullable=True)
    insurance_years = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    client_ip = Column(String(45), nullable=True)
    note = Column(Text, nullable=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "calc_type": self.calc_type,
            "input_data": self.input_data,
            "result": self.result,
            "ovz": self.ovz,
            "vz": self.vz,
            "pension_amount": self.pension_amount,
            "insurance_years": self.insurance_years,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "client_ip": self.client_ip,
            "note": self.note,
        }
