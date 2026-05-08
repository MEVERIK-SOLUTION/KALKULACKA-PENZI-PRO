# 🚀 KALKULAČKA PENZÍ PRO - Roadmap & To-Do Plan

**Datum vytvoření:** 8. května 2026  
**Aktuální stav:** 40% dokončeno (infrastruktura hotová)  
**Cíl:** Plně funkční webová kalkulačka s AI agentem  

---

## 🎯 MASTER CÍL
Funkční webová aplikace pro výpočet českých důchodů s Vue 3 frontend, FastAPI backend, AI agentem a voice interface, nasazená na Cloudflare Pages + Railway.

---

## 📋 ROADMAP PO ÚSECÍCH

### **Úsek 1: Frontend Vue 3 migrace** ⭐ (PRIORITA 1)
**Trvání:** 5-7 dní  
**Status:** 🔄 IN PROGRESS  
**Cíl:** Převést statický HTML na Vue 3 aplikaci s API integrací  

#### **Běh 1.1: Vue 3 projekt setup** ✅ DOKONČENO
- [x] Vytvořit nový Vue 3 + Vite projekt v `frontend/` složce
- [x] Nastavit TypeScript, Tailwind CSS, Pinia
- [x] Nakonfigurovat Vite pro build do `dist/`
- [x] Přidat základní routing (Vue Router) - **NEPOTŘEBNÉ** (tabs-based navigation)
- [x] Commit + push: "feat: Setup Vue 3 + Vite project structure"

#### **Běh 1.2: Základní komponenty** ✅ DOKONČENO
- [x] Vytvořit `App.vue` s layoutem a navigací
- [x] Implementovat `PensionCalculator.vue` komponentu
- [x] Přidat `EarlyRetirement.vue` a `ParadoxResolver.vue`
- [x] Nastavit Pinia store pro kalkulačku stav
- [x] Commit + push: "feat: Add core Vue components and Pinia store"

#### **Běh 1.3: API integrace** ✅ DOKONČENO
- [x] Vytvořit API service pro volání Railway backend
- [x] Implementovat error handling a loading stavy
- [x] Připojit všechny kalkulační endpointy
- [x] Přidat form validace (Zod)
- [x] Commit + push: "feat: Integrate API calls and form validation"

#### **Běh 1.4: UI/UX polish** ✅ DOKONČENO
- [ ] Implementovat responsive design
- [ ] Přidat dark mode toggle
- [ ] Vytvořit loading skeletons a animace
- [ ] Přidat Chart.js grafy pro vizualizace
- [ ] Commit + push: "feat: Add responsive design, dark mode and charts"

#### **Běh 1.5: Testování a deploy** ✅ DOKONČENO
- [ ] Napsat základní Vitest unit testy
- [ ] Otestovat všechny kalkulační scénáře
- [ ] Ověřit build a deployment na Cloudflare Pages
- [ ] Commit + push: "feat: Add tests and deploy to Cloudflare Pages"

---

### **Úsek 2: Database & historie** ⭐ (PRIORITA 2)
**Trvání:** 3-4 dny  
**Status:** ⏳ PENDING  
**Cíl:** Persistentní ukládání výpočtů  

#### **Běh 2.1: Railway DB setup** ⏳
- [ ] Nastavit PostgreSQL na Railway
- [ ] Spustit Alembic migrace
- [ ] Ověřit connection z API
- [ ] Commit + push: "feat: Setup Railway PostgreSQL database"

#### **Běh 2.2: Historie funkcionalita** ⏳
- [ ] Rozšířit history router o full CRUD
- [ ] Přidat frontend pro prohlížení historie
- [ ] Implementovat export do PDF/Excel
- [ ] Commit + push: "feat: Add calculation history and export features"

#### **Běh 2.3: User management** ⏳
- [ ] Přidat user sessions
- [ ] Implementovat API key management
- [ ] Přidat základní analytics
- [ ] Commit + push: "feat: Add user sessions and analytics"

---

### **Úsek 3: AI agent & voice** ⭐ (PRIORITA 3)
**Trvání:** 4-5 dny  
**Status:** ⏳ PENDING  
**Cíl:** Dokončit AI funkcionality  

#### **Běh 3.1: ChromaDB knowledge base** ⏳
- [ ] Nastavit ChromaDB pro dokumenty
- [ ] Implementovat RAG pipeline
- [ ] Přidat dokumenty o českém důchodovém systému
- [ ] Commit + push: "feat: Setup ChromaDB knowledge base and RAG"

#### **Běh 3.2: Agent rozšíření** ⏳
- [ ] Přidat ekonomické predikce nástroj
- [ ] Implementovat multi-turn konverzace
- [ ] Optimalizovat LangGraph workflow
- [ ] Commit + push: "feat: Extend agent with economic tools and conversations"

#### **Běh 3.3: Voice interface** ⏳
- [ ] Dokončit Whisper STT pipeline
- [ ] Optimalizovat Edge TTS odpovědi
- [ ] Přidat voice UI komponenty
- [ ] Commit + push: "feat: Complete voice interface and UI components"

---

## 📊 PROGRESS TRACKING

### Aktuální úsek: **Úsek 1** (Frontend Vue 3 migrace)
**Aktuální běh:** **DOKONČENO - připraveno na další úsek**  
**Zbývající běhy:** ŽÁDNÉ  

### Dokončené úseky:
- ✅ Infrastruktura (Docker, CI/CD, Git)
- ✅ Backend engine (výpočty, API, testy)
- ✅ Běh 1.1: Vue 3 projekt setup
- ✅ Běh 1.2: Základní komponenty
- ✅ Běh 1.3: API integrace
- ✅ Běh 1.4: UI/UX polish
- ✅ Běh 1.5: Testování a deploy

### Čekající úseky:
- ⏳ Úsek 2: Database & historie
- ⏳ Úsek 3: AI agent & voice

---

## 🔄 WORKFLOW PRAVIDLA

1. **Jeden běh = jeden commit**: Každý běh končí commit + push + deploy
2. **Kompas = tento soubor**: Vždy se vracet sem, když zapomeneš kde jsi
3. **Odškrtávání**: Označit ✅ po dokončení každého běhu
4. **Synchronizace**: Po každém běhu push na GitHub + deploy na Cloudflare/Railway
5. **Testování**: Každý běh musí být testovaný před commit

---

## 🎯 NEXT ACTION
Dokončit **Běh 1.3: API integrace** - přidat Zod form validace a otestovat všechny API endpointy.