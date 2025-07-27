# DeltaQuanta

> **Data Engineering Excellence Starts Here**  
> A fully containerized Lakehouse pipeline with Delta Lake, Spark optimizations, and Prefect orchestration.

---

## 🏷️ Key Features

- **Modern Lakehouse Architecture**  
  - Delta Lake storage with ACID transactions & time‑travel  
  - Spark SQL & DataFrame optimizations (caching, partition pruning)

- **Data Lake & Partitioning Design**  
  - Directory layout:
    ```text
    └─ data/lake/
       ├─ stocks_delta/       # raw Delta tables
       │  ├─ symbol=AAPL/
       │  ├─ symbol=TSLA/
       │  └─ _delta_log/
       └─ stocks_enriched/    # enriched with factors
          ├─ symbol=AAPL/
          └─ symbol=TSLA/
    ```

- **End‑to‑End Docker Packaging**  
  - One‑step `docker compose up --build`  
  - Services: Prefect Orion, Spark ETL, MinIO (S3), your Python app

- **Automated Workflow**  
  - Prefect 2.x flow with daily scheduling, email alerts, parameterization  
  - CI/CD via GitHub Actions on every push to `main`

---

## ⚙️ Architecture Overview

```text
[ Finnhub API ]
       ↓
 [ /ingestion/fetch_stock_data.py ]
       ↓
   Raw JSON → data/lake/stocks_delta
       ↓
 [ etl/spark_job.py → transform_indicators ]
       ↓
 Enriched Delta → data/lake/stocks_enriched
       ↓
 [ workflows/prefect_pipeline.py ]
       ↓
 Scheduled daily, alerts on failure
       ↓
   Docker Compose & GitHub Actions
```

---

## 📦 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/cl17189/quantlake.git
cd quantlake

# 2. Configure environment
cp .env.sample .env  # then edit the file
# Fill in:
# FINNHUB_API_KEY=your_token
# AWS_ACCESS_KEY_ID=minio
# AWS_SECRET_ACCESS_KEY=minio123
# MINIO_ENDPOINT=http://minio:9000

# 3. Build and launch
cd docker
docker compose up --build
```

---

## 📊 Computed Indicators

| Category        | Indicator                   |
| --------------- | --------------------------- |
| **Price Action**| `price_change_pct`, `ma_5`, `ma_20`, `price_volatility_7d`, `jump_risk_index` |
| **Volume Flow** | `volume_spike_ratio`, `turnover_ratio`              |
| **Impact & Liquidity** | `price_impact_factor`, `abnormal_volume_index`   |
| **Fundamentals**| `pe_ratio`, `eps`, `revenue`       |
| **(Optional)**  | `news_sentiment_score`             |

---

## 🔧 Tech Stack

![Tech Stack](pic/tech_stack.jpg)

- **Python 3.10** · **PySpark** · **delta-spark**  
- **Prefect 2.x** · **Docker & Docker Compose**  
- **MinIO** (S3‑compatible) · **GitHub Actions**

---


## 📬 License & Contact

- Released under the MIT License  
