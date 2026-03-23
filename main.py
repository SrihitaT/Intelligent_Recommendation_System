import streamlit as st
import pandas as pd
import numpy as np

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Student Analytics Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# CUSTOM CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #111827 50%, #0f0c29 100%);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(17, 24, 39, 0.95) !important;
    border-right: 1px solid rgba(99, 102, 241, 0.3);
}

/* Main header */
.dashboard-title {
    font-family: 'Space Mono', monospace;
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(90deg, #818cf8, #c084fc, #fb7185);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -1px;
    margin-bottom: 0;
}

.dashboard-subtitle {
    font-size: 0.9rem;
    color: #6b7280;
    font-weight: 400;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-top: 2px;
}

/* Section headers */
.section-header {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    font-weight: 700;
    color: #818cf8;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    border-bottom: 1px solid rgba(129, 140, 248, 0.2);
    padding-bottom: 8px;
    margin-bottom: 16px;
}

/* Quadrant cards */
.quadrant-card {
    background: rgba(255, 255, 255, 0.03);
    border-radius: 12px;
    padding: 20px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    height: 100%;
    transition: border-color 0.3s;
}

.quadrant-card:hover {
    border-color: rgba(129, 140, 248, 0.4);
}

.quadrant-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    margin-bottom: 4px;
}

.quadrant-emoji {
    font-size: 1.6rem;
    margin-bottom: 8px;
    display: block;
}

.student-chip {
    display: inline-block;
    background: rgba(129, 140, 248, 0.15);
    border: 1px solid rgba(129, 140, 248, 0.3);
    border-radius: 999px;
    padding: 3px 10px;
    font-size: 0.72rem;
    color: #a5b4fc;
    margin: 2px 2px 2px 0;
    font-family: 'DM Sans', sans-serif;
}

.anomaly-badge {
    background: rgba(251, 113, 133, 0.15);
    border: 1px solid rgba(251, 113, 133, 0.4);
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 0.78rem;
    color: #fb7185;
    margin: 4px 0;
}

.risk-high { border-left: 3px solid #fb7185; }
.risk-medium { border-left: 3px solid #fbbf24; }
.risk-low { border-left: 3px solid #34d399; }

/* Metric override */
[data-testid="stMetricValue"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 1.8rem !important;
    color: #e0e7ff !important;
}

[data-testid="stMetricLabel"] {
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #6b7280 !important;
}

/* Divider */
hr { border-color: rgba(255,255,255,0.06) !important; }

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    border: none !important;
    color: white !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.5rem 1rem !important;
    width: 100%;
    transition: opacity 0.2s !important;
}

.stButton > button:hover {
    opacity: 0.85 !important;
}

/* Data editor */
[data-testid="stDataEditor"] {
    border-radius: 10px;
    overflow: hidden;
}

/* Sidebar labels */
[data-testid="stSidebar"] label {
    color: #9ca3af !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# HELPER FUNCTIONS
# ──────────────────────────────────────────────

def generate_sample_data():
    """Generate 20 diverse student profiles."""
    np.random.seed(42)
    profiles = {
        "Name": [
            # High Performers (4)
            "Aisha Khan", "Rohan Mehta", "Priya Nair", "Arjun Sharma",
            # At-Risk (5)
            "Dev Patel", "Sneha Iyer", "Kiran Rao", "Ananya Singh", "Rahul Gupta",
            # Improving / Climbers (4)
            "Meera Joshi", "Aarav Kumar", "Zara Ahmed", "Vikram Das",
            # Sudden Dip (3)
            "Nisha Reddy", "Siddharth Bose", "Lakshmi Nair",
            # Anomaly cases (4)
            "Omar Sheikh", "Pooja Verma", "Ravi Teja", "Ishaan Malik",
        ],
        "Attendance (%)": [
            95, 92, 88, 91,          # High performers
            55, 48, 60, 52, 45,      # At-risk
            70, 68, 72, 65,          # Improving
            89, 91, 85,              # Sudden dip
            80, 75, 50, 88,          # Anomaly
        ],
        "Avg Score (%)": [
            88, 85, 82, 90,          # High performers
            42, 38, 50, 45, 35,      # At-risk
            48, 52, 45, 55,          # Improving
            84, 80, 78,              # Sudden dip
            78, 72, 65, 76,          # Anomaly
        ],
        "Quiz Score (%)": [
            91, 87, 85, 93,          # High performers
            40, 35, 48, 42, 33,      # At-risk
            75, 78, 70, 72,          # Improving – high quiz
            55, 48, 52,              # Sudden dip – low quiz vs high avg
            45, 48, 38, 41,          # Anomaly – big dip from avg
        ],
    }
    return pd.DataFrame(profiles)


def compute_metrics(df, wa, ws, wq):
    """Compute risk scores, deltas, and categories."""
    df = df.copy()
    df["Risk Score"] = (
        (100 - df["Attendance (%)"]) * wa +
        (100 - df["Avg Score (%)"]) * ws +
        (100 - df["Quiz Score (%)"]) * wq
    )
    df["Delta (Quiz - Avg)"] = df["Quiz Score (%)"] - df["Avg Score (%)"]
    df["Anomaly"] = df["Delta (Quiz - Avg)"] < -15

    mean_avg   = df["Avg Score (%)"].mean()
    mean_quiz  = df["Quiz Score (%)"].mean()

    def categorize(row):
        high_avg  = row["Avg Score (%)"]  >= mean_avg
        high_quiz = row["Quiz Score (%)"] >= mean_quiz
        if   high_avg  and high_quiz: return "High Flyers"
        elif high_avg  and not high_quiz: return "Sudden Dip"
        elif not high_avg and high_quiz: return "The Climbers"
        else: return "Critical Support"

    df["Category"] = df.apply(categorize, axis=1)

    def recommendation(row):
        c = row["Category"]
        if c == "High Flyers":     return "Provide advanced extension material."
        if c == "Sudden Dip":      return "Investigate external factors or specific topic gaps."
        if c == "The Climbers":    return "Acknowledge recent improvement; maintain momentum."
        return "Mandatory foundational workshop required."

    df["Recommendation"] = df.apply(recommendation, axis=1)

    risk_max = df["Risk Score"].max()
    risk_min = df["Risk Score"].min()
    if risk_max != risk_min:
        df["Risk Level"] = pd.cut(
            df["Risk Score"],
            bins=[risk_min - 0.01, risk_min + (risk_max - risk_min) * 0.33,
                  risk_min + (risk_max - risk_min) * 0.66, risk_max + 0.01],
            labels=["Low", "Medium", "High"]
        )
    else:
        df["Risk Level"] = "Low"

    return df, mean_avg, mean_quiz


# ──────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎓 Dashboard Config")
    subject_name = st.text_input("Subject Name", value="Advanced Mathematics")

    st.markdown("---")
    st.markdown("**⚖️ Risk Weight Customization**")
    st.caption("Weights are auto-normalized to sum to 1.")

    w_attendance = st.slider("Attendance Weight",   0.0, 1.0, 0.30, 0.05)
    w_score      = st.slider("Avg Score Weight",    0.0, 1.0, 0.40, 0.05)
    w_quiz       = st.slider("Quiz Score Weight",   0.0, 1.0, 0.30, 0.05)

    total_w = w_attendance + w_score + w_quiz
    if total_w == 0:
        wa = ws = wq = 1/3
    else:
        wa = w_attendance / total_w
        ws = w_score      / total_w
        wq = w_quiz       / total_w

    st.markdown(
        f"<small style='color:#6b7280'>Normalized → Att: **{wa:.2f}** | Score: **{ws:.2f}** | Quiz: **{wq:.2f}**</small>",
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown("**📊 Risk Threshold**")
    benchmark = st.slider("Benchmark (%)", 50, 90, 70, 5)

    st.markdown("---")
    demo_clicked = st.button("⚡ Generate Sample Class")


# ──────────────────────────────────────────────
# SESSION STATE – data grid
# ──────────────────────────────────────────────
if "grid_data" not in st.session_state:
    st.session_state.grid_data = pd.DataFrame(
        {"Name": [""] * 20,
         "Attendance (%)": [0] * 20,
         "Avg Score (%)":  [0] * 20,
         "Quiz Score (%)": [0] * 20}
    )

if demo_clicked:
    st.session_state.grid_data = generate_sample_data()


# ──────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────
col_title, col_info = st.columns([3, 1])
with col_title:
    st.markdown(f'<div class="dashboard-title">Student Analytics</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="dashboard-subtitle">{subject_name} · Intelligence Engine v2</div>', unsafe_allow_html=True)
with col_info:
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 Use sidebar to tune risk weights & benchmark.", icon=None)

st.markdown("---")


# ──────────────────────────────────────────────
# DATA ENTRY
# ──────────────────────────────────────────────
st.markdown('<p class="section-header">01 · Student Data Input</p>', unsafe_allow_html=True)

edited_df = st.data_editor(
    st.session_state.grid_data,
    use_container_width=True,
    num_rows="fixed",
    column_config={
        "Name":            st.column_config.TextColumn("👤 Name",           width="medium"),
        "Attendance (%)":  st.column_config.NumberColumn("📅 Attendance %",  min_value=0,  max_value=100, step=1, format="%d%%"),
        "Avg Score (%)":   st.column_config.NumberColumn("📝 Avg Score %",   min_value=0,  max_value=100, step=1, format="%d%%"),
        "Quiz Score (%)":  st.column_config.NumberColumn("⚡ Quiz Score %",  min_value=0,  max_value=100, step=1, format="%d%%"),
    },
    hide_index=True,
    key="editor",
)
st.session_state.grid_data = edited_df


# ──────────────────────────────────────────────
# PROCESS — filter valid rows
# ──────────────────────────────────────────────
valid_df = edited_df[edited_df["Name"].str.strip() != ""].copy()

if len(valid_df) < 2:
    st.warning("⚠️ Enter at least 2 students (or click **Generate Sample Class**) to activate the Intelligence Engine.")
    st.stop()

result_df, mean_avg, mean_quiz = compute_metrics(valid_df, wa, ws, wq)


# ──────────────────────────────────────────────
# KPI TILES
# ──────────────────────────────────────────────
st.markdown("---")
st.markdown('<p class="section-header">02 · Class KPIs</p>', unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5)
class_avg_att   = result_df["Attendance (%)"].mean()
class_avg_score = result_df["Avg Score (%)"].mean()
class_avg_quiz  = result_df["Quiz Score (%)"].mean()
anomaly_count   = result_df["Anomaly"].sum()
high_risk_count = (result_df["Risk Level"] == "High").sum()

with k1:
    st.metric("📅 Avg Attendance", f"{class_avg_att:.1f}%",
              delta=f"{class_avg_att - benchmark:+.1f}% vs {benchmark}%")
with k2:
    st.metric("📝 Avg Score", f"{class_avg_score:.1f}%",
              delta=f"{class_avg_score - benchmark:+.1f}% vs {benchmark}%")
with k3:
    st.metric("⚡ Avg Quiz Score", f"{class_avg_quiz:.1f}%",
              delta=f"{class_avg_quiz - benchmark:+.1f}% vs {benchmark}%")
with k4:
    st.metric("🚨 Academic Anomalies", int(anomaly_count),
              delta=f"{'⚠ Detected' if anomaly_count > 0 else 'None'}", delta_color="inverse")
with k5:
    st.metric("🔴 High Risk Students", int(high_risk_count),
              delta=f"of {len(result_df)} total", delta_color="inverse")


# ──────────────────────────────────────────────
# VISUAL RISK MAP
# ──────────────────────────────────────────────
st.markdown("---")
st.markdown('<p class="section-header">03 · Visual Risk Map</p>', unsafe_allow_html=True)

chart_col, legend_col = st.columns([3, 1])

with chart_col:
    chart_data = result_df[["Name", "Attendance (%)", "Quiz Score (%)", "Risk Score", "Category"]].copy()
    chart_data = chart_data.rename(columns={
        "Attendance (%)": "Attendance",
        "Quiz Score (%)": "Quiz Score",
    })
    st.scatter_chart(
        chart_data,
        x="Attendance",
        y="Quiz Score",
        color="Category",
        size="Risk Score",
        use_container_width=True,
        height=360,
    )
    st.caption("Bubble size = Risk Score. X-axis = Attendance, Y-axis = Quiz Score.")

with legend_col:
    st.markdown("<br>", unsafe_allow_html=True)
    cat_counts = result_df["Category"].value_counts()
    for cat, emoji, color in [
        ("High Flyers",     "🚀", "#34d399"),
        ("Sudden Dip",      "📉", "#fbbf24"),
        ("The Climbers",    "📈", "#818cf8"),
        ("Critical Support","🆘", "#fb7185"),
    ]:
        count = cat_counts.get(cat, 0)
        st.markdown(
            f"<div style='margin:6px 0;padding:10px;background:rgba(255,255,255,0.04);"
            f"border-radius:8px;border-left:3px solid {color}'>"
            f"<span style='font-size:1.1rem'>{emoji}</span> "
            f"<span style='font-size:0.82rem;color:#e0e7ff;font-weight:600'>{cat}</span><br>"
            f"<span style='font-size:0.75rem;color:#6b7280'>{count} student{'s' if count!=1 else ''}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )


# Risk bar chart
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("**Risk Score Distribution** (higher = more at risk)")
bar_data = result_df[["Name", "Risk Score"]].set_index("Name").sort_values("Risk Score", ascending=False)
st.bar_chart(bar_data, height=220, use_container_width=True)


# ──────────────────────────────────────────────
# LOGIC MATRIX — 4 QUADRANTS
# ──────────────────────────────────────────────
st.markdown("---")
st.markdown('<p class="section-header">04 · Intelligence Matrix · Student Categorization</p>', unsafe_allow_html=True)

q1, q2, q3, q4 = st.columns(4)

QUADRANTS = [
    ("High Flyers",     "🚀", "#34d399",
     "Provide advanced extension material.",
     "High Avg + High Quiz", q1),
    ("Sudden Dip",      "📉", "#fbbf24",
     "Investigate external factors or specific topic gaps.",
     "High Avg + Low Quiz", q2),
    ("The Climbers",    "📈", "#818cf8",
     "Acknowledge recent improvement; maintain momentum.",
     "Low Avg + High Quiz", q3),
    ("Critical Support","🆘", "#fb7185",
     "Mandatory foundational workshop required.",
     "Low Avg + Low Quiz", q4),
]

for cat, emoji, color, rec, tag, col in QUADRANTS:
    students = result_df[result_df["Category"] == cat]["Name"].tolist()
    with col:
        chips_html = "".join(
            f"<span class='student-chip'>{s}</span>" for s in students
        ) if students else "<span style='color:#4b5563;font-size:0.78rem'>No students</span>"

        anomalies_in_cat = result_df[
            (result_df["Category"] == cat) & (result_df["Anomaly"])
        ]["Name"].tolist()
        anomaly_html = "".join(
            f"<div class='anomaly-badge'>⚠ {s} — Academic Anomaly</div>"
            for s in anomalies_in_cat
        )

        st.markdown(
            f"""<div class='quadrant-card' style='border-top:3px solid {color}'>
                <span class='quadrant-emoji'>{emoji}</span>
                <div class='quadrant-title' style='color:{color}'>{cat}</div>
                <div style='font-size:0.7rem;color:#6b7280;margin-bottom:10px'>{tag}</div>
                <div style='font-size:0.78rem;color:#9ca3af;margin-bottom:12px;
                     background:rgba(255,255,255,0.04);padding:8px;border-radius:6px'>
                    💬 {rec}
                </div>
                <div style='margin-bottom:8px'>{chips_html}</div>
                {anomaly_html}
            </div>""",
            unsafe_allow_html=True,
        )


# ──────────────────────────────────────────────
# ANOMALY ALERTS
# ──────────────────────────────────────────────
anomalies = result_df[result_df["Anomaly"]]
if not anomalies.empty:
    st.markdown("---")
    st.markdown('<p class="section-header">⚠ Academic Anomaly Alerts</p>', unsafe_allow_html=True)
    for _, row in anomalies.iterrows():
        st.error(
            f"**{row['Name']}** — Quiz dropped **{abs(row['Delta (Quiz - Avg)']):.1f}%** "
            f"below historical average. "
            f"(Avg: {row['Avg Score (%)']:.0f}% → Quiz: {row['Quiz Score (%)']:.0f}%) "
            f"· Category: {row['Category']}"
        )


# ──────────────────────────────────────────────
# INTERVENTION TABLE — HIGH RISK ONLY
# ──────────────────────────────────────────────
st.markdown("---")
st.markdown('<p class="section-header">05 · High-Risk Intervention Table</p>', unsafe_allow_html=True)

high_risk = result_df[result_df["Risk Level"] == "High"].sort_values("Risk Score", ascending=False)

if high_risk.empty:
    st.success("✅ No high-risk students detected under current weight configuration.")
else:
    display_cols = [
        "Name", "Attendance (%)", "Avg Score (%)", "Quiz Score (%)",
        "Delta (Quiz - Avg)", "Risk Score", "Category", "Anomaly", "Recommendation"
    ]
    intervention_table = high_risk[display_cols].copy()
    intervention_table["Risk Score"] = intervention_table["Risk Score"].round(2)
    intervention_table["Delta (Quiz - Avg)"] = intervention_table["Delta (Quiz - Avg)"].round(1)

    st.dataframe(
        intervention_table,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Name":               st.column_config.TextColumn("👤 Name"),
            "Attendance (%)":     st.column_config.NumberColumn("📅 Att%",    format="%d%%"),
            "Avg Score (%)":      st.column_config.NumberColumn("📝 Avg%",    format="%d%%"),
            "Quiz Score (%)":     st.column_config.NumberColumn("⚡ Quiz%",   format="%d%%"),
            "Delta (Quiz - Avg)": st.column_config.NumberColumn("Δ Delta",    format="%.1f%%"),
            "Risk Score":         st.column_config.ProgressColumn("🔴 Risk",  min_value=0, max_value=100),
            "Category":           st.column_config.TextColumn("Category"),
            "Anomaly":            st.column_config.CheckboxColumn("⚠ Anomaly"),
            "Recommendation":     st.column_config.TextColumn("💬 Action Required", width="large"),
        },
    )
    st.caption(f"Showing {len(high_risk)} of {len(result_df)} students flagged as High Risk.")


# ──────────────────────────────────────────────
# FULL RESULTS (EXPANDABLE)
# ──────────────────────────────────────────────
with st.expander("📋 View Full Class Report"):
    full_display = result_df[[
        "Name", "Attendance (%)", "Avg Score (%)", "Quiz Score (%)",
        "Delta (Quiz - Avg)", "Risk Score", "Risk Level", "Category", "Anomaly", "Recommendation"
    ]].copy()
    full_display["Risk Score"] = full_display["Risk Score"].round(2)
    full_display["Delta (Quiz - Avg)"] = full_display["Delta (Quiz - Avg)"].round(1)
    st.dataframe(full_display, use_container_width=True, hide_index=True)


# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────
st.markdown("---")
st.markdown(
    f"<div style='text-align:center;color:#374151;font-size:0.75rem;font-family:Space Mono,monospace'>"
    f"AI Student Analytics · {subject_name} · "
    f"Weights → Att:{wa:.2f} | Score:{ws:.2f} | Quiz:{wq:.2f} · "
    f"Benchmark: {benchmark}%"
    f"</div>",
    unsafe_allow_html=True,
)