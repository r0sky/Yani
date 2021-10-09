from newspaper import Article


def get_news_text(news_url: str):
  """
  scrapes website and returns the content
  Args:
    news_url: url to be scraped
  Returns:
    content in the related page
  """
  print("Getting Article Content..")
  if news_url is None:
    print("URL is missing")
    return None
  else:
    article = Article(news_url)
    article.download()
    article.parse()
    return article.text
