# Pflegeassistenz‑Navigator (Bim4Care)

The **Pflegeassistenz‑Navigator** is a prototype **web application** designed to help caregivers, nursing staff, and patients navigate and plan within **care facilities or assisted living environments**. It combines a **Python backend** with a **browser-based frontend** to provide a digital assistant for accessibility and orientation.

---

## What the App Does

- Provides a **simple, interactive web interface** to support orientation in care environments.
- Helps **care staff and elderly/disabled persons** by offering a tool to view and navigate spaces more effectively.
- Lays the groundwork for integration with **BIM (Building Information Modeling)**, enabling visualization of real-world floorplans with accessibility considerations (e.g., barrier-free routes).

In short: **Pflegeassistenz-Navigator is a care navigation assistant — a web tool where a Python backend serves an HTML/JS frontend to help plan and visualize accessible routes, rooms, and support information for patients and caregivers.**

---

## Project Structure

```
Pflegeassistenz‑Navigator/
├─ .vscode/           # Editor settings (optional)
├─ website/           # Frontend: HTML, CSS, JS files
├─ main.py            # Python backend server
├─ README.md          # Documentation
├─ .gitignore
```

---

## ⚙️ Components

### Backend (`main.py`)
- Built using **Flask**.
- Runs a local web server to serve the frontend.
- Includes simple routing and data handling logic.

### Frontend (`website/`)
- HTML/CSS/JavaScript files forming the user interface.
- Pages include **questionnaire, ai interaction window** for interacting with the system.

---

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/nikhilgat/Pflegeassistenz-Navigator.git
   cd Pflegeassistenz-Navigator
   ```

2. Set up a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # On Windows: .\venv\Scripts\activate
   pip install flask             # or fastapi/jinja2 if required
   ```

3. Run the backend:
   ```bash
   python main.py
   ```

4. Open your browser and go to:
   ```
   http://localhost:(your port)
   ```

---

## Why It Matters

- **Aging societies** need digital tools for elderly care and facility navigation.
- Reduces **caregiver burden** by providing a digital assistant for daily orientation tasks.
- Supports **accessibility goals** (wheelchair access, barrier-free routes, etc.).

---

## Next Steps

- Document actual backend dependencies (add `requirements.txt`).
- Expand documentation of the `website/` frontend (pages, scripts, styles).
- Add screenshots and demo workflows to illustrate functionality.
- Include contribution guidelines and licensing details.

---

## License

MIT License.
