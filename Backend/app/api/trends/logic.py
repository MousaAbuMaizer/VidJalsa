from pytrends.request import TrendReq

async def get_trending_topics():
    pytrends = TrendReq(hl='en-US', tz=360)
    trending = pytrends.trending_searches(pn='united_states')
    topics = trending[0].head(8).tolist()
    return topics
