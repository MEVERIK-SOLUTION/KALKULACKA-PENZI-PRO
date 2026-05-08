from io import StringIO

import pandas as pd
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    from api.main import app
    return TestClient(app)


CSV_INFLATION = """\
CasRef_ID;Staprofi_ID;Ukazatel;Období;Hodnota
1;WCEN01MT01;Stejné období předchozího roku = 100;2024-01;103.2
1;WCEN01MT01;Stejné období předchozího roku = 100;2024-02;103.0
1;WCEN01MT01;Stejné období předchozího roku = 100;2024-03;102.9
1;WCEN01MT01;Stejné období předchozího roku = 100;2024-04;102.8
1;WCEN01MT01;Stejné období předchozího roku = 100;2024-05;101.9
"""

CSV_WAGES = """\
CasRef_ID;Staprofi_ID;Ukazatel;Období;Hodnota
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2014-Q1;24000
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2014-Q2;24200
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2014-Q3;24500
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2014-Q4;24800
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2015-Q1;25000
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2015-Q2;25300
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2015-Q3;25600
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2015-Q4;26000
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2016-Q1;26500
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2016-Q2;27000
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2016-Q3;27500
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2016-Q4;28000
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2017-Q1;28500
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2017-Q2;29000
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2017-Q3;29500
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2017-Q4;30000
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2018-Q1;30500
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2018-Q2;31000
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2018-Q3;31500
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2018-Q4;32000
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2019-Q1;33000
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2019-Q2;33500
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2019-Q3;34000
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2019-Q4;34500
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2020-Q1;35000
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2020-Q2;33500
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2020-Q3;34000
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2020-Q4;34800
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2021-Q1;37000
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2021-Q2;37500
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2021-Q3;37800
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2021-Q4;38500
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2022-Q1;39500
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2022-Q2;40000
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2022-Q3;40500
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2022-Q4;40800
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2023-Q1;41000
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2023-Q2;41500
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2023-Q3;41800
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2023-Q4;42500
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2024-Q1;43500
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2024-Q2;44000
"""


@pytest.fixture(autouse=True)
def mock_csu_data(monkeypatch):
    """Mock DataStat _get_csv so tests don't hit real API."""

    def mock_inflation(_self):
        return pd.read_csv(StringIO(CSV_INFLATION), sep=";")

    def mock_wages(_self):
        return pd.read_csv(StringIO(CSV_WAGES), sep=";")

    import cz_pension_api.datastat as ds
    monkeypatch.setattr(ds.DataStatClient, "get_inflation_monthly", mock_inflation)
    monkeypatch.setattr(ds.DataStatClient, "get_inflation_rate_annual", mock_inflation)
    monkeypatch.setattr(ds.DataStatClient, "get_inflation_rate_monthly", mock_inflation)
    monkeypatch.setattr(ds.DataStatClient, "get_wages_quarterly", mock_wages)


class TestDataInflation:
    def test_inflation_returns_rate(self, client):
        resp = client.get("/data/inflation")
        assert resp.status_code == 200
        data = resp.json()
        assert "rate" in data
        assert "unit" in data
        assert data["unit"] == "%"
        assert data["rate"] > 0

    def test_inflation_source(self, client):
        resp = client.get("/data/inflation")
        data = resp.json()
        assert data["source"] == "ČSÚ DataStat"


class TestDataAvgWage:
    def test_avg_wage_returns_amount(self, client):
        resp = client.get("/data/avg-wage")
        assert resp.status_code == 200
        data = resp.json()
        assert "amount" in data
        assert data["amount"] > 0
        assert data["unit"] == "Kč/měsíc"


class TestDataWageGrowth:
    def test_wage_growth_default(self, client):
        resp = client.get("/data/wage-growth")
        assert resp.status_code == 200
        data = resp.json()
        assert "rate" in data
        assert data["period_years"] == 10

    def test_wage_growth_custom_period(self, client):
        resp = client.get("/data/wage-growth?years_back=2")
        assert resp.status_code == 200
        data = resp.json()
        assert data["period_years"] == 2

    def test_wage_growth_invalid_param(self, client):
        resp = client.get("/data/wage-growth?years_back=-1")
        assert resp.status_code == 200
