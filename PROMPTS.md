# Raw AI Prompting Log & Conversation History

This document contains the unedited prompt history and engineering interactions used to build, debug, and refine the Car Dealership Inventory System.

---

### Prompt 1: Initial Architecture & Database Seeding
> **User Prompt:** "Dear I have one doubt why cannot you make that already 10 car models should be there to show to the customers to search. Now whatever we are doing is like we have to add and update it should not be like that right"

* **AI Assistance:** Implemented `@app.on_event("startup")` in FastAPI to automatically seed 10 default vehicle entries into the SQLite database (`car_dealership.db`) on startup using SQLAlchemy.

---

### Prompt 2: API Route Operations & Admin Examples
> **User Prompt:** "Can you give Audi example for delete and restock and update"

* **AI Assistance:** Formatted REST API requests for `/api/vehicles/{id}` endpoints showing how to restock stock levels (`+1`), update vehicle metadata, and perform deletion on specific vehicle records like Audi models.

---

### Prompt 3: Environment Setup & Dual Terminal Execution
> **User Prompt:** "Dear, how to make both the backend and frontend VS Code visible... Dear I am not understanding, up to now we updated the entire main.py right? That is in the backend now, should I run this in the backend itself or do I have to move to the frontend?"

* **AI Assistance:** Guided the setup of split terminals in VS Code (`Ctrl + ~`), running `uvicorn app.main:app --reload` inside `/backend` and `npm run dev` inside `/frontend`.

---

### Prompt 4: UI/UX & Visual Styling Enhancements
> **User Prompt:** "Is it happening in that web and also now that web is actually looking so simple can we make it colourful is it possible"

* **AI Assistance:** Refined CSS card layouts, adjusted color schemes, and enhanced button hover/disabled states for stock counts (`quantity == 0`).

---

### Prompt 5: Git Remote Configuration & Debugging
> **User Prompt:** "fatal: 'origin' does not appear to be a git repository / fatal: Could not read from remote repository. Please make sure you have the correct access rights and the repository exists. (venv) PS C:\Users\dell\car-dealership-inventory\backend>"

* **AI Assistance:** Resolved Git remote pathing errors by re-orienting terminal execution to the root directory (`cd ..`) and adding the GitHub remote origin URL.

---

### Prompt 6: Application Testing & Workflow Steps
> **User Prompt:** "Dear give the steps like how to test the web application line by line"

* **AI Assistance:** Provided step-by-step instructions for executing Pytest suite on backend API routes and validating live frontend operations (Search, Buy, Restock, Delete, Add).