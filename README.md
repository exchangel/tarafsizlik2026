# Tarafsızlık Türkiye (Objective Turkey)

A media analysis platform that aggregates and clusters news from 36 Turkish news sources to identify editorial stances and differences in coverage.

## Live Demo
[tarafsizlik2026.streamlit.app](https://tarafsizlik2026.streamlit.app/)

## Overview
**Tarafsızlık Türkiye** collects news articles from 36 national RSS feeds spanning various political alignments (Left/Opposition, Center/Independent, Right/Pro-Government). 

The platform uses LLM-based clustering (Google Gemini) to group articles covering the same event. It provides a visual breakdown of editorial coverage per topic and highlights "Blindspots" — events that are covered by one political alignment but omitted by another.

## Architecture
- **Data Ingestion (`veri_cekici.py`):** Fetches RSS feeds incrementally to prevent duplicate processing.
- **Data Processing (`ai_analiz.py`):** Uses Google Gemini via API to cluster identical events and assign standardized tags. Enforces a 30-day rolling window to manage dataset size.
- **CI/CD Pipeline (GitHub Actions):** Scheduled via cron to run 3 times a day. Triggers data scraping, runs the clustering, and commits the updated dataset.
- **Frontend (Streamlit):** A responsive, multi-language (TR/EN) web application directly linked to the repository. 

## Technology Stack
- **Python** (Pandas, Feedparser)
- **Streamlit** (Web UI)
- **Google GenAI (Gemini)** (Text Clustering)
- **Plotly** (Data Visualization)
- **GitHub Actions** (Automation)

## Testing & Validation
- **Unique Source Counting:** Ensures multiple articles from the same source on a single topic are counted once in the editorial distribution.
- **Timezone Standardization:** Standardizes mixed RSS publication dates (offset-aware and offset-naive) to UTC and naive formats for consistent filtering (24h, 7d, 30d).
- **Incremental Fetching:** Verifies that previously processed article links are skipped to reduce unnecessary API calls.

## Local Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/exchangel/tarafsizlik2026.git
   cd tarafsizlik2026
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your Gemini API Key as an environment variable:
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```
4. Run the data pipeline:
   ```bash
   python veri_cekici.py
   python ai_analiz.py
   ```
5. Launch the application:
   ```bash
   streamlit run uygulama.py
   ```

## Author
Levent

