import feedparser, datetime, requests
from flask import request, jsonify, abort
from flask.views import MethodView
from bs4 import BeautifulSoup


def iso8601_to_epoch(iso_time):
    """Converts a W3-style ISO 8601 UTC timestamp to an integer number of seconds since epoch"""
    dt = datetime.datetime.strptime(iso_time, '%Y-%m-%dT%H:%M:%SZ')
    epoch = datetime.datetime.utcfromtimestamp(0)
    return int((dt - epoch).total_seconds())

class RecentPostsView(MethodView):

	default_limit = 50
	base_url = 'http://www.kijiji.ca'

	def __init__(self):
		self.posts = []
		self.rss_url = None

	def post(self):
		params = request.get_json(force=True, silent=True) or {}
		trigger_fields = params.get('triggerFields', {})
		search_url = trigger_fields.get('search_url')
		if not search_url:
			abort(400)
		self.rss_url = self.get_rss_url(search_url)
		limit = params.get('limit', self.default_limit)
		self.get_posts(limit)
		return jsonify(data=self.posts)

	def get_rss_url(self, query_url):
		html = requests.get(query_url)
		soup = BeautifulSoup(html.text, 'html.parser')
		link_tag = soup.find_all('link', type = 'application/rss+xml')[0]
		return self.base_url + link_tag['href']

	def get_posts(self, limit):
		entries = feedparser.parse(self.rss_url).entries
		i = 0
		# Each RSS feed page contains 20 entries
		for entry in entries:
			i += 1
			if i > limit:
				break
			post = {}
			print type(entry)
			post['title'] = entry.title
			post['created_at'] = entry.updated
			post['description'] = entry.description
			post['link'] = entry.guid
			post['meta'] = {
        		"id": entry.guid,
        		"timestamp": iso8601_to_epoch(entry.date)
      		}
			self.posts.append(post)

if __name__ == "__main__":
    test = RecentPostsView()
    test.rss_url = test.get_rss_url('http://www.kijiji.ca/b-storage-parking/city-of-toronto/c39l1700273?ad=wanted&more-info=storage')
    print test.rss_url
    test.get_posts(10)
    print test.posts

