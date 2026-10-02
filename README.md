# Tarafsızlık Türkiye (Objective Turkey)

An objective, AI-powered media analysis platform that clusters current events across the Turkish media landscape to reveal editorial stances and coverage blindspots.

## Live Demo
[tarafsizlik2026.streamlit.app](https://tarafsizlik2026.streamlit.app/)

## Overview
In todays highly polarized media environment, it's often difficult to get a complete picture of current events. **Tarafsızlık Türkiye** automatically scrapes news from 36 national sources across the political spectrum (Left/Opposition, Center/Independent, Right/Pro-Government). 

Instead of relying on manual tagging, the platform utilizes AI to intelligently group articles discussing the exact same event. It then visualizes the editorial coverage ratio for each topic and highlights "Blindspots" —crucial events that are heavily covered by one side but completely ignored by the other.

## Architecture & Automation
This project is designed to be a fully autonomous, serverless, and zero-cost:
- **Data Ingestion (`veri_cekici.py`):** Periodically fetches RSS feeds from 36 sources. Built with an incremental design to fetch only new data and prevent duplicates.
- **AI Processing (`ai_analiz.py`):** Uses Google Gemini to group identical events and assign standardized tags. Enforces a 30-day rolling window to keep the dataset lightweight.
- **CI/CD Pipeline (GitHub Actions):** Runs automatically 3 times a day via Cron jobs. The workflow triggers data scraping, runs the AI analysis, and pushes the updated dataset back to the repository.
- **Frontend (Streamlit):** A responsive, multi-language (TR/EN) web application directly linked to the GitHub repository. Any automated data update instantly reflects on the live site.

## Tech Used
- **Python**
- **Streamlit** (UI & Cloud Deployment)
- **Pandas** (Data manipulation)
- **Feedparser** (RSS Scraping)
- **Google GenAI (Gemini)** (NLP clustering)
- **Plotly** (Data Visualization)
- **GitHub Actions** (CI/CD & Automation)

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
4. Run the data pipeline (if you want to fetch fresh data locally):
   ```bash
   python veri_cekici.py
   python ai_analiz.py
   ```
5. Launch the Streamlit app:
   ```bash
   streamlit run uygulama.py
   ```

## Author
Developed by Levent.
