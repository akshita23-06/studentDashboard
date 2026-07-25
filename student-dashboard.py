import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

# ------------------ Custom CSS ------------------
st.markdown("""
<style>
.main{
    background-color:#F5F7FA;
}
h1{
    color:#003366;
    text-align:center;
}
.stButton>button{
    background-color:#003366;
    color:white;
    border-radius:8px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ Title ------------------
st.title("🎓 Student Performance Analytics Dashboard")
st.write("Analyze student performance using interactive filters and visualizations.")

# ------------------ Load Dataset ------------------
df = pd.read_csv("student_performance.csv")

# ------------------ Sidebar Filters ------------------
st.sidebar.header("Filters")

department = st.sidebar.multiselect(
    "Department",
    df["Department"].unique(),
    default=df["Department"].unique()
)

semester = st.sidebar.multiselect(
    "Semester",
    sorted(df["Semester"].unique()),
    default=sorted(df["Semester"].unique())
)

attendance = st.sidebar.slider(
    "Attendance Range",
    int(df["Attendance"].min()),
    int(df["Attendance"].max()),
    (
        int(df["Attendance"].min()),
        int(df["Attendance"].max())
    )
)

filtered_df = df[
    (df["Department"].isin(department)) &
    (df["Semester"].isin(semester)) &
    (df["Attendance"] >= attendance[0]) &
    (df["Attendance"] <= attendance[1])
]

# ------------------ Display Data ------------------
st.subheader("Filtered Student Data")
st.dataframe(filtered_df, use_container_width=True)

# ------------------ Download CSV ------------------
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Filtered Data",
    csv,
    "filtered_students.csv",
    "text/csv"
)

# ------------------ Summary ------------------
st.subheader("Summary Statistics")
st.write(filtered_df.describe())

# ------------------ Charts ------------------

# Average Marks by Department
st.subheader("Average Marks by Department")

avg_marks = filtered_df.groupby("Department")["Marks"].mean()

fig1, ax1 = plt.subplots()
ax1.bar(avg_marks.index, avg_marks.values)
ax1.set_ylabel("Average Marks")
st.pyplot(fig1)

# Semester Distribution
st.subheader("Semester Distribution")

fig2, ax2 = plt.subplots()
filtered_df["Semester"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%",
    ax=ax2
)
ax2.set_ylabel("")
st.pyplot(fig2)

# Histogram
st.subheader("Marks Distribution")

fig3, ax3 = plt.subplots()
ax3.hist(filtered_df["Marks"], bins=10)
ax3.set_xlabel("Marks")
ax3.set_ylabel("Students")
st.pyplot(fig3)

# Scatter Plot
st.subheader("Attendance vs Marks")

fig4, ax4 = plt.subplots()
ax4.scatter(filtered_df["Attendance"], filtered_df["Marks"])
ax4.set_xlabel("Attendance")
ax4.set_ylabel("Marks")
st.pyplot(fig4)

st.success("Dashboard Loaded Successfully!")