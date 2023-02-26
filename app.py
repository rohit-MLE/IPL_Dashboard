import pandas as pd
# pip install pandas openpyxl
import plotly.express as px
# pip install plotly-express
import streamlit as st
import altair as alt

# pip install streamlit


st.set_page_config(page_title="Test Dashboard", page_icon=":bar_chart:", layout="wide")


# Read data from CSV file
@st.cache_data
def get_data_from_csv():
    df = pd.read_csv("ipl_2023_dataset.csv", usecols=[1, 2, 3, 4])
    return df


df = get_data_from_csv()

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
player_type = st.sidebar.multiselect(
    "Select the Player Type:",
    options=df["Type"].unique(),
    default=df["Type"].unique()
)

team = st.sidebar.multiselect(
    "Select the Team:",
    options=df["Team"].unique(),
    default=df["Team"].unique()
)

df_selection = df.query(
    "`Type` == @player_type & Team == @team"
)

# ---- MAINPAGE ----
st.title(":bar_chart: IPL Dashboard")
st.markdown("##")

# TOP KPI's
total_price = int(df_selection["Price Cr"].sum())
average_price = round(df_selection["Price Cr"].mean(), 1)

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Total Price:")
    st.subheader(f"INR {total_price:,} Cr")
with right_column:
    st.subheader("Average Price:")
    st.subheader(f"INR {average_price} Cr")

st.markdown("""---""")

# Price BY Team [BAR CHART]
price_by_team = (
    df_selection.groupby(by=["Team"]).sum()[["Price Cr"]].sort_values(by="Price Cr")
)
fig_team_price = px.bar(
    price_by_team,
    x="Price Cr",
    y=price_by_team.index,
    orientation="h",
    title="<b>Price by Teams</b>",
    color_discrete_sequence=["#0083B8"] * len(price_by_team),
    template="plotly_white",
)
fig_team_price.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# Price BY Team [PIE CHART]
fig_team_price_pie = px.pie(
    price_by_team,
    values="Price Cr",
    names=price_by_team.index,
    title="<b>Price by Teams</b>",
    color_discrete_map={team.lower().strip(): color for team, color in {
        "Royal Challengers Bangalore": "#FF0000",
        "Chennai Super Kings": "yellow",
        "Mumbai Indians": "blue",
        "Gujrat Titans": "#004C99",
        "Rajasthan Royals": "pink",
        "Lucknow Super Giants": "#33FFFF",
        "Delhi capitals": "#6666FF",
        "Sunrisers hyderabad": "orange",
        "Punjab Kings": "#FF66B2",
        "Unsold": "#331900"
    }.items()},
    template="plotly_white",
)


fig_team_price_pie.update_layout(
    plot_bgcolor="rgba(0,0,0,0)"
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_team_price, use_container_width=True)
right_column.plotly_chart(fig_team_price_pie, use_container_width=True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
