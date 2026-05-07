# KALKULAČKA PENZÍ PRO - GitHub Setup Guide

> Jak vytvořit privátní GitHub repo a pushovat lokální projekt

---

## 📋 Krok 1: Vytvořit GitHub Repository

### 1.1 Na GitHub.com

1. Přejdi na https://github.com/new
2. Vyplň:
   - **Repository name:** `KALKULAČKA-PENZÍ-PRO` (nebo s pomlčkami/bez diakritiky)
   - **Description:** "Expertní ekosystém pro důchodovou analýzu a optimalizaci"
   - **Visibility:** Private ✅
   - **Initialize with:** None (my máme lokální .git)

3. Klikni "Create repository"

### 1.2 Kopíruj HTTPS URL

Po vytvoření repo vidíš na `<>`Code tlačítko - kopíruj URL:
```
https://github.com/matejkocanda/KALKULAČKA-PENZÍ-PRO.git
```

---

## 🔗 Krok 2: Připojit Lokální Repository k GitHub

### V Terminálu:

```bash
cd "/Users/matejkocanda/Library/Mobile Documents/com~apple~CloudDocs/PensionCalculator"

# Přidej GitHub jako remote
git remote add origin https://github.com/matejkocanda/KALKULAČKA-PENZÍ-PRO.git

# Ověř
git remote -v
```

Output by měl být:
```
origin  https://github.com/matejkocanda/KALKULAČKA-PENZÍ-PRO.git (fetch)
origin  https://github.com/matejkocanda/KALKULAČKA-PENZÍ-PRO.git (push)
```

---

## 📤 Krok 3: Pushovat kód na GitHub

```bash
# Pushni main branch (máš tam 3 commity)
git push -u origin main

# Output:
# Enumerating objects: 45, done.
# Counting objects: 100% (45/45), done.
# ...
# To github.com:matejkocanda/KALKULAČKA-PENZÍ-PRO.git
#  * [new branch]      main -> main
# Branch 'main' set up to track remote branch 'main' from 'origin'.
```

### Pokud dostaneš error "403 Forbidden":

Potřebuješ **GitHub Personal Access Token** (PAT):

1. Přejdi https://github.com/settings/tokens
2. "Generate new token (classic)"
3. Scope: `repo` + `workflow`
4. Vygeneruj & zkopíruj token
5. V terminálu:
   ```bash
   git remote set-url origin https://<GITHUB_TOKEN>@github.com/matejkocanda/KALKULAČKA-PENZÍ-PRO.git
   git push -u origin main
   ```

---

## ✅ Krok 4: Ověřit na GitHub

1. Přejdi na https://github.com/matejkocanda/KALKULAČKA-PENZÍ-PRO
2. Měl bys vidět:
   - ✅ 3 commits v `main`
   - ✅ Všechny soubory (src/, api/, config/, tests/, etc.)
   - ✅ README.md se zobrazuje
   - ✅ GitHub Actions workflow soubory v `.github/workflows/`

---

## 🔐 Krok 5: GitHub Secrets Setup (PRO CI/CD)

### 5.1 Otevřít Settings

1. Na repo: https://github.com/matejkocanda/KALKULAČKA-PENZÍ-PRO/settings/secrets/actions
2. Klikni "New repository secret"

### 5.2 Přidej Secrets (Až bude tokeny)

Jakmile vygeneruješ Cloudflare + Railway tokeny, vložíš je tady:

```
CLOUDFLARE_API_TOKEN = <tvůj-cloudflare-token>
CLOUDFLARE_ACCOUNT_ID = <tvůj-account-id>
CLOUDFLARE_EMAIL = tvoj@email.com
RAILWAY_TOKEN = <tvůj-railway-token>
```

Tyto se pak automaticky vloží do GitHub Actions workflowů.

---

## 🔄 Krok 6: GitHub Actions Setup

### 6.1 Ověřit že workflows jsou aktivní

1. Přejdi do https://github.com/matejkocanda/KALKULAČKA-PENZÍ-PRO/actions
2. Měl bys vidět:
   - `test-build.yml` - běží při push na main/develop
   - `deploy-pages.yml` - deploy na CF Pages
   - `deploy-railway.yml` - deploy API na Railway

### 6.2 Manuální Trigger (pro test)

```bash
git push  # Pushe commit
# Přejdi na Actions tab - měl by se spustit test-build workflow
```

---

## 📝 Krok 7: Lokální Git Workflow (DO BUDOUCNA)

### Při práci na novém featureu:

```bash
# 1. Vytvoř feature branch
git checkout -b feature/vue3-frontend

# 2. Dělej změny
echo "..." > FRONTEND_MIGRATION_PLAN.md

# 3. Commit
git add FRONTEND_MIGRATION_PLAN.md
git commit -m "feat: Start Vue 3 frontend migration"

# 4. Push na GitHub
git push -u origin feature/vue3-frontend

# 5. Vytvořit Pull Request na GitHub
# - GitHub ti nabídne "Compare & pull request" button
# - Doplň popis
# - Čekej na CI/CD (testy musí projít)
# - Merge do main

# 6. Po merge, local cleanup
git checkout main
git pull origin main
git branch -d feature/vue3-frontend
```

---

## 🎯 Commit Message Convention

Sledujeme **Conventional Commits**:

```bash
# Feature
git commit -m "feat: description"

# Bug fix
git commit -m "fix: description"

# Documentation
git commit -m "docs: description"

# Chore (deps, config)
git commit -m "chore: description"

# Testing
git commit -m "test: description"

# Styling (no code changes)
git commit -m "style: description"

# Refactoring
git commit -m "refactor: description"
```

**Příklady:**
```bash
git commit -m "feat: Add Vue 3 PensionCalculator component"
git commit -m "fix: Fix API timeout issue in calculator.ts"
git commit -m "docs: Update README with installation steps"
git commit -m "chore: Add Dockerfile and docker-compose"
```

---

## 📊 GitHub Projects & Issues

### 7.1 Projects Setup (Kanban Board)

1. Přejdi https://github.com/matejkocanda/KALKULAČKA-PENZÍ-PRO/projects
2. Klikni "New project"
3. Vyberi "Table" view
4. Vytvoř columns: `Backlog | In Progress | In Review | Done`

### 7.2 Issues Template

Vytvoř `.github/ISSUE_TEMPLATE/bug_report.md`:
```markdown
## Popis Chyby
[Detailní popis]

## Kroki k reprodukci
1. ...
2. ...

## Očekávané chování
[Co by mělo být]

## Aktuální chování
[Co je špatně]

## Prostředí
- OS: macOS
- Python: 3.11
- Browser: Safari
```

---

## 🔐 Bezpečnost Repo

### 8.1 Branch Protection (Main)

1. Settings → Branches → "Add rule"
2. Vyplň: `main`
3. Zapni:
   - ✅ "Require a pull request before merging"
   - ✅ "Dismiss stale pull request approvals when new commits are pushed"
   - ✅ "Require status checks to pass before merging"
     - Vyber `test-build` workflow

### 8.2 Codeowners (Optional)

Vytvoř `.github/CODEOWNERS`:
```
# Python backend
src/backend/ @matejkocanda
api/ @matejkocanda

# Frontend
frontend/ @matejkocanda

# Konfiguraci
config/ @matejkocanda
```

---

## 📖 Návazné Kroky

### Next: Cloudflare Pages Setup

1. Přejdi https://dash.cloudflare.com/
2. "Workers & Pages" → "Create" → "Connect to Git"
3. Vyber repo: `KALKULAČKA-PENZÍ-PRO`
4. Configure:
   - Framework: Vue
   - Build command: `npm run build`
   - Build output directory: `dist`
5. Deploy

### Next: Railway.com Setup

1. https://railway.app/ → Create New Project
2. GitHub integration → vyberi repo
3. Railway auto-detects `Dockerfile`
4. Deploy!

---

## ✅ Checklist

- [ ] GitHub repo vytvořen (private)
- [ ] Lokální git remote nastaven
- [ ] Kód pushnutý na main
- [ ] Workflow soubory viditelné v Actions
- [ ] GitHub Secrets připraveni (po tokenech)
- [ ] Branch protection na main (optional)
- [ ] README viditelný na GitHub

---

## 🚀 Teď jsi připraven na:

1. **Frontend Development** → `git checkout -b feature/vue3-frontend`
2. **Database Setup** → `git checkout -b feature/d1-integration`
3. **Authentication** → `git checkout -b feature/oauth`
4. **Deployment** → GitHub Actions automaticky deployuje

---

**Status:** Lokální project synchronizovaný s GitHub  
**Next:** Čekám na tvé confirmaci + tokeny pro Cloudflare + Railway
