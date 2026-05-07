### Projektový záměr: Expertní ekosystém pro důchodovou analýzu a optimalizaci (Next-Gen Pension Portal)

Tento dokument definuje strategický a technologický rámec pro vývoj komplexní platformy nové generace určené k hloubkové analýze a matematické optimalizaci starobních důchodů. Systém je navržen jako reakce na legislativní realitu roku 2026 a zaplňuje kritické vakuum na trhu finančního poradenství.

##### 1\. Strategické vymezení a vize projektu

V souvislosti s důchodovou reformou 2026 čelí veřejnost zásadnímu problému: státní nástroje jako ePortál ČSSZ nebo aplikace IDA plní pouze orientační, „stateless“ funkci. Jejich zásadním limitem je, že uživatelem doplněná data nejsou trvale ukládána ani validována pro budoucí použití. Náš ekosystém přináší zásadní změnu paradigmatu – přechod od jednorázového výpočtu k „stateful“ správě důchodového aktiva.Klíčovým přínosem systému je identifikace skrytých finančních rezerv, které standardní státní systémy ignorují (náhradní doby, vyloučené doby, optimalizace OSVČ). Zatímco průměrný občan přichází o cca 10 % výše důchodu kvůli neúplné evidenci, naše řešení funguje jako permanentní digitální trezor pro validované nároky. Pro finančního poradce představuje platformu pro budování odborné autority, pro klienta pak nástroj pro celoživotní dohled nad jeho budoucí rentou, překonávající statické PDF reporty směrem k dynamickému End-to-End řízení.

##### 2\. Architektonický koncept: Tříúrovňový ekosystém

Systém je postaven na robustní třívrstvé architektuře, která odděluje veřejnou edukaci, profesionální správu portfolia a klientský self-service.

1. **Veřejná zóna (Public Page):**  High-traffic rozhraní zaměřené na lead-gen a edukaci o zákonu č. 155/1995 Sb. Obsahuje "Shadow Calculator" pro rychlou indikaci chybějících let pojištění.  
2. **Virtuální kancelář poradce (Advisor Branch):**  Profesionální CRM a analytický modul. Umožňuje hromadnou správu klientských kmenů, asynchronní nahrávání IOLDP přes REST API a generování expertních auditů.  
3. **Klientský portál (Client Space):**  Persistentní prostor pro klienta. Na rozdíl od státní IDA, tento portál uchovává historická data, sleduje splnění podmínky 35 let pojištění a integruje predikci státního důchodu se soukromými produkty (DIP, penzijní připojištění).| Funkční modul | Veřejná zóna | Advisor Branch | Client Space || \------ | \------ | \------ | \------ || Legislativní zpravodajství | Základní | Expertní (včetně judikátů) | Personalizované || Datová persistence (Stateful) | Ne | Ano (Database Persistence) | Ano || Nahrávání a OCR IOLDP | Ne | Ano | Ano || Paralelní simulace scénářů | Ne | Ano (Plný přístup) | Vizualizace výsledků || Monitoring chybějících dob | Indikativní | Detailní (Analýza mezer) | Tracking postupu doložení |

##### 3\. Expertní výpočetní engine a "Decision Paradox"

Jádrem systému je vysoce pokročilý výpočetní engine (Python-based), který striktně separuje matematickou logiku od legislativních konstant (vyhlášek). Tato architektura zaručuje škálovatelnost při každoročních novelizacích.

* **Datová syntéza:**  Engine propojuje surová data z IOLDP se sadou 40+ dodatečných proměnných získaných ze strukturovaného dotazníku (vojna, studium, péče, odklady ZŠ).  
* **Algoritmizace rozhodovacího paradoxu:**  Jádro modelu neprovádí prosté sčítání. Implementujeme logiku  **diluce osobního vyměřovacího základu (OVZ)** . Algoritmus paralelně simuluje scénáře: se započtením náhradní doby vs. bez něj. Pokud doložení chybějící doby (např. studium před r. 1996\) zvýší dobu pojištění, ale kvůli nulovému příjmu naředí OVZ natolik, že výsledná částka klesne, engine doporučí tuto dobu úřadům nenárokovat.  
* **Optimalizační moduly:**  Specifické algoritmy pro OSVČ simulují vliv dobrovolných doplatků na pojistném v posledních letech před důchodem pro maximalizaci renty.**Kritické parametry algoritmu pro rok 2026:**  
1. **Accrual Rate (Procentní výměra):**  Snížení z 1,5 % o 0,005 % ročně (pro rok 2026 činí sazba 1,495 % za každý rok pojištění).  
2. **Redukční hranice:**  První hranice stanovena na 21 331 Kč (zápočet 99 %).  
3. **Základní výměra:**  Pevná složka 4 900 Kč (10 % průměrné mzdy).  
4. **Minimální důchod:**  Stanoven na 9 800 Kč (složen ze základní výměry 4 900 Kč a minimální procentní výměry 4 900 Kč).  
5. **VVZ (Všeobecný vyměřovací základ):**  Klíčový koeficient pro přepočet dřívějších příjmů na současnou hodnotu.

##### 4\. Metodika sběru dat a integrace se státní správou

Pro dosažení expertní úrovně analýzy využívá platforma Mobile-First dotazníky, které sbírají data neobsažená v evidenci ČSSZ.

* **Workflow integrace:**  Proces začíná uploadem IOLDP (PDF) z ePortálu. Engine automaticky mapuje mezeru mezi "prvním a posledním nárokovým dokladem" a aktivuje dotazníkovou logiku pro výplň těchto hluchých míst.  
* **Strukturovaný checklist (výběr z 40+ polí):**  
* **Vzdělání:**  Datum nástupu do 1\. třídy ZŠ (včetně  **odkladů školní docházky** ), přesné termíny SŠ/VŠ.  
* **PhD Rule:**  Evidence doktorského studia po r. 2009 (započtení až 4 let při úspěšném dokončení).  
* **Rodina:**  Rodná čísla dětí (výchovné 500 Kč/dítě, stanovení důchodového věku žen).  
* **Úřad práce:**  Diferenciace dob s podporou a bez podpory (vliv na 80% krácení doby).  
* **Evidence dokladů:**  Modul pro ukládání digitálních kopií (vysvědčení, vojenské knížky) pro pozdější proces doložení chybějících dob na OSSZ.

##### 5\. AI Asistence: Inteligentní vrstva pro poradce a klienty

AI v našem systému nefunguje jako autonomní generátor, ale jako expertní interpretační vrstva nad fixním matematickým enginem.

* **AI Validation Loop:**  Veškeré výstupy AI jsou cross-referencovány proti hard-coded výpočetnímu jádru. AI identifikuje anomálie (např. duplicity v IOLDP nebo chybějící vyloučené doby), ale finální výpočet provádí engine.  
* **Legislativní Watchdog:**  AI agent v reálném čase monitoruje  *Sbírku zákonů*  a identifikuje podzimní vyhlášky MPSV. Při změně parametrů (např. VVZ) automaticky spouští re-kalkulaci portfolia a notifikuje poradce o nutnosti aktualizace klientské strategie.  
* **Klientský interpret:**  Překlad právních termínů ( *vyloučená doba* ,  *redukční hranice* ) do srozumitelného jazyka na základě konkrétních dat klienta, čímž eliminuje bariéru "španělské vesnice".

##### 6\. Profesionální výstupy, reporting a správa portfolia

Výstupy jsou koncipovány jako auditní zprávy s vysokou vypovídací hodnotou, srovnávající stav "As-Is" (státní evidence) a "To-Be" (po expertní optimalizaci).**Layout klientského dashboardu (Wireframe):**

###### *MOJE PENZE 2026 | Klient: Jan Novák | Věk: 45 let*

**STÁTNÍ SLOŽKA (PREDIKCE)Datum nároku:**  15\. 03\. 1946 (za 20 let)  **Evidovaná doba:**  22 let / 35 let (podmínka splněna na 63 %)  **Odhadovaný důchod:**   **22 450 Kč**  (v dnešní hodnotě)**OPTIMALIZAČNÍ POTENCIÁL**\!  **Nalezena mezera:**  1998–2000 (pravděpodobně studium) \!  **Potenciální přínos:**  \+1 250 Kč / měsíčně \!  **Akce:**  Nahrát maturitní vysvědčení do trezoru.**SOUKROMÉ PORTFOLIO (DIP / PENZKO)Aktuální hodnota:**  450 000 Kč  **Projektovaná renta:**  8 500 Kč / měsíčně (po dobu 15 let)  
**CELKOVÁ PŘEDPOKLÁDANÁ RENTA: 30 950 Kč**

##### 7\. Technická správa, aktualizace a bezpečnost

Udržitelnost systému v dynamickém legislativním prostředí roku 2026 je zajištěna následujícími mechanismy:

* **Governance aktualizací:**  Roční cyklus aktualizace konstant (VVZ, koeficienty, redukční hranice) probíhá přes externí konfigurační vrstvu bez zásahu do zdrojového kódu.  
* **Aktuariální validace:**  Pravidelné testování výpočetního enginu proti kontrolním vzorkům MPSV a reálným výstupům z IDA pro zajištění 100% přesnosti.  
* **Bezpečnost dat (GDPR+):**  Šifrování citlivých údajů (rodná čísla dětí, vyměřovací základy) na úrovni databáze (AES-256). Systém je připraven na integraci s bankovními API (PSD2) pro automatizovaný monitoring soukromých investičních složek.  
* **Maintenance náklady:**  Monitoring novel zákona č. 155/1995 Sb. a provoz legislativního watchdogu.

