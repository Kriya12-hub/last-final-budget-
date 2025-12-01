import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------ PAGE CONFIG ------------------ #
st.set_page_config(
    page_title="Budget Analysis Dashboard",
    layout="wide",
    page_icon="📊"
)

# ------------------ STYLES ------------------ #
st.markdown("""
<style>
    .main { background-color: #F3F4F6; }
    .title { color: #1E3A8A; font-size: 36px; font-weight: 700; }
    .header { color: #1E40AF; font-size: 24px; margin-top: 20px; }
    .subheader { color: #1E3A8A; font-size: 18px; }
</style>
""", unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------ #
st.sidebar.title("📂 Navigation")
section = st.sidebar.radio(
    "Go to:",
    ["Home", "Data Overview", "Analysis", "Graphs"]
)

uploaded_file = st.sidebar.file_uploader("Upload Budget CSV", type=["csv"])


# ------------------ LOAD DATA ------------------ #
df = None
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
    except:
        st.error("❌ Could not read CSV. Please upload a valid file.")
        df = None


# ------------------ HOME ------------------ #
if section == "Home":
    st.markdown("<div class='title'>📊 Budget Analysis Dashboard</div>", unsafe_allow_html=True)
    st.write("""
    Welcome to the Budget Analysis Dashboard.

    **Upload a CSV file** from the sidebar to start.
    
    ### Dashboard Features
    - Data preview  
    - Summary statistics  
    - Department-level analysis  
    - Yearly comparisons  
    - Bar & line charts  
    """)


# ------------------ DATA OVERVIEW ------------------ #
elif section == "Data Overview":
    st.markdown("<div class='header'>📁 Dataset Overview</div>", unsafe_allow_html=True)

    if df is None:
        st.warning("⚠️ Please upload a CSV file.")
    else:
        st.subheader("Preview")
        st.dataframe(df.head(), use_container_width=True)

        st.subheader("Statistics")
        st.write(df.describe())


# ------------------ ANALYSIS ------------------ #
elif section == "Analysis":
    st.markdown("<div class='header'>📌 Data Analysis</div>", unsafe_allow_html=True)

    if df is None:
        st.warning("⚠️ Upload a CSV file to continue.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            dept = st.selectbox("Select Department", df["Department"].unique())
        with col2:
            mode = st.selectbox("Analysis Type", ["Year-wise Budget", "Compare Two Years"])

        years = df.columns[1:]  # all year columns
        row = df[df["Department"] == dept].iloc[0]

        if mode == "Year-wise Budget":
            st.subheader(f"Budget for {dept}")
            st.write(row)

        else:
            col3, col4 = st.columns(2)
            with col3:
                year1 = st.selectbox("First Year", years)
            with col4:
                year2 = st.selectbox("Second Year", years)

            v1 = float(row[year1])
            v2 = float(row[year2])

            st.metric(label=f"{dept} ({year2})", value=v2, delta=v2 - v1)


# ------------------ GRAPHS ------------------ #
elif section == "Graphs":
    st.markdown("<div class='header'>📈 Visualisations</div>", unsafe_allow_html=True)

    if df is None:
        st.warning("⚠️ Upload a CSV file to generate charts.")
    else:
        dept = st.selectbox("Select Department", df["Department"].unique())
        years = df.columns[1:]
        row = df[df["Department"] == dept].iloc[0]

        # BAR CHART
        st.markdown("<div class='subheader'>Bar Chart</div>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.bar(years, row[1:].astype(float))
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # LINE CHART
        st.markdown("<div class='subheader'>Line Chart</div>", unsafe_allow_html=True)
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        ax2.plot(years, row[1:].astype(float), marker="o")
        plt.xticks(rotation=45)
        st.pyplot(fig2)

        st.info(f"""
        **Highest Budget:** {years[row[1:].values.argmax()]}  
        **Lowest Budget:**  {years[row[1:].values.argmin()]}  
        **Total Budget:**   {row[1:].sum():,.2f} crores  
        """)
