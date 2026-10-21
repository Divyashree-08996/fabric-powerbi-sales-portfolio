# Alex Rivera — Data Analyst & Power BI Developer Portfolio

A high-performance, clean minimalist light portfolio tailored specifically for **Data Analysts**, **Power BI Developers**, and **Python Analytics Practitioners**.

---

## 🌟 Highlights & Features

- **Aesthetic**: Clean Minimalist Light with crisp Inter typography, high-contrast metrics, refined borders, and generous whitespace.
- **Interactive Executive BI Simulator**: Built with dynamic filters (Territory & Period) and interactive Chart.js visualizations that dynamically recalculate KPIs (Revenue, Margin, Accounts, Churn).
- **In-Depth Case Studies**: Real-world business scenarios including:
  1. *Enterprise SAP Partner 360 & Analytics in Microsoft Fabric* (Fabric OneLake + PySpark Delta Lake + Direct Lake Power BI)
  2. *Executive B2B Sales & Margins Command Center* (Power BI + DAX)
  3. *E-Commerce RFM Segmentation Engine* (Python + Scikit-Learn)
  4. *Supply Chain & Stockout Prevention System* (Power BI + Python ETL)
  5. *Automated SQL Data Quality & Reconciliation Suite* (PostgreSQL + Python)
- **Production Code Snippets**: Expandable, syntax-highlighted PySpark Delta merges, DAX measures, and Python clustering pipelines.
- **Skills Matrix & Certifications**: Showcasing DP-600 (Fabric Analytics Engineer Associate), PL-300 (Microsoft Power BI Data Analyst Associate), PCAP Python, and SQL optimization.

---

## 🚀 How to Run

### Option 1: Instant Direct Browser Preview (Zero Setup)
Simply double-click or open [index.html](file:///c:/Users/hp/Documents/antigravity/dazzling-hypatia/index.html) directly in any modern web browser (Chrome, Edge, Firefox, Safari). No installation or build step required!

---

### Option 2: Python Flask Web Server
Run the lightweight Python backend server that serves the portfolio and REST API endpoints:

```bash
# 1. Install dependencies (if not already installed)
pip install -r requirements.txt

# 2. Run the application
python app.py
```
Then navigate to: **`http://127.0.0.1:5000`**

#### Available API Endpoints:
- `GET /api/projects` — Retrieve case studies in JSON format (supports `?category=powerbi` filtering)
- `GET /api/metrics` — Retrieve career benchmark numbers
- `POST /api/contact` — Handle visitor contact submissions

---

### Option 3: Python Streamlit Application
For a native, pure Python data app experience powered by Streamlit and Plotly:

```bash
# Run Streamlit
streamlit run portfolio_streamlit.py
```
This opens an interactive data dashboard with live sliders, Plotly charts, and tabbed case studies.

---

## 📁 Project Structure

```text
├── index.html              # Standalone Clean Minimalist Light Web Portfolio
├── app.py                  # Python Flask server & REST API
├── portfolio_streamlit.py  # Python Streamlit data portfolio app
├── requirements.txt        # Python package requirements
├── .streamlit/
│   └── config.toml         # Streamlit clean light theme configuration
└── README.md               # Documentation and guide
```

---

## ✏️ How to Customize

1. **Personal Information & Name**:
   - In [index.html](file:///c:/Users/hp/Documents/antigravity/dazzling-hypatia/index.html), search for `Alex Rivera` and replace with your name.
   - Update your contact links, LinkedIn, and GitHub in the Contact section.
2. **Projects**:
   - Add or modify case studies in both [index.html](file:///c:/Users/hp/Documents/antigravity/dazzling-hypatia/index.html) and [app.py](file:///c:/Users/hp/Documents/antigravity/dazzling-hypatia/app.py) (`PROJECTS_DATA`).
3. **Deploying**:
   - **GitHub Pages**: Simply push this repo to GitHub and enable GitHub Pages on `main` branch.
   - **Streamlit Community Cloud**: Connect your repository and select `portfolio_streamlit.py`.
   - **Render / Railway / Heroku**: Deploy `app.py` directly with `gunicorn app:app`.
