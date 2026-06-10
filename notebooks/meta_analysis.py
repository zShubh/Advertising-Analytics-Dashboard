import streamlit as st
import pandas as pd

# ── Page config — must be first streamlit command ─────────────────────────────
st.set_page_config(
    page_title = "Ad Performance Dashboard",
    page_icon  = "📊",
    layout     = "wide"   # use full screen width
)

# ── Load data — cache so it doesn't reload every time ────────────────────────
@st.cache_data   # this decorator saves the data in memory
def load_data():
    df         = pd.read_csv('merged_ad_data.csv')
    ad_metrics = pd.read_csv('ad_metrics_clustered.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df, ad_metrics

df, ad_metrics = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/fluency/96/graph.png", width=80)
st.sidebar.title("Ad Analysis")
st.sidebar.markdown("---")
st.sidebar.markdown("### Navigation")
st.sidebar.markdown("Use the pages above to explore:")
st.sidebar.markdown("- 📊 Ad Performance")
st.sidebar.markdown("- 📈 Campaign Analysis")
st.sidebar.markdown("- 🎯 Cluster Results")
st.sidebar.markdown("- ⏰ Time Patterns")

# ── Home page ─────────────────────────────────────────────────────────────────
st.title("📊 Ad Performance Dashboard")
st.markdown("Complete analysis of 400,000 ad events across 200 ads and 50 campaigns.")
st.markdown("---")

# ── KPI cards row ─────────────────────────────────────────────────────────────
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label = "Total Events",
        value = f"{len(df):,}"
    )
with col2:
    st.metric(
        label = "Total Ads",
        value = f"{df['ad_id'].nunique()}"
    )
with col3:
    st.metric(
        label = "Total Campaigns",
        value = f"{df['campaign_id'].nunique()}"
    )
with col4:
    ctr = df['is_click'].mean() * 100
    st.metric(
        label = "Avg Click Rate",
        value = f"{ctr:.2f}%"
    )
with col5:
    pvr = df['is_purchase'].mean() * 100
    st.metric(
        label = "Avg Purchase Rate",
        value = f"{pvr:.2f}%"
    )

st.markdown("---")

# ── Quick overview charts ─────────────────────────────────────────────────────
import plotly.express as px

col1, col2 = st.columns(2)

with col1:
    st.subheader("Event Type Distribution")
    event_counts = df['event_type'].value_counts().reset_index()
    event_counts.columns = ['event_type', 'count']
    fig = px.pie(
        event_counts,
        values = 'count',
        names  = 'event_type',
        color_discrete_sequence = px.colors.qualitative.Set2
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Events by Platform")
    # Reconstruct platform from one-hot columns
    df['ad_platform'] = 'Facebook'
    df.loc[df['platform_Instagram'] == 1, 'ad_platform'] = 'Instagram'

    platform_counts = df['ad_platform'].value_counts().reset_index()
    platform_counts.columns = ['platform', 'count']
    fig2 = px.bar(
        platform_counts,
        x     = 'platform',
        y     = 'count',
        color = 'platform',
        color_discrete_sequence = ['#4267B2', '#C13584']
    )
    st.plotly_chart(fig2, use_container_width=True)

# ── Data preview ──────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("Raw Data Preview")

# Let user filter by event type
event_filter = st.multiselect(
    "Filter by Event Type",
    options = df['event_type'].unique().tolist(),
    default = df['event_type'].unique().tolist()
)

filtered_df = df[df['event_type'].isin(event_filter)]
st.dataframe(
    filtered_df[['event_id', 'ad_id', 'user_id', 'timestamp',
                  'event_type', 'time_of_day', 'day_of_week']].head(100),
    use_container_width=True
)
st.caption(f"Showing 100 of {len(filtered_df):,} filtered rows")