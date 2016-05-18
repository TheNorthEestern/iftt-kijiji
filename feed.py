import feedparser
from flask import request, jsonify, abort
from flask.views import MethodView

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
			post['title'] = entry.title
			post['created_at'] = entry.updated
			post['description'] = entry.description
			post['meta'] = {
        		"id": entry.guid,
        		"timestamp": 1383597267 # TODO: timestamp properly!
      		}
			self.posts.append(post)

