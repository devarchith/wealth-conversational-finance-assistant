# Development Log

This log records observed work; it does not backdate or simulate activity.

## Milestone 1 - Report reconstruction specification

- **Summary:** Read the complete 49-page report, extracted all text/tables/figures, inspected architecture, UI, functional-test, retrospective, ER, and appendix screenshots, and classified coherent finance requirements versus copied/unsafe material.
- **Main files:** `docs/PROJECT_SPEC.md`, `ARCHITECTURE.md`, `FEATURE_MATRIX.md`, `DATABASE_SCHEMA.md`, `API_SPEC.md`, `RECONSTRUCTION_ASSUMPTIONS.md`, `IMPLEMENTATION_PLAN.md`, `.gitignore`, `.env.example`.
- **Tests/checks:** Confirmed the source report remains outside the repository and is ignored by name/path; checked documentation coverage against the supplied reconstruction brief.
- **Known limitations:** GitHub repository exists privately, but shell Git authentication/transport is not yet configured; work is committed locally until a secure push route is established.
- **Commit:** pending

## Milestone 2 - Backend vertical slice

- **Summary:** Implemented FastAPI configuration, MongoDB and in-memory repository contracts, password hashing, JWT authentication, password resets, role checks, user and financial profiles, deterministic recommendations, rule-based NLP, mock/OpenAI-compatible AI providers, user-owned history, mock/SMTP email, mock/Cloudinary storage, admin summary, and provider fallbacks.
- **Main files:** `backend/app`, `backend/tests`, `backend/pyproject.toml`, `backend/Dockerfile`.
- **Tests/checks:** 18 backend tests passed; application coverage 83%; Python bytecode compilation passed; `pip check` reported no broken requirements.
- **Failures fixed:** Password-reset confirmation initially reused an intentionally invalid placeholder domain that the email validator correctly rejected. Replaced it with a valid non-user validation address and reran the full suite.
- **Known limitations:** Live MongoDB and external providers are not required by the test suite; MongoDB is the production repository and mock providers are the credential-free default.
- **Commit:** pending
