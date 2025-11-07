# 🧠 Apache JIRA → JSONL Scraper (Technical Assignment Submission)
### Candidate: **Prudhvi Raj**
### Repository: [https://github.com/prudhvilabcd/apache-jira-scraper](https://github.com/prudhvilabcd/apache-jira-scraper)

---

## 📘 Overview  
This project scrapes public issues from **[Apache’s JIRA portal](https://issues.apache.org/jira)** for selected open-source projects such as Hadoop, Hive, and HBase.  
It automatically handles pagination, rate limits, and transforms raw HTML/JSON data into clean **JSONL** format suitable for ML or analytics.

✅ **Goal:** Build a reliable, resumable web scraping pipeline that produces structured datasets from Apache JIRA.  

---

## ⚙️ Features Implemented

| Feature | Description | Status |
|----------|--------------|--------|
| **Data Scraping** | Fetches issues, metadata, and comments | ✅ |
| **Pagination Handling** | Iteratively scrapes multiple pages efficiently | ✅ |
| **Error Handling** | Handles HTTP 429 & 504 with exponential backoff | ✅ |
| **Resume Capability** | Uses checkpoints to continue from the last successful state | ✅ |
| **Data Transformation** | Converts HTML → Plain Text using BeautifulSoup | ✅ |
| **JSONL Output** | Outputs one issue per line in structured JSONL format | ✅ |
| **Configurable Parameters** | Project keys, retry count, page size in YAML config | ✅ |
| **Incremental Checkpoints** | Updates after each issue for fault tolerance | ✅ |

---

## 🧩 System Architecture

```
├── src/
│   ├── main.py          # Entry point – orchestrates scraping
│   ├── scraper.py       # Fetches data from JIRA REST API
│   ├── transform.py     # Cleans & converts data to JSONL
│   ├── utils.py         # Checkpoint manager, helpers
│
├── checkpoints/         # Stores progress for each project
├── data/                # Final JSONL output files
├── config.yaml          # Configuration file (editable)
├── requirements.txt     # Python dependencies
├── README.md            # Documentation (this file)
```

---

## ⚙️ Setup Instructions

### 1️⃣ Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # For Windows
# source venv/bin/activate  # For Linux/Mac
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration (config.yaml)

```yaml
projects:
  - HADOOP
  - HBASE
  - HIVE

output_dir: data
page_size: 100

retry:
  max_retries: 5
  base_sleep_seconds: 2
  max_sleep_seconds: 60
```

🔹 You can replace projects with any Apache JIRA key (e.g., `KAFKA`, `SPARK`, `ZOOKEEPER`).  

---

## ▶️ Run the Project

```bash
python -m src.main --config config.yaml
```

This will generate files under `/data/{PROJECT}.json` and update `/checkpoints/{PROJECT}.json`.  

---

## 📊 Example Output (JSONL)

```json
{
  "project": "HADOOP",
  "issue_key": "HADOOP-9999",
  "metadata": {
    "title": "Fix NullPointerException in namenode",
    "status": "Open",
    "priority": "Major",
    "assignee": "user123",
    "created": "2025-11-07T11:23:45",
    "updated": "2025-11-07T12:34:56"
  },
  "description": "Detailed issue description here...",
  "comments": ["plain text comment 1", "plain text comment 2"],
  "classification_target": "Open"
}
```

---

## 🧠 Design & Architecture Highlights

| Area | Implementation |
|------|----------------|
| **API-based Scraping** | Uses JIRA REST API (`/rest/api/2/search`) instead of HTML for efficiency |
| **Resumable Execution** | Checkpoints for each project (`last_updated_iso`, `seen_keys`) |
| **Transformation Layer** | Cleans HTML → plain text and appends derived fields |
| **Fault Tolerance** | Retries failed requests with exponential backoff |
| **Extensibility** | Modular codebase; can add new projects easily |

---

## ⚡ Performance Metrics

| Project | Issues Scraped | Time Taken | Speed |
|----------|----------------|-------------|--------|
| **HADOOP** | 13,615 | 26s | ~5.4 issues/s |
| **HBASE** | 29,468 | 2h 3m | ~3.9 issues/s |
| **HIVE** | 29,978 | 1h 44m | ~4.7 issues/s |

---

## 🚀 Future Enhancements
- Multi-threaded scraping for faster speed  
- Integrate summarization or NLP preprocessing for JSONL datasets  
- Add Dockerfile + CI/CD setup  
- SQLite backend for stronger checkpointing  

---

## 🧾 Notes for Evaluation
- All data collected from **public Apache JIRA endpoints** — no authentication required  
- Dataset stored as `.jsonl` for downstream ML/LLM use cases  
- Code is **idempotent** (safe to re-run) and **recoverable** from last checkpoint  

---

## 📂 Data Access (Google Drive)
Due to GitHub’s 25MB file upload limit, the full dataset (≈900MB JSONL) is stored here:  
📎 **[Google Drive Link – Data Folder](https://drive.google.com/drive/folders/1hkzbmajJ4ofY4zS58_hg-Z90mP3xjit?usp=sharing)**  

---

## 📥 Repository Access
🔗 **GitHub Repo:** [https://github.com/prudhvilabcd/apache-jira-scraper](https://github.com/prudhvilabcd/apache-jira-scraper)  
📦 **ZIP Download:** [Click to Download ZIP](https://github.com/prudhvilabcd/apache-jira-scraper/archive/refs/heads/main.zip)

---

## 👨‍💻 Author
**Name:** Prudhvi Raj  
**Role:** M.Tech (CSE) Student, NIT Delhi  
**Focus Areas:** AI, ML, and Data Mining  

---

## ⭐ Support
If this project was part of your review, please ⭐ it on GitHub — it helps recognition and visibility.

---
