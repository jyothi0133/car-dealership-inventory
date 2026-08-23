# AI Prompting Log & Development Iterations

This log details how AI tools (Gemini) were leveraged as an engineering collaborator to build, test, and refine the Car Dealership Inventory System, following TDD and clean code practices.

---

## Iteration History & Engineering Process

### 1. Project Architecture & Setup
* **Intent:** Establish a modular FastAPI backend paired with a React (Vite) frontend.
* **Prompt Used:** *"Help me set up a full-stack car dealership app with a FastAPI backend, SQLite database, and React Vite frontend."*
* **Outcome & Verification:** Created separated `/backend` and `/frontend` directories, configured CORS middleware in FastAPI, and verified local dev servers.

### 2. TDD & Database Seeding
* **Intent:** Follow Test-Driven Development (TDD) by writing backend tests for vehicle inventory endpoints and seeding initial records.
* **Prompt Used:** *"How do I automatically seed 10 vehicle models into SQLite on FastAPI startup, and how do I write Pytest cases to verify endpoint responses?"*
* **Outcome & Verification:** Implemented `@app.on_event("startup")` in FastAPI to seed 10 default records. Wrote tests in `tests/test_vehicles.py` and confirmed all passed using `pytest`.

### 3. Full CRUD & Interactive Logic
* **Intent:** Wire up live search, stock reduction (`/buy`), stock increase (`/restock`), vehicle addition, and deletion.
* **Prompt Used:** *"The buy button and admin actions are not reflecting changes. Help me implement API routes for buying, restocking, deleting, and adding vehicles, and connect them to React state handlers."*
* **Outcome & Verification:** Built `/buy`, `/restock`, `POST`, and `DELETE` endpoints. Monitored Uvicorn logs to confirm `200 OK` status codes for state mutations.

### 4. UI/UX Polishing & Contrast Fixes
* **Intent:** Address readability and layout issues on the frontend.
* **Prompt Used:** *"Fix header layout spacing and increase car title text contrast against dark card backgrounds."*
* **Outcome & Verification:** Refined CSS inline styling and layout spacing. Verified fixed contrast and responsiveness across card components.

---

## Key Learnings & Engineering Judgment
* **AI Collaboration:** Used AI for boilerplate generation, state handler patterns, and test structure while personally reviewing logic and terminal outputs.
* **Bug Fixes & Debugging:** Resolved line-ending normalization warnings (`CRLF/LF`), handled SQLite connection sessions safely, and verified CORS origin handling.
* **Code Understanding:** Full clarity on FastAPI routing, SQLAlchemy sessions, Pytest execution, and React state synchronization