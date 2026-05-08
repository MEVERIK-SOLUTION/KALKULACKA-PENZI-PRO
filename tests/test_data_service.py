from io import StringIO

import pandas as pd
import pytest

CSV_INFLATION = """\
CasRef_ID;Staprofi_ID;Ukazatel;Období;Hodnota
1;WCEN01MT01;Stejné období předchozího roku = 100;2024-01;103.2
1;WCEN01MT01;Stejné období předchozího roku = 100;2024-02;102.8
1;WCEN01MT01;Stejné období předchozího roku = 100;2024-03;101.9
"""

CSV_WAGES = """\
CasRef_ID;Staprofi_ID;Ukazatel;Období;Hodnota
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2015-Q1;30000
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2016-Q1;31500
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2017-Q1;33000
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2018-Q1;34500
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2019-Q1;36000
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2020-Q1;35000
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2021-Q1;37000
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2022-Q1;39500
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2023-Q1;41000
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2024-Q1;43500
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2024-Q2;44000
"""


@pytest.fixture(autouse=True)
def mock_csu(monkeypatch):
    def mock_inflation(_self):
        return pd.read_csv(StringIO(CSV_INFLATION), sep=";")

    def mock_wages(_self):
        return pd.read_csv(StringIO(CSV_WAGES), sep=";")

    import cz_pension_api.datastat as ds
    monkeypatch.setattr(ds.DataStatClient, "get_inflation_monthly", mock_inflation)
    monkeypatch.setattr(ds.DataStatClient, "get_wages_quarterly", mock_wages)


@pytest.fixture
def svc():
    from data_service import PensionDataService
    return PensionDataService(use_cache=False)


class TestPensionDataService:
    def test_get_latest_inflation_yoy(self, svc):
        rate = svc.get_latest_inflation_yoy()
        assert rate is not None
        assert rate > 0
        assert rate == pytest.approx(1.9, rel=1e-3)

    def test_get_latest_avg_wage(self, svc):
        wage = svc.get_latest_avg_wage()
        assert wage is not None
        assert wage > 0
        assert wage == 44000.0

    def test_get_wage_growth_rate(self, svc):
        rate = svc.get_wage_growth_rate(years_back=2)
        assert rate is not None
        assert rate > 0

    def test_get_wage_growth_short_period(self, svc):
        rate = svc.get_wage_growth_rate(years_back=100)
        assert rate is None

    def test_get_wage_no_data(self, monkeypatch, svc):
        empty_df = pd.read_csv(StringIO("CasRef_ID;Staprofi_ID;Ukazatel;Období;Hodnota\n"), sep=";")
        import cz_pension_api.datastat as ds
        monkeypatch.setattr(ds.DataStatClient, "get_inflation_monthly", lambda _self: empty_df)
        rate = svc.get_latest_inflation_yoy()
        assert rate is None
