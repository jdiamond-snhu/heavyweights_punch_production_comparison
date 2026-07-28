import streamlit as st
import pandas as pd
import plotly.express as px

# 1. App Configuration
st.set_page_config(page_title="Heavyweight Punch Analytics Engine", layout="wide")
st.title("🥊 Heavyweight Punch Production Matrix")
st.write(
    "Analyze and compare historical punch records across elite heavyweight bouts. "
    "The dots on each line represent individual, completed professional fights."
st.caption("Designed by Jeff Diamond-Radecki, 2026." 
)

# 2. Cached Data Input with Column Cleaning
@st.cache_data
def load_data():
    df = pd.read_csv("heavyweight_data.csv")
    # Clean headers programmatically to strip accidental spaces
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()

    # 3. Sidebar Selection Controls
    st.sidebar.header("Data Filter Configurations")
    
    metric_options = {
        "Punches_Thrown": "Total Punches Thrown",
        "Punches_Landed": "Total Punches Landed",
        "Power_Punches_Landed": "Power Punches Landed",
        "Power_Punches_Thrown": "Power Punches Thrown"
    }
    
    selected_metric = st.sidebar.selectbox(
        "Select Graph Analysis Metric:",
        options=list(metric_options.keys()),
        format_func=lambda x: metric_options[x]
    )

    all_fighters = sorted(df["Fighter"].unique())
    
    # Pre-select the Big Three default heavyweights if they exist in the CSV pool
    preferred_defaults = ["Oleksandr Usyk", "Tyson Fury", "Anthony Joshua"]
    available_defaults = [f for f in preferred_defaults if f in all_fighters]

    selected_fighters = st.sidebar.multiselect(
        "Choose Heavyweights to Compare:",
        options=all_fighters,
        default=available_defaults if available_defaults else all_fighters[:3]
    )

    if selected_fighters:
        filtered_df = df[df["Fighter"].isin(selected_fighters)]

        # 4. Explicit Color Map (Enforces Bright Green for Tyson Fury)
        custom_color_map = {}
        for fighter in selected_fighters:
            if fighter == "Tyson Fury":
                custom_color_map[fighter] = "#00FF00"
            else:
                custom_color_map[fighter] = None

        # 5. Build Dynamic Plotly Analytics Graph with Dot Interaction
        fig = px.line(
            filtered_df,
            x="Bout_Sequence",
            y=selected_metric,
            color="Fighter",
            color_discrete_map=custom_color_map,
            markers=True,
            hover_data=["Opponent", "Punches_Thrown", "Punches_Landed"],
            labels={
                "Bout_Sequence": "Bout Scale (Earliest to Most Recent Logged)", 
                selected_metric: metric_options[selected_metric]
            },
            title=f"Timeline Analysis: {metric_options[selected_metric]}"
        )
        
        fig.update_layout(xaxis=dict(tickmode="linear", tick0=1, dtick=1))
        st.plotly_chart(fig, use_container_width=True)
        
        # 6. Comprehensive Multi-Column Raw Data Viewer
        with st.expander("📊 View Detailed Historical Match Details"):
            st.write("Complete data grid including punches thrown, landed, and power-punch metrics:")
            
            display_df = filtered_df.sort_values(["Fighter", "Bout_Sequence"])
            
            readable_df = display_df[[
                "Fighter", "Bout_Sequence", "Opponent", 
                "Punches_Thrown", "Punches_Landed", 
                "Power_Punches_Landed", "Power_Punches_Thrown"
            ]].rename(columns={
                "Bout_Sequence": "Bout #",
                "Punches_Thrown": "Thrown",
                "Punches_Landed": "Landed",
                "Power_Punches_Landed": "Power Landed",
                "Power_Punches_Thrown": "Power Thrown"
            })
            
            st.dataframe(readable_df, use_container_width=True, hide_index=True)

    else:
        st.warning("Please select at least one active heavyweight from the sidebar menu to populate the trend lines.")

except FileNotFoundError:
    st.error("Could not locate 'heavyweight_data.csv'. Ensure the file is inside your GitHub commit.")
