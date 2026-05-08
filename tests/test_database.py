from datetime import datetime

from src.backend.database.models import CalculationHistory


class TestCalculationHistoryModel:
    def test_to_dict_returns_all_fields(self):
        record = CalculationHistory(
            id=1,
            calc_type="pension",
            input_data={"annual_income": 500000},
            result={"pension_amount": 20000},
            ovz=38000.0,
            vz=25000.0,
            pension_amount=20000.0,
            insurance_years=45.0,
            created_at=datetime(2026, 1, 1, 12, 0, 0),
            client_ip="127.0.0.1",
            note="test record",
        )
        d = record.to_dict()
        assert d["id"] == 1
        assert d["calc_type"] == "pension"
        assert d["ovz"] == 38000.0
        assert d["pension_amount"] == 20000.0
        assert d["insurance_years"] == 45.0
        assert d["client_ip"] == "127.0.0.1"
        assert d["note"] == "test record"
        assert d["created_at"] == "2026-01-01T12:00:00"

    def test_to_dict_handles_null(self):
        record = CalculationHistory(
            id=2,
            calc_type="test",
            input_data={},
            result={},
        )
        d = record.to_dict()
        assert d["ovz"] is None
        assert d["vz"] is None
        assert d["note"] is None
        assert d["client_ip"] is None

    def test_default_created_at(self):
        record = CalculationHistory(
            calc_type="test",
            input_data={"x": 1},
            result={"y": 2},
        )
        assert record.created_at is None  # SQLAlchemy default at DB level

    def test_table_name(self):
        assert CalculationHistory.__tablename__ == "calculation_history"
