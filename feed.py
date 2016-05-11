import feedparser, requests
from bs4 import BeautifulSoup

class RecentPosts:
	def __init__(self):
		self.posts = []
		self.base_url = 'http://www.kijiji.ca'
		self.rss_url = None

	def get_rss_url(self, query_url):
		html = requests.get(query_url)
		soup = BeautifulSoup(html.text, 'html.parser')
		link_tag = soup.find_all('link', type = 'application/rss+xml')[0]
		self.rss_url =  self.base_url + link_tag['href']

	def get_posts(self):
		entries = feedparser.parse(self.rss_url).entries
		for entry in entries:
			post = {}
			post['title'] = entry.title
			post['created_at'] = entry.updated
			post['description'] = entry.description
			post['meta'] = {
        		"id": entry.guid,
        		"timestamp": 1383597267 # TODO: timestamp properly!
      		}
			self.posts.append(post)

url = 'http://www.kijiji.ca/b-classic-cars/city-of-toronto/convertible/c122l1700273a161'
test = RecentPosts()
test.get_rss_url(url)
test.get_posts()

print test.posts
