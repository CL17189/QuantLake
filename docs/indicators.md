# 📊 Finance DE Pipeline: Data Engineering for Quant Research

**Data Engineering Excellence Starts From Here.**  
This project builds an automated and scalable data pipeline for stock market analysis, designed for quant researchers, analysts, and data scientists.

---

## 🧱 Project Architecture

- **API Ingestion**: Fetch real-time and historical market data from [Finnhub](https://finnhub.io/)
- **ETL with PySpark**: Clean, transform, and enrich data with derived indicators
- **Delta Lake Storage**: Store structured partitions in Delta format with versioning
- **Workflow Automation**: Managed by [Prefect 2.x](https://www.prefect.io/)
- **Deployment**: Containerized with Docker, orchestrated via GitHub Actions

---

## 🎯 Who Is This For?

> This platform is designed for **quantitative researchers and financial data scientists**  
> who need clean, reliable, and feature-rich stock data for backtesting or model training.

---

## 📐 Extracted Metrics & Indicators

Below is a curated list of traditional and advanced indicators that are automatically computed in the ETL pipeline.

| Category        | Indicator                    | Description |
|----------------|------------------------------|-------------|
| 📈 Price Action | `price_change_pct`           | Daily price change percentage $(P_t - P_{t-1})/P_{t-1}$ |
|                | `ma_5`, `ma_20`               | Moving averages over 5 and 20 days |
|                | `price_volatility_7d`        | 7-day rolling volatility |
|                | `jump_risk_index`            | Count of extreme price movements over past 7 days |
| 📊 Volume & Flow| `volume_spike_ratio`         | Current volume vs 7-day average |
|                | `turnover_ratio`             | Volume / Market Cap |
|                | `price_impact_factor`        | $(P_{high} - P_{low}) / volume$ |
| ⚡ Innovation   | `abnormal_volume_index (AVI)`| Z-score of today’s volume vs 30-day history |
|                | `composite_liquidity_score`  | Combines spread, volume, turnover |
| 🧱 Fundamentals | `pe_ratio`, `eps`, `revenue` | Extracted via profile API |
| 🧠 Sentiment    | `news_sentiment_score`       | (Optional) via Finnhub NLP API |

---

## 🔧 Technologies Used

> ![Tech Stack](../pic/tech_stack.jpg)

| Tool       | Purpose            |
|------------|--------------------|
| PySpark    | Data transformation |
| Delta Lake | Storage & versioning |
| Prefect    | Workflow orchestration |
| Docker     | Environment isolation |
| GitHub Actions | CI/CD automation |
| MinIO      | Local S3-compatible data lake |

---

## 📦 Output Structure

s3a://datalake/stocks_delta/
├── symbol=AAPL/
│ ├── part-0000.snappy.parquet
│ └── _delta_log/

---

## 🚀 Example Use Cases

- 📈 **Backtest** momentum or volatility strategies with engineered features  
- 🔬 **Train ML models** on long-horizon indicators  
- 📊 **Visualize stock performance** with dynamic dashboards

---

## 📬 Contact

> Built by [Your Name or GitHub Handle](https://github.com/yourprofile)  
> For questions or collaboration: your_email@example.com
