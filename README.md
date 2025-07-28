# DeltaQuanta

> **Data Engineering Excellence Starts Here**  
> A fully containerized Lakehouse pipeline with Delta Lake, Spark optimizations, and Prefect orchestration.

---

## 🏷️ Key Features

- **Modern Lakehouse Architecture**  
  - Delta Lake storage with ACID transactions & time‑travel  
  - Spark SQL & DataFrame optimizations (caching, partition pruning, AQE)
- **Data Lake & Partitioning Design**  
  - Separate Delta tables per factor type  
  - Partitioned by `symbol` and date fields for each table  
  - Z-Order on `symbol` to speed up point lookups
- **End‑to‑End Docker Packaging**  
  - One‑step `docker compose up --build`  
  - Services: Prefect Orion, Spark ETL, MinIO (S3), Streamlit app  
- **Automated Workflow & CI/CD**  
  - Prefect 2.x flows with daily scheduling, alerts  
  - GitHub Actions on push to `main`

---

## ⚙️ Partitioned Table Structure

Below is the directory layout under `data/lake/`, showing partitions for each Delta table:

```
data/lake/  
├── PriceFactors/ # Price related features  
│ ├── symbol=AAPL/ # Partition by symbol  
│ │ ├── trade_date=2025-07-01/part-...snappy.parquet  
│ │ └── trade_date=2025-07-02/...  
│ └── symbol=TSLA/  
├── VolumeFactors/ # Volume related features  
│ └── symbol=AAPL/  
│ └── trade_date=2025-07-01/...  
├── ImpactFactors/ # Impact & liquidity features  
│ └── symbol=AAPL/  
│ └── trade_date=2025-07-01/...  
└── Fundamentals/ # Fundamental metrics   
└── symbol=AAPL/   
├── report_date=2025-07-27/part-...parquet   
└── report_date=2025-04-30/...
```

- **PriceFactors** partition keys: `symbol`, `trade_date`
- **VolumeFactors** partition keys: `symbol`, `trade_date`
- **ImpactFactors** partition keys: `symbol`, `trade_date`
- **Fundamentals** partition keys: `symbol`, `report_date`

Partitioning by date fields ensures predicate pushdown and efficient scans.

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
