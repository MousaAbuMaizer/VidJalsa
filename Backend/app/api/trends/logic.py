from pytrends.request import TrendReq

async def get_trending_topics():
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        trending = pytrends.trending_searches(pn='united_states')
        topics = trending[0].head(8).tolist()
        return topics
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
