# 🏠 Housing Market Intelligence Web Application

An interactive Python analytical dashboard built with **Streamlit** and **Plotly** to visualize property sales data, replacing legacy Tableau workbooks[cite: 1].

---

## 📌 Project Overview

This application provides real-time filtering and visualization of residential housing data[cite: 1]. It features:
- **Top-line KPI Cards**: Key metrics including median sales price, price per square foot, total listings, and average year built.
- **Geospatial Mapping**: OpenStreetMap integration displaying property locations scaled by square footage and colored by price.
- **Price vs. Area Analysis**: Scatter plots with ordinary least squares (OLS) regression trendlines.
- **Categorical Distributions**: Interactive distribution plots grouped by bedrooms, bathrooms, condition, or property grade.
- **Data Export**: Expanded table viewer with CSV download functionality for filtered record sets.

---

## 📁 Repository Structure

```text
tableau-to-webapp/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions deployment workflow
├── data/
│   └── Housing Dataset.xlsx    # Source property sales dataset[cite: 1]
├── src/
│   ├── app.py                  # Main Streamlit layout & filter logic
│   ├── components.py           # Plotly chart & KPI component functions
│   └── data_loader.py          # Data ingestion & cleaning pipeline
├── Dockerfile                  # Container build instructions
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

---

## 🚀 Local Setup & Development

### Prerequisites
- Python 3.9+ installed on your machine.
- Source file `Housing Dataset.xlsx` placed inside the `data/` folder[cite: 1].

### Step 1: Open Terminal & Navigate to Project Directory
```cmd
cd path/to/tableau-to-webapp
```

### Step 2: Create and Activate Virtual Environment
* **Windows (Command Prompt):**
  ```cmd
  python -m venv venv
  .\venv\Scripts\activate.bat
  ```
* **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
* **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Streamlit Application
```bash
streamlit run src/app.py
```
*The app will automatically open in your browser at `http://localhost:8501`.*

---

## 🐳 Running with Docker Locally

To test the containerized version locally before cloud deployment:

```bash
# Build the Docker image
docker build -t housing-app .

# Run the container locally on port 8080
docker run -p 8080:8080 housing-app
```
*Access the app in your browser at `http://localhost:8080`.*

---

## ☁️ Google Cloud Run Deployment

### 1. Enable Required GCP APIs
```bash
gcloud services enable run.googleapis.com artifactregistry.googleapis.com
```

### 2. Create Artifact Registry Repository
```bash
gcloud artifacts repositories create housing-repo \
    --repository-format=docker \
    --location=us-central1
```

### 3. Deploy via GitHub Actions CI/CD
Whenever code is pushed to the `main` branch, the workflow inside `.github/workflows/deploy.yml` will automatically build the image and publish it to Cloud Run.

**Required GitHub Repository Secrets** (`Settings -> Secrets and variables -> Actions`):
- `GCP_PROJECT_ID`: Your GCP Project ID.
- `GCP_SA_KEY`: JSON private key for a GCP Service Account with `Cloud Run Developer` and `Artifact Registry Writer` permissions.