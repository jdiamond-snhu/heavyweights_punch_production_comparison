import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Heavyweight Punch Production App", layout="wide")
st.title("🥊 Heavyweight Punch Production: Latest 14 Outings")
st.write(
    "Track total punches thrown over each fighter's **latest 14 consecutive bouts**."
    " Fight 1 represents their 14th most recent fight, while Fight 14 is their absolute latest performance."
)

# 2. Data Caching
@st.cache_data
def load_data():
    return pd.read_csv("heavyweight_data.csv")

try:
    df = load_data()

    fighter_pool = [
        "Oleksandr Usyk", "Daniel Dubois", "Anthony Joshua", "Agit Kabayel", 
        "Tyson Fury", "Fabio Wardley", "Filip Hrgović", "Moses Itauma", 
        "Frank Sánchez", "Efe Ajagba", "Murat Gassiev", "Justis Huni"
    ]
    df_pool = df[df["Fighter"].isin(fighter_pool)]

    # 3. Sidebar Filtering Logic
    st.sidebar.header("App Controls")
    selected_fighters = st.sidebar.multiselect(
        "Choose Heavyweights to Display:",
        options=sorted(df_pool["Fighter"].unique()),
        default=["Tyson Fury", "Anthony Joshua", "Oleksandr Usyk", "Moses Itauma"]
    )

    if selected_fighters:
        # Filter rows based on selection
        filtered_df = df_pool[df_pool["Fighter"].isin(selected_fighters)]

        # 4. Color Logic Setup
        # Assign Tyson Fury a strict green color; let Plotly handle the rest automatically
        custom_color_map = {}
        for fighter in selected_fighters:
            if fighter == "Tyson Fury":
                custom_color_map[fighter] = "#00FF00"  # Bright Green (or use 'green')
            else:
                custom_color_map[fighter] = None       # Plotly falls back to default theme colors

        # 5. Build Custom Plotly Line Graph
        fig = px.line(
            filtered_df,
            x="Bout_Sequence",
            y="Punches_Thrown",
            color="Fighter",
            color_discrete_map=custom_color_map,
            markers=True,  # Adds dots to data points for clarity
            labels={"Bout_Sequence": "Bout Timeline (1 to 14)", "Punches_Thrown": "Total Punches Thrown"},
            title="Relative Punch Volume Comparison Timeline"
        )
        
        # Format the X-axis grid lines to display whole integers from 1 to 14
        fig.update_layout(xaxis=dict(tickmode="linear", tick0=1, dtick=1))
        
        # Display the custom graph
        st.plotly_chart(fig, use_container_width=True)
        
        # 6. Expanded Detailed Raw Data Table
        with st.expander("📊 View Detailed Historical Match Details"):
            st.write("Below is the expanded match matrix showing opponent names and exact punch totals:")
            
            # Pivot the matrix specifically for display (showing Opponent and Punches side-by-side)
            display_df = filtered_df.sort_values(["Bout_Sequence", "Fighter"])
            
            # Display clean, scrollable dataframe with formatting
            st.dataframe(
                display_df[["Fighter", "Bout_Sequence", "Opponent", "Punches_Thrown"]], 
                use_container_width=True,
                hide_index=True
            )

    else:
        st.warning("Please select at least one active heavyweight from the sidebar menu to populate the trend lines.")

except FileNotFoundError:
    st.error("Could not locate 'heavyweight_data.csv'. Ensure the file is inside your GitHub commit.")
