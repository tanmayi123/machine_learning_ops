# Airflow Lab 1 — K-Means Clustering Pipeline with Enhancements

Airflow pipeline that performs K-Means clustering on credit card data, containerized with Docker, and enhanced with an auto-generated interactive dashboard and email alerting.

---

## Lab Structure

```
airflow_lab/
├── setup.sh                  # Environment setup script
├── docker-compose.yaml       # Docker Compose configuration
├── .env                      # Environment variables (secrets, not pushed to GitHub)
├── .gitignore                # Git ignore rules
├── config/
│   └── airflow.cfg           # Airflow configuration
├── dags/
│   ├── airflow.py            # DAG definition (5 tasks)
│   ├── data/
│   │   ├── file.csv          # Training data
│   │   └── test.csv          # Test data for predictions
│   ├── dashboard/
│   │   └── dashboard.html    # Auto-generated HTML dashboard (gitignored)
│   └── src/
│       ├── __init__.py       # Empty init file
│       └── lab.py            # Core ML functions
```

---

## What This Pipeline Does

This pipeline performs unsupervised machine learning using **K-Means clustering** on credit card customer data. It automatically determines the optimal number of clusters using the **Elbow Method** and generates a full visual dashboard of results.

### Dataset Features Used
- `BALANCE` — Credit card balance
- `PURCHASES` — Total purchases made
- `CREDIT_LIMIT` — Credit limit assigned

---

## Prerequisites

- **Docker Desktop** (4GB+ memory allocated, 8GB recommended)
- **Git**
- **Python 3.x**
- A **Gmail account** with an App Password (for email alerts)

---

## Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your_username/airflow_lab.git
cd airflow_lab
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
AIRFLOW_UID=501
AIRFLOW__SMTP__SMTP_USER=your_gmail@gmail.com
AIRFLOW__SMTP__SMTP_PASSWORD=your_16_char_app_password
AIRFLOW__SMTP__SMTP_MAIL_FROM=your_gmail@gmail.com
ALERT_EMAIL=your_gmail@gmail.com
```

> Never commit `.env` to GitHub. It is already listed in `.gitignore`.

### 3. Initialize Airflow

```bash
mkdir -p ./logs ./plugins ./config
echo "AIRFLOW_UID=$(id -u)" >> .env
docker compose up airflow-init
```

Wait for:
```
User "airflow2" created with role "Admin"
airflow-init exited with code 0
```

### 4. Start Airflow

```bash
docker compose up
```

Wait until you see:
```
airflow-webserver-1 | "GET /health HTTP/1.1" 200 141
```

### 5. Access the UI

Open **http://localhost:8080** and log in with:
- **Username:** `airflow2`
- **Password:** `airflow2`

---

## DAG: Airflow_Lab1

The DAG consists of **5 tasks** running sequentially:

```
load_data_task
      ↓
data_preprocessing_task
      ↓
build_save_model_task
      ↓
load_model_task
      ↓
generate_dashboard_task   ⭐ Enhancement
```

### Task Descriptions

| Task | Description |
|------|-------------|
| `load_data_task` | Loads `file.csv`, serializes with pickle + base64 for XCom |
| `data_preprocessing_task` | Drops nulls, selects features, applies MinMax scaling |
| `build_save_model_task` | Fits KMeans for k=1–49, saves model, returns SSE values |
| `load_model_task` | Loads model, finds optimal k via elbow method, predicts on `test.csv` |
| `generate_dashboard_task` | Generates interactive HTML dashboard with plots and metrics ⭐ |

### Triggering the DAG

In the Airflow UI, click the **▶ (play)** button next to `Airflow_Lab1` to trigger a manual run.

---

## Core ML Functions (`dags/src/lab.py`)

### `load_data()`
Loads `file.csv` and returns base64-encoded pickled DataFrame for XCom-safe transfer between tasks.

### `data_preprocessing(data_b64)`
- Drops null values
- Selects `BALANCE`, `PURCHASES`, `CREDIT_LIMIT` columns
- Applies **MinMaxScaler** normalization
- Returns base64-encoded pickled numpy array

### `build_save_model(data_b64, filename)`
- Fits **KMeans** for k = 1 to 49
- Saves the final model to `dags/model/filename`
- Returns list of SSE (inertia) values

### `load_model_elbow(filename, sse)`
- Loads saved model
- Uses **KneeLocator** to find optimal k from elbow curve
- Runs predictions on `test.csv`
- Returns prediction as JSON-safe integer

### `generate_dashboard(data_b64, sse, optimal_k)` ⭐
- Recomputes KMeans with optimal k
- Calculates **Silhouette Score**
- Generates interactive **Plotly** charts
- Saves `dashboard.html` to `dags/dashboard/`

---

## ⭐ Enhancements

### Enhancement 1 — Auto-Generated Interactive HTML Dashboard

A 5th DAG task (`generate_dashboard_task`) automatically generates a rich HTML dashboard after every successful pipeline run.

**Dashboard includes:**
- **Elbow Curve** — SSE vs number of clusters with optimal k marked by a red dashed line
- **Cluster Distribution** — Bar chart showing number of data points per cluster
- **Model Metrics Table:**
  - Optimal K (Elbow Method)
  - Silhouette Score
  - Min/Max SSE
  - Run timestamp

**Built with:** Plotly (interactive, zoomable charts)

**Output location:** `dags/dashboard/dashboard.html`

To view after a run:
```bash
open ~/airflow_lab/dags/dashboard/dashboard.html
```

---

### Enhancement 2 — Email Alerts on DAG Success/Failure

Automated email notifications are sent after every DAG run using Gmail SMTP.

**Success email** — sent when all 5 tasks complete successfully:
- DAG name
- Run ID
- Completion timestamp

**Failure email** — sent when any task fails:
- DAG name
- Failed task name
- Run ID
- Failure timestamp

**Setup:**
Configured via environment variables in `.env` and `docker-compose.yaml` using Airflow's built-in SMTP integration. Gmail App Password is required (never hardcoded).

---

## Security

- All secrets (Gmail credentials, SMTP password) are stored in `.env`
- `.env` is listed in `.gitignore` and never pushed to GitHub
- `docker-compose.yaml` references secrets via `${VARIABLE}` syntax
- `ALERT_EMAIL` is read at runtime via `os.environ.get('ALERT_EMAIL')`

---

## Python Dependencies

Installed automatically via `_PIP_ADDITIONAL_REQUIREMENTS` in `docker-compose.yaml`:

```
pandas
scikit-learn
kneed
plotly
```

---

## Stopping Airflow

```bash
docker compose down
```

To also remove volumes:
```bash
docker compose down -v
```
![WhatsApp Image 2026-02-24 at 1 58 00 PM](https://github.com/user-attachments/assets/4bc714e3-e144-4fe2-8adf-ad241957fbd6)

![WhatsApp Image 2026-02-24 at 1 59 01 PM](https://github.com/user-attachments/assets/2b6ad851-253a-48fd-92bb-043a37ce533f)

![WhatsApp Image 2026-02-24 at 1 59 24 PM](https://github.com/user-attachments/assets/e00b01a9-79e4-4314-a41e-b2745892f07f)

![WhatsApp Image 2026-02-24 at 2 28 55 PM](https://github.com/user-attachments/assets/453d2913-45db-4863-8514-404a0bb7042c)

![WhatsApp Image 2026-02-24 at 2 30 33 PM](https://github.com/user-attachments/assets/ab06a962-0f59-4e18-9f5f-aab5979c0c1f)

![WhatsApp Image 2026-02-24 at 2 45 07 PM](https://github.com/user-attachments/assets/03ec1dd7-d4bc-4c04-83de-87ccfb63b87f)

![WhatsApp Image 2026-02-24 at 2 47 41 PM](https://github.com/user-attachments/assets/65ac371a-ac40-4159-ab2a-4f8a66db5eda)


---
