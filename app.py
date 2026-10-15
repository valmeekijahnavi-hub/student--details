import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# -------------------- Page setup --------------------
st.set_page_config(
    page_title="Student Details Dashboard",
    page_icon="🎓",
    layout="wide",
)

st.title("🎓 Student Details & Academic Performance Dashboard")
st.caption("Explore how study habits, attendance, and student background relate to exam performance.")

DATA_FILE = Path(__file__).parent / "StudentPerformanceFactors.csv"

@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    # Convert numeric-looking columns safely, while leaving category columns unchanged.
    for col in data.columns:
        if col not in data.select_dtypes(include="number").columns:
            converted = pd.to_numeric(data[col], errors="coerce")
            if converted.notna().sum() == data[col].notna().sum():
                data[col] = converted
    return data

try:
    df = load_data(DATA_FILE)
except FileNotFoundError:
    st.error(
        "Dataset not found. Keep StudentPerformanceFactors.csv in the same folder as app.py."
    )
    st.stop()
except Exception as exc:
    st.error(f"Could not read the dataset: {exc}")
    st.stop()

if "Exam_Score" not in df.columns:
    st.error("The dataset must contain an 'Exam_Score' column.")
    st.stop()

# -------------------- Sidebar filters --------------------
st.sidebar.header("🔎 Dashboard Filters")
st.sidebar.write("Every filter below updates **all KPIs and charts**.")

filtered = df.copy()

# Category filters: selections are applied to the same filtered dataset used by every chart.
category_columns = [
    "Gender",
    "School_Type",
    "Motivation_Level",
    "Parental_Involvement",
    "Access_to_Resources",
    "Internet_Access",
    "Extracurricular_Activities",
]

for col in category_columns:
    if col in filtered.columns:
        values = sorted(filtered[col].dropna().astype(str).unique().tolist())
        selected = st.sidebar.multiselect(
            col.replace("_", " "),
            options=values,
            default=values,
            key=f"filter_{col}",
        )
        if selected:
            filtered = filtered[filtered[col].astype(str).isin(selected)]
        else:
            filtered = filtered.iloc[0:0]

# Numeric range filters are also applied globally.
numeric_filter_columns = ["Attendance", "Hours_Studied", "Exam_Score"]
for col in numeric_filter_columns:
    if col in filtered.columns and pd.api.types.is_numeric_dtype(df[col]):
        low = int(df[col].min())
        high = int(df[col].max())
        if low < high:
            selected_range = st.sidebar.slider(
                col.replace("_", " "),
                min_value=low,
                max_value=high,
                value=(low, high),
                key=f"range_{col}",
            )
            filtered = filtered[filtered[col].between(selected_range[0], selected_range[1])]

def reset_filters():
    for col in category_columns:
        if col in df.columns:
            st.session_state[f"filter_{col}"] = sorted(df[col].dropna().astype(str).unique().tolist())
    for col in numeric_filter_columns:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            low = int(df[col].min())
            high = int(df[col].max())
            if low < high:
                st.session_state[f"range_{col}"] = (low, high)

st.sidebar.button("Reset all filters", on_click=reset_filters, use_container_width=True)

st.sidebar.divider()
st.sidebar.caption("Tip: choose one or more categories. To compare all students, leave every category selected.")

# -------------------- Empty-filter handling --------------------
if filtered.empty:
    st.warning("No students match these filters. Select more options in the sidebar.")
    st.stop()

# -------------------- KPI cards --------------------
total_students = len(filtered)
avg_score = filtered["Exam_Score"].mean()
median_score = filtered["Exam_Score"].median()
avg_attendance = filtered["Attendance"].mean() if "Attendance" in filtered.columns else None

k1, k2, k3, k4 = st.columns(4)
k1.metric("Students in selection", f"{total_students:,}")
k2.metric("Average exam score", f"{avg_score:.1f}")
k3.metric("Median exam score", f"{median_score:.1f}")
if avg_attendance is not None:
    k4.metric("Average attendance", f"{avg_attendance:.1f}%")
else:
    k4.metric("Average attendance", "N/A")

st.divider()

# -------------------- Charts (all use filtered data) --------------------
left, right = st.columns(2)

with left:
    st.subheader("1. Exam Score Distribution")
    fig = px.histogram(
        filtered, x="Exam_Score", nbins=20,
        title="Number of students by exam score",
        labels={"Exam_Score": "Exam score", "count": "Number of students"},
        color_discrete_sequence=["#3B82F6"],
    )
    fig.update_layout(bargap=0.08)
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("2. Study Hours vs Exam Score")
    if {"Hours_Studied", "Exam_Score"}.issubset(filtered.columns):
        color_col = "Gender" if "Gender" in filtered.columns else None
        fig = px.scatter(
            filtered, x="Hours_Studied", y="Exam_Score",
            color=color_col, opacity=0.65,
            title="Study hours compared with exam score",
            labels={"Hours_Studied": "Hours studied", "Exam_Score": "Exam score"},
            hover_data=[c for c in ["Attendance", "Previous_Scores", "Motivation_Level"] if c in filtered.columns],
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Study-hours columns are not available in this dataset.")

left2, right2 = st.columns(2)

with left2:
    st.subheader("3. Average Exam Score by Motivation")
    if "Motivation_Level" in filtered.columns:
        score_by_motivation = (
            filtered.groupby("Motivation_Level", as_index=False)["Exam_Score"]
            .mean()
            .sort_values("Exam_Score", ascending=False)
        )
        fig = px.bar(
            score_by_motivation, x="Motivation_Level", y="Exam_Score",
            title="Average exam score for each motivation level",
            labels={"Motivation_Level": "Motivation level", "Exam_Score": "Average exam score"},
            text_auto=".1f",
            color="Exam_Score",
            color_continuous_scale="Blues",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Motivation level is not available in this dataset.")

with right2:
    st.subheader("4. Attendance vs Exam Score")
    if {"Attendance", "Exam_Score"}.issubset(filtered.columns):
        fig = px.scatter(
            filtered, x="Attendance", y="Exam_Score",
            title="Attendance compared with exam score",
            labels={"Attendance": "Attendance (%)", "Exam_Score": "Exam score"},
            trendline="ols" if len(filtered) >= 2 else None,
            opacity=0.6,
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Attendance is not available in this dataset.")

st.subheader("5. Correlation Heatmap")
numeric_data = filtered.select_dtypes(include="number")
if numeric_data.shape[1] >= 2:
    corr = numeric_data.corr(numeric_only=True)
    fig = px.imshow(
        corr, text_auto=".2f", aspect="auto",
        color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
        title="Correlation between numeric variables",
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("At least two numeric columns are required for the correlation heatmap.")

with st.expander("View filtered student records"):
    st.write(f"Showing {len(filtered):,} of {len(df):,} records.")
    st.dataframe(filtered, use_container_width=True, hide_index=True)
    csv_bytes = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download filtered data as CSV",
        data=csv_bytes,
        file_name="filtered_student_details.csv",
        mime="text/csv",
    )

st.caption("Data source: StudentPerformanceFactors.csv. Charts describe associations in this dataset and do not prove cause and effect.")
