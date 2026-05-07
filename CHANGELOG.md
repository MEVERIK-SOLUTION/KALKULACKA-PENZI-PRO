# Changelog

Všechny důležité změny projektu KALKULAČKA PENZÍ PRO jsou zdokumentovány v tomto souboru.

Formát je založen na [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
a projekt používá [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- Vue 3 frontend migration
- Database (D1) integration
- OAuth authentication (Google, Microsoft, iCloud, Seznam)
- E2E testing (Playwright)
- Docker containerization
- NVIDIA NIM integration (optional)
- Public API documentation

---

## [0.1.0-alpha] - 2026-05-07

### Added
- Initial project setup
- **Engine Core:**
  - OVZ Calculator (§15 ZDP) - `ovz_calculator.py`
  - Reduction Engine - `reduction_engine.py`
  - Paradox Resolver (náhradní doby) - `paradox_resolver.py`
  - Pension Calculator (starobní + předčasný důchod) - `pension_calculator.py`
- **API Layer:**
  - FastAPI backend with 4 endpoints
  - CORS enabled for local development
  - Swagger/OpenAPI documentation
- **Frontend:**
  - MVP SPA with HTML/CSS/JS
  - 3 tabs: Pension | OVZ | Paradox
  - Basic form handling
- **Tests:**
  - 13 unit tests (all passing)
  - pytest + pylint configured
  - Pylint score: 8.78/10
- **Configuration:**
  - legislative_2026.yaml - parametry zákona
  - requirements.txt - Python dependencies
  - scripts/run.sh - development launcher
- **DevOps:**
  - .gitignore for Python/Node/IDE
  - .env.example for configuration template
  - .gitattributes for line endings
  - GitHub Actions workflows (test, deploy)
- **Documentation:**
  - README.md with setup instructions
  - Architecture overview
  - API endpoint documentation

### Project Structure
```
PensionCalculator/
├── api/main.py
├── config/legislative_2026.yaml
├── src/backend/engine/
│   ├── ovz_calculator.py
│   ├── reduction_engine.py
│   ├── paradox_resolver.py
│   └── pension_calculator.py
├── frontend/index.html
├── tests/unit/
│   ├── test_ovz_calculator.py
│   ├── test_reduction_engine.py
│   ├── test_paradox_resolver.py
│   └── test_pension_calculator.py
├── scripts/run.sh
├── requirements.txt
├── README.md
├── CHANGELOG.md
├── .gitignore
├── .env.example
├── .gitattributes
└── .github/workflows/
    ├── test-build.yml
    ├── deploy-pages.yml
    └── deploy-railway.yml
```

### Status
- ✅ Engine complete with validation
- ✅ API functional (MVP)
- ✅ Unit tests passing (13/13)
- 📋 Frontend MVP ready for Vue 3 migration
- 📋 Ready for GitHub repo initialization

### Notes
- Current coverage: All core calculations validated against MPSV standards
- Next phase: Database integration + multi-user support
- CI/CD workflows prepared, waiting for GitHub Actions activation

---

## [Future Versions]

### v0.2.0 - Database & Authentication
- D1 database integration
- OAuth providers (Google, Microsoft, iCloud, Seznam)
- User session management
- Calculation history storage

### v0.3.0 - Frontend Complete
- Vue 3 / React migration
- Complete UI/UX design
- Mobile responsiveness
- Form validation & error handling

### v1.0.0 - Production Ready
- Full E2E testing
- Docker deployment
- Railway.com hosting
- Cloudflare Pages + Workers
- Public API release

---

## Template for Next Entry

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New features

### Changed
- Changed features

### Fixed
- Bug fixes

### Removed
- Removed features

### Security
- Security updates
```

---

**Last Updated:** 7. května 2026
**Maintained By:** Matej Kocanda
