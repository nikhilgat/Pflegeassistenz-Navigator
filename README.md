# Pflegeassistenz‑Navigator (Bim4Care)

The **Pflegeassistenz‑Navigator** is a prototype **web application** designed to help caregivers, nursing staff, and patients within **care facilities or assisted living environments**. It combines a **Python backend** with a **browser-based frontend** to provide a digital assistant for accessibility.

---

## What the App Does

- Provides a **simple, interactive web interface** to support orientation in care environments.
- Helps **care staff and elderly/disabled persons** by offering a tool which understands their medical condition and provides improvement suggestions.

In short: **Pflegeassistenz-Navigator is a care assistant — a web tool where a Python-Flask backend serves an HTML/JS frontend**

---

## Project Structure

```
Pflegeassistenz‑Navigator/
├─ .vscode/           # Editor settings
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
- Reduces **caregiver burden** by providing a digital assistant for daily requirements.
- 
---

## Next Steps

- To Document actual backend dependencies (add `requirements.txt`).
- Expand documentation of the `website/` frontend (pages, scripts, styles).
- Add screenshots and demo workflows to illustrate functionality.
- Include contribution guidelines and licensing details.

---

## License

MIT License.
