CSV_INFLATION_MONTHLY = """\
CasRef_ID;Staprofi_ID;Ukazatel;Období;Hodnota
1;WCEN01MT01;Stejné období předchozího roku = 100;2024-01;103.2
1;WCEN01MT01;Stejné období předchozího roku = 100;2024-02;103.0
1;WCEN01MT01;Stejné období předchozího roku = 100;2024-03;102.9
1;WCEN01MT01;Stejné období předchozího roku = 100;2024-04;102.8
1;WCEN01MT01;Stejné období předchozího roku = 100;2024-05;101.9
1;WCEN01MT01;Měsíční index = 100;2024-01;101.2
1;WCEN01MT01;Měsíční index = 100;2024-02;100.8
"""

CSV_WAGES_QUARTERLY = """\
CasRef_ID;Staprofi_ID;Ukazatel;Období;Hodnota
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2023-Q1;41000
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2023-Q2;41500
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2023-Q3;42000
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2023-Q4;42800
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2024-Q1;43500
2;MZDQ1T1;Průměrná hrubá měsíční mzda na přepočtené počty zaměstnanců (Kč);2024-Q2;44000
"""

CSV_ANNUAL_INFLATION = """\
CasRef_ID;Staprofi_ID;Ukazatel;Období;Hodnota
3;CEN0101HT01;Průměrná roční míra inflace;2023;10.7
3;CEN0101HT01;Průměrná roční míra inflace;2024;2.4
"""

NKOD_PENSION_DATASETS = {
    "results": {
        "bindings": [
            {
                "title": {"type": "literal", "value": "Průměrný starobní důchod"},
                "description": {"type": "literal", "value": "Data o průměrných důchodech v ČR"},
            },
            {
                "title": {"type": "literal", "value": "Příjemci důchodů"},
                "description": {"type": "literal", "value": "Počty příjemců důchodů podle typu"},
            },
        ]
    }
}

KATALOG_SADY = [
    {"id": "WCEN01MT01", "name": "Indexy spotřebitelských cen"},
    {"id": "MZDQ1T1", "name": "Průměrné mzdy"},
]

KATALOG_SADA_INFO = {"id": "WCEN01MT01", "name": "Indexy spotřebitelských cen", "popis": "CPI meziroční a meziměsíční"}
