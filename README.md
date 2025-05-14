# 🎮 Video Game Sales Dashboard

An interactive multi-page web dashboard built with [Dash](https://dash.plotly.com/), [Plotly](https://plotly.com/python/), and [Bootstrap](https://dash-bootstrap-components.opensource.faculty.ai/) to explore and visualize video game sales data.

## 📂 Project Structure

```
.
├── app.py
├── data/
│ └── video_games_sales.csv
├── pages/
│ ├── pg1.py # Summary dashboard
│ └── pg2.py # Interactive detailed analysis
├── README.md

```

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/ArmanFahradyan/DataVisualizationProject.git
cd DataVisualizationProject
```

### 2. Install Dependencies

Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Then install dependencies:

```bash
pip install dash plotly pandas dash-bootstrap-components
```

## 🚀 Run the App

```bash
python app.py
```

Then open your browser and go to: `http://127.0.0.1:8050/`

---
