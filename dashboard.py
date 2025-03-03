# dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
from scrape_news import scrape_real_estate_news
from sentiment_analysis import analyze_sentiment, explain_sentiment_vader

# Set page configuration (title, icon, layout)
st.set_page_config(
    page_title="Real Estate Sentiment Dashboard",
    page_icon="🏠",
    layout="wide",
)

# Custom CSS for styling
custom_css = """
<style>
/* Background and font colors */
body {
    background-color: #f5f5f5;
    color: #333;
}

/* Style the header */
h1 {
    color: #2c3e50;
    text-align: center;
}

/* Style for expander headers */
.streamlit-expanderHeader {
    font-size: 1.1rem;
    font-weight: bold;
    color: #2c3e50;
}

/* Custom table styling */
.css-1d391kg {
    background-color: #ffffff;
    border: 1px solid #ddd;
    border-radius: 5px;
}

/* Style for clickable links */
a {
    color: #2980b9;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.title("🏠 Real Estate Market Sentiment Analysis Dashboard")

# Use columns for layout
col1, col2 = st.columns(2)
with col1:
    st.header("News Articles")
with col2:
    st.header("Sentiment Charts")

# Fetch articles
st.write("Fetching news articles...")
articles = scrape_real_estate_news(limit=15)

if not articles:
    st.error("No articles found. Please check the scraping module or try again later.")
else:
    st.success(f"Found {len(articles)} articles.")

# Process articles and compute sentiment
results = []
for art in articles:
    text = art["headline"] + ". " + art["snippet"]
    sentiment = analyze_sentiment(text)
    explanation = explain_sentiment_vader(text)
    art["sentiment_label"] = sentiment["label"]
    art["sentiment_score"] = sentiment["score"]
    art["explanation"] = explanation
    results.append(art)

df = pd.DataFrame(results)

# Left Column: Data Table
with col1:
    st.write("### Articles Overview")
    st.dataframe(df[['headline', 'date', 'sentiment_label', 'sentiment_score']])
    
    st.write("### Detailed Analysis")
    for idx, row in df.iterrows():
        with st.expander(f"{row['headline']}"):
            st.markdown(f"**Headline:** {row['headline']}")
            st.markdown(f"**Publication Date:** {row.get('date', 'N/A')}")
            st.markdown(f"**Snippet:** {row['snippet']}")
            st.markdown(f"**Sentiment:** {row['sentiment_label']} (Score: {row['sentiment_score']:.2f})")
            st.markdown(f"**Explanation:** {row['explanation']}")
            if row.get("url"):
                st.markdown(f"[Read Full Article]({row['url']})", unsafe_allow_html=True)

# Right Column: Charts
with col2:
    if "sentiment_label" in df.columns:
        sentiment_counts = df["sentiment_label"].value_counts().reset_index()
        sentiment_counts.columns = ["Sentiment", "Count"]
        
        st.write("#### Sentiment Distribution (Bar Chart)")
        bar_fig = px.bar(
            sentiment_counts, 
            x="Sentiment", 
            y="Count", 
            title="Sentiment Distribution",
            color="Sentiment",
            color_discrete_map={"Positive": "#27ae60", "Neutral": "#f1c40f", "Negative": "#e74c3c"}
        )
        st.plotly_chart(bar_fig, use_container_width=True)
        
        st.write("#### Sentiment Distribution (Pie Chart)")
        pie_fig = px.pie(
            sentiment_counts, 
            names="Sentiment", 
            values="Count", 
            title="Sentiment Proportions",
            color="Sentiment",
            color_discrete_map={"Positive": "#27ae60", "Neutral": "#f1c40f", "Negative": "#e74c3c"}
        )
        st.plotly_chart(pie_fig, use_container_width=True)
    else:
        st.write("No sentiment data available to display charts.")

# st.write("### About This Dashboard")
# st.markdown("""
# This dashboard was created to provide a clear overview of current real estate market sentiment by analyzing news articles.  
# It uses a high-quality pre-trained sentiment model and leverages an explanation module based on VADER’s lexicon to offer transparency on how sentiment is derived.
# """)