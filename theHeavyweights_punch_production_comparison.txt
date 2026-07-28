import streamlit as st
import pandas as pd

# 1. Page & Layout Configuration
st.set_page_config(page_title="Heavyweight Punch Production App", layout="wide")
st.title("🥊 Heavyweight Punch Production: Latest 14 Outings")
st.write(
    "This graph tracks total punches thrown over each fighter's **latest 14 consecutive bouts**."
    " Fight 1 represents their 14th most recent fight, while Fight 14 is their absolute latest performance."
)

# 2. Data Caching for Speed
@st.cache_data
def load_data():
    # Looks for your CSV file in the same GitHub repository folder
    df = pd.read_csv("heavyweight_data.csv")
    return df

try:
    df = load_data()

    # The 12 active heavyweights specified
    fighter_pool = [
        "Oleksandr Usyk", "Daniel Dubois", "Anthony Joshua", "Agit Kabayel", 
        "Tyson Fury", "Fabio Wardley", "Filip Hrgović", "Moses Itauma", 
        "Frank Sánchez", "Efe Ajagba", "Murat Gassiev", "Justis Huni"
    ]

    # Clean the dataset to ensure it only tracks our target list
    df_pool = df[df["Fighter"].isin(fighter_pool)]

    # 3. Interactive Multi-Select Sidebar
    st.sidebar.header("App Controls")
    selected_fighters = st.sidebar.multiselect(
        "Choose Heavyweights to Display:",
        options=sorted(df_pool["Fighter"].unique()),
        default=["Tyson Fury", "Anthony Joshua", "Oleksandr Usyk", "Moses Itauma"] # High contrast default view
    )

    if selected_fighters:
        # Filter rows based on sidebar selection
        filtered_df = df_pool[df_pool["Fighter"].isin(selected_fighters)]

        # 4. Pivot Table for Streamlit Charting Engine
        # X-Axis = Bout_Sequence (1 to 14), Line Keys = Fighter, Values = Punches_Thrown
        chart_data = filtered_df.pivot(
            index="Bout_Sequence", 
            columns="Fighter", 
            values="Punches_Thrown"
        )

        # Force the index to maintain a strict sequence from 1 up to 14
        chart_data = chart_data.reindex(range(1, 15))

        # 5. Build and Display Interactive Graph
        st.subheader("Relative Punch Volume Comparison Timeline")
        st.line_chart(chart_data)
        
        # 6. Data Transparency Inspector
        with st.expander("📊 Click to inspect raw matrix data"):
            st.dataframe(chart_data, use_container_width=True)

    else:
        st.warning("Please select at least one active heavyweight from the sidebar menu to populate the trend lines.")

except FileNotFoundError:
    st.error("Could not locate 'heavyweight_data.csv'. Ensure the filename matches perfectly in your GitHub commit.")
