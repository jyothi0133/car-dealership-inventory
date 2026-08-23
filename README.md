# Car Dealership Inventory Management System

A production-ready, full-stack web application designed for car dealerships to monitor, manage, and process vehicle inventory in real time. The project features a robust **FastAPI** REST backend powered by **SQLite** and **SQLAlchemy**, coupled with a responsive **React (Vite)** frontend interface.

---

## Application Features

- **Automated Database Seeding:** Pre-populates the database with 10 default vehicle entries upon startup to guarantee immediate visual data upon initial application launch.
- **Real-Time Client-Side Search:** Instant multi-parameter filtering across make, model, category, and specifications.
- **Transactional Vehicle Purchase:** Integrated "Buy Now" logic that safely decrements inventory stock level (`-1`) in real time.
- **Admin Management Panel:** Interactive administrative dashboard enabling managers to:
  - Add new vehicles with comprehensive metadata (make, model, price, category, stock count).
  - Restock vehicle inventory (`+1` stock count per operation).
  - Delete obsolete vehicle records permanently from the database.
- **Cross-Origin Resource Sharing (CORS):** Explicitly configured CORS middleware allowing seamless API communication between frontend and backend environments.
- **Interactive API Documentation:** Automatically generated FastAPI Swagger UI docs available at `/docs`.

---

## Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend UI** | React.js, Vite, JavaScript (ES6+), Modern CSS3 |
| **Backend API** | Python 3.x, FastAPI, Uvicorn (ASGI Server), Pydantic |
| **ORM & Database** | SQLAlchemy, SQLite3 |
| **Version Control** | Git, GitHub |

## My AI Usage

### Tools Used
- **Gemini (Google AI):** Primary collaborator for architecture design, TDD setup, code generation, and debugging.

### How AI Was Leveraged
- **Backend Architecture & TDD:** Brainstormed FastAPI endpoint design, SQLite ORM models, and wrote test cases using `pytest`.
- **Frontend State Management:** Generated React component structures and `fetch` integration logic.
- **Debugging & Styling:** Used AI to resolve CORS issues, layout text overlap, and contrast adjustments.

### Reflection on AI Impact
Using AI significantly accelerated boilerplate setup and allowed a strong focus on Test-Driven Development (TDD) and clean code architecture. Human oversight was critical to verify test outcomes, fix configuration paths, and ensure proper git execution.
---

## Repository Architecture

```text
car-dealership-inventory/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── database.py       # SQLAlchemy engine & session setup
│   │   ├── main.py           # FastAPI routes & startup seed logic
│   │   └── models.py         # Database models & Pydantic schemas
│   ├── tests/                # Pytest execution scripts
│   ├── car_dealership.db     # SQLite database
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Main React component & API handlers
│   │   ├── main.jsx          # DOM entry point
│   │   └── index.css         # Styling rules
│   ├── package.json          # Node dependencies
│   └── vite.config.js        # Vite development configuration
├── README.md                 # Technical documentation
└── PROMPTS.md                # AI engineering process log
