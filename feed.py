import feedparser, datetime
from flask import request, jsonify, abort
from flask.views import MethodView


def iso8601_to_epoch(iso_time):
    """Converts a W3-style ISO 8601 UTC timestamp to an integer number of seconds since epoch"""
    dt = datetime.datetime.strptime(iso_time, '%Y-%m-%dT%H:%M:%SZ')
    epoch = datetime.datetime.utcfromtimestamp(0)
    return int((dt - epoch).total_seconds())

class RecentPostsView(MethodView):

	default_limit = 50

	def __init__(self):
		self.posts = []
		self.rss_url = None

	def post(self):
		params = request.get_json(force=True, silent=True) or {}
		trigger_fields = params.get('triggerFields', {})
		self.rss_url = trigger_fields.get('search_url')
		if not self.rss_url:
			abort(400)
		limit = params.get('limit', self.default_limit)
		self.get_posts(limit)
		return jsonify(data=self.posts)

	def get_posts(self, limit):
		entries = feedparser.parse(self.rss_url).entries
		i = 0
		for entry in entries:
			i += 1
			if i > limit:
				break
			post = {}
			print type(entry)
			post['title'] = entry.title
			post['created_at'] = entry.updated
			post['description'] = entry.description
			post['meta'] = {
        		"id": entry.guid,
        		"timestamp": iso8601_to_epoch(entry.date)
      		}
			self.posts.append(post)

# if __name__ == "__main__":
#     test = RecentPostsView()
#     test.rss_url = 'http://www.kijiji.ca/rss-srp-classic-cars/city-of-toronto/convertible/c122l1700273a161'
#     test.get_posts(10)
#     print test.posts

