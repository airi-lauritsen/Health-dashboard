import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="🏃 Health Dashboard", layout="wide")


st.title("🏃 Health Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv("health_daily.csv")
    df["date"] = pd.to_datetime(df["date"])
    df = df[df["date"] >= "2020-11-01"]
    return df

df = load_data()


k1, k2, k3 = st.columns(3)
k1.metric("Steps",      f"{int(df['steps'].mean()):,}")
k2.metric("Active calories", f"{int(df['active_calories'].mean()):,}")
k3.metric("Resting heart rate",     f"{int(df['resting_hr'].mean()):,}")





#年でフィルターできるようにするで
# 行1: dfのdate列から年だけ取り出し→重複を消す→リストにする
years = df["date"].dt.year.unique().tolist()

# 行2: セレクトボックスを表示して、選んだ年をselected_yearに入れる
selected_year = st.sidebar.selectbox("年を選択", years, index=years.index(2020))

# 行3: dfの中からdate列の年がselected_yearと同じ行だけ取り出す
df_filtered = df[df["date"].dt.year == selected_year]


#月でフィルターできるようにするで
# 行1: dfのdate列から月だけ取り出し→重複を消す→リストにする
months = sorted(df["date"].dt.month.unique().tolist())

#indexでディフォルトを11月に（11月からデータ開始するため）
selected_month = st.sidebar.selectbox("月を選択", months, index=months.index(11))

# 行3: dfの中からdate列の年がselected_monthと同じ行だけ取り出す
df_filtered = df_filtered[df_filtered["date"].dt.month == selected_month]




col1, col2  = st.columns(2)
with col1:
    st.subheader("Daily Steps🚶")
    st.metric("Avg for this month", f"{int(df_filtered["steps"].mean())} 歩")
    fig = px.line(df_filtered, x="date", y="steps",  labels={"date": "Date", "steps": "Steps"})
    
    fig.update_traces(line_color="#FFB6C1")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Active Calories🔥")
    st.metric("Avg for this month", f"{df_filtered["active_calories"].mean():.1f} kcal")
    fig_cal = px.line(df_filtered, x="date", y="active_calories",
                      labels={"active_calories": "kcal", "date": "Date"})
    fig_cal.update_traces(line_color="#FFB6C1")
    st.plotly_chart(fig_cal, use_container_width=True)

col3, col4  = st.columns(2)
with col3:
    st.subheader("Resting heartrate 🧡")
    st.metric("Avg for this month", f"{int(df_filtered["resting_hr"].mean())} bpm")
    fig_hr = px.line(df_filtered, x="date", y="resting_hr",
                     labels={"resting_hr": "bpm", "date":"Date"})
    fig_hr.update_traces(line_color="#FFB6C1")
    st.plotly_chart(fig_hr, use_container_width=True)


with col4:
    st.subheader("Monthly Average Steps 🚶")
    month_names = {1:"1月", 2:"2月", 3:"3月", 4:"4月", 5:"5月", 6:"6月",
               7:"7月", 8:"8月", 9:"9月", 10:"10月", 11:"11月", 12:"12月"}
    
    monthly_steps = df.groupby(df['date'].dt.month)['steps'].mean().reset_index()
    monthly_steps["month"] = monthly_steps["date"].map(month_names)
    fig_st = px.bar(monthly_steps, x="month", y="steps", template="plotly_white", 
                    labels={"month":"Month", "steps":"平均歩数"}, color="steps",color_continuous_scale="RdPu")
    st.plotly_chart(fig_st, use_container_width=True)