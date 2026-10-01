
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Vocal AI Profiling Console", page_icon="🧠", layout="wide")

st.markdown("<style>.metric-card-box {background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.03); border: 1px solid #e2e8f0; text-align: center;} .profile-container {background: #f8fafc; padding: 25px; border-radius: 12px; border-left: 6px solid #6366f1; color: #1e293b;}</style>", unsafe_allow_html=True)

@st.cache_data(ttl=2)
def ingest_and_merge_datasets(data_dir="data"):
    meta_path = os.path.join(data_dir, "student_meta.csv")
    obs_path = os.path.join(data_dir, "live_obs.csv")
    ai_path = os.path.join(data_dir, "ai_insights.csv")
    
    if not (os.path.exists(meta_path) and os.path.exists(obs_path) and os.path.exists(ai_path)):
        st.warning("⚠️ Data files not found. Run the Colab export cell to populate real data.")
        demo_ids = ['STU001']
        return pd.DataFrame({'student_id': demo_ids, 'name': ['Waiting for Data'], 'general_confidence':, 'cognitive_load':, 'sentiment_positivity':, 'vocal_confidence':, 'processing_flow':, 'linguistic_precision':, 'ai_profile': ['Run your notebook cell to see real output here.']})

    try:
        df_meta = pd.read_csv(meta_path)
        df_obs = pd.read_csv(obs_path)
        df_ai = pd.read_csv(ai_path)
        for df_item in [df_meta, df_obs, df_ai]:
            if 'student_id' in df_item.columns:
                df_item['student_id'] = df_item['student_id'].astype(str).str.strip()
        merged_df = pd.merge(df_meta, df_obs, on="student_id", how="inner")
        final_df = pd.merge(merged_df, df_ai, on="student_id", how="inner")
        numeric_cols = ['general_confidence', 'cognitive_load', 'sentiment_positivity', 'vocal_confidence', 'processing_flow', 'linguistic_precision']
        for col in numeric_cols:
            if col in final_df.columns:
                final_df[col] = pd.to_numeric(final_df[col], errors='coerce').fillna(0)
        return final_df
    except Exception as e:
        st.error(f"Ingestion Error: {str(e)}")
        return pd.DataFrame()

df = ingest_and_merge_datasets()

if df.empty:
    st.error("No valid dataset available.")
    st.stop()

df['selector_string'] = df['student_id'].astype(str) + " - " + df['name'].astype(str)
st.sidebar.title("🧠 Neuro Map Console")
student_selection = st.sidebar.selectbox("Select Student Focus Track:", df['selector_string'].unique())
target_id = student_selection.split(" - ")[0]
student_data = df[df['student_id'] == target_id].iloc[0]

tab_overview, tab_deepdive = st.tabs(["📊 Global Cohort Metrics", "👤 Individual Vocal Profile & Neuro Map"])

with tab_overview:
    st.title("📊 Enterprise Overview Metric Matrix")
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
    with col_kpi1: st.markdown(f"<div class='metric-card-box'><small>Cohort Size</small><h3>{len(df)}</h3></div>", unsafe_allow_html=True)
    with col_kpi2: st.markdown(f"<div class='metric-card-box'><small>Avg Vocal Confidence</small><h3>{df['vocal_confidence'].mean():.1f}%</h3></div>", unsafe_allow_html=True)
    with col_kpi3: st.markdown(f"<div class='metric-card-box'><small>Avg Processing Flow</small><h3>{df['processing_flow'].mean():.1f}%</h3></div>", unsafe_allow_html=True)
    with col_kpi4: st.markdown(f"<div class='metric-card-box'><small>Avg Linguistic Precision</small><h3>{df['linguistic_precision'].mean():.1f}%</h3></div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🚨 Cognitive Load vs. General Confidence Spread")
    fig_scatter = px.scatter(df, x="general_confidence", y="cognitive_load", hover_name="name", size="processing_flow", color="vocal_confidence", color_continuous_scale=px.colors.sequential.Icefire, labels={"general_confidence": "General Confidence (%)", "cognitive_load": "Cognitive Stress (%)"}, template="plotly_white")
    fig_scatter.add_hline(y=75, line_dash="dash", line_color="#ef4444", annotation_text="High Cognitive Distress Zone")
    st.plotly_chart(fig_scatter, use_container_width=True)

with tab_deepdive:
    st.title(f"👤 Behavioral Deep Dive: {student_data['name']}")
    left_ui_panel, right_ui_panel = st.columns([1.1, 1])
    with left_ui_panel:
        st.subheader("🧠 3D Vocal Delivery Neuro Map")
        neuro_labels = ['Vocal Confidence', 'Processing Flow', 'Linguistic Precision']
        neuro_values = [float(student_data['vocal_confidence']), float(student_data['processing_flow']), float(student_data['linguistic_precision'])]
        labels_closed = neuro_labels + [neuro_labels[0]]
        values_closed = neuro_values + [neuro_values[0]]
        
        fig_neuro_map = go.Figure()
        fig_neuro_map.add_trace(go.Scatterpolar(r=values_closed, theta=labels_closed, fill='toself', fillcolor='rgba(99, 102, 241, 0.25)', line=dict(color='#6366f1', width=3)))
        fig_neuro_map.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, height=380, template="plotly_white")
        st.plotly_chart(fig_neuro_map, use_container_width=True)
        
        st.subheader("⚡ Context Indicators")
        st.markdown(f"**General Sentiment Positivity:** `{int(student_data['sentiment_positivity'])}%`")
        st.progress(int(max(0, min(100, student_data['sentiment_positivity']))))
        st.markdown(f"**Cognitive Load Exposure:** `{int(student_data['cognitive_load'])}%`")
        st.progress(int(max(0, min(100, student_data['cognitive_load']))))

    with right_ui_panel:
        st.subheader("🤖 Unstructured AI Profile (Groq Synthesized)")
        st.markdown(f"<div class='profile-container'>{student_data['ai_profile']}</div>", unsafe_allow_html=True)
