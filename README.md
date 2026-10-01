# 🧠 Student Vocal AI Profiling & Neuro Analytics Dashboard

An enterprise-ready, highly scalable interactive web application built with **Streamlit** and **Plotly** to visualize student vocal delivery metrics and AI-synthesized behavioral profiles.

## 🚨 IMPORTANT DATA INTEGRATION NOTE
**This dashboard does not rely on static dummy coding data.** 
The architecture is dynamically connected to your **Google Colab Notebook pipeline**. Every time you run the final cell of the Colab execution stack, it dynamically extracts and overwrites the local data storage with **REAL, AUTHENTIC STUDENT DATA** captured from live observations and your Groq API workflows.

---

## 🛠️ How to Deploy & Update the Dashboard

### Step 1: Export Real Data from Your Colab Notebook
1. Open and execute your integrated **Google Colab Notebook**.
2. Run the pipeline sequentially until you execute the very last code cell.
3. The final cell will automatically flush out template parameters and dump your actual student records into a local folder named `data/` across 3 clean files (`student_meta.csv`, `live_obs.csv`, and `ai_insights.csv`).

### Step 2: Install UI Dependencies
Open your terminal or command line prompt inside this project folder and run:
```bash
pip install -r requirements.txt
```

### Step 3: Launch the Dynamic Portal
Execute the following command to boot up the web instance:
```bash
streamlit run app.py
```
The dashboard will automatically open in a local browser window (`http://localhost:8501`), populating your **Real Student Records**, **Genuine Groq AI Text Profiles**, and your specialized **3D Neuro Map Triangle** (*Vocal Confidence, Processing Flow, and Linguistic Precision*).
