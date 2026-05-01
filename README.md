# 🚀 Automated Crypto Data Pipeline (Local)

This project is an automated data pipeline that collects, processes, stores, and visualizes cryptocurrency price data (Bitcoin & Ethereum) from a public API. The pipeline is designed to run locally and supports periodic data updates using task scheduling.

---

## 📌 Project Overview

The system performs:
- Data extraction from API (CoinGecko)
- Data storage into SQLite database
- Data validation (duplicate prevention)
- Data visualization (time-series trend)
- Logging system for monitoring
- Optional email reporting

This project demonstrates a simple **end-to-end ETL pipeline** with automation capabilities.

---

## ⚙️ Tech Stack

- Python
- requests (API handling)
- SQLite (data storage)
- matplotlib (visualization)
- smtplib (email reporting)
- OS & datetime (automation support)

---

## 🔄 Pipeline Flow

1. **Extract**
   - Fetch cryptocurrency prices (BTC & ETH) from CoinGecko API

2. **Transform**
   - Validate new data (avoid duplicates)
   - Structure data for storage

3. **Load**
   - Store data into SQLite database

4. **Visualize**
   - Generate trend chart for recent data

5. **Monitor**
   - Save logs for each execution

6. **(Optional) Notify**
   - Send report via email with chart attachment

---

## 📊 Features

- ✅ Automated data collection from API  
- ✅ Duplicate data prevention  
- ✅ SQLite-based data storage  
- ✅ Time-series visualization  
- ✅ Logging system  
- ✅ Ready for scheduling (Task Scheduler / Cron)  
- 🔄 Email reporting (optional)

---

## 🖥️ How to Run (Local)

1. Clone repository:
```bash
git clone https://github.com/username/crypto-data-pipeline.git
cd crypto-data-pipeline
