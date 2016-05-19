from flask import Flask, request, abort, jsonify
from feed import RecentPostsView
app = Flask(__name__)

app.debug = True
app.config['JSON_AS_ASCII'] = False

@app.errorhandler(401)
def unauthorized(e):
    error = {'message' :'Unauthorized'}
    return jsonify(errors=[error]), 401

@app.errorhandler(400)
def unauthorized(e):
    error = {'message' :'Missing required trigger field'}
    return jsonify(errors=[error]), 400

@app.after_request
def force_content_type(response):
    """RFC 4627 stipulates that 'application/json' takes no charset parameter,
    but IFTTT expects one anyway. We have to twist Flask's arm to get it to
    break the spec."""
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@app.before_request
def validate_channel_key():
    channel_key = request.headers.get("IFTTT-Channel-Key")
    if channel_key != 'qWxWsbxFo_0fcw6kjD6lluxjt2ydqyNBseYQ87DWGW1PEI1656eKG6pyLatkIobf':
        #print channel_key, type(channel_key)
        abort(401)

@app.route("/ifttt/v1/status")
def status():
    return ""

@app.route('/ifttt/v1/test/setup', methods=['POST'])
def test_setup():
    """Required by the IFTTT endpoint test suite."""
    ret = {'samples': {'triggers': {
    	'new_post_by_search_url': {'search_url': 'http://www.kijiji.ca/b-classic-cars/city-of-toronto/convertible/c122l1700273a161'}
    }}}
    return jsonify(data=ret)

app.add_url_rule('/ifttt/v1/triggers/new_post_by_search_url',
	view_func=RecentPostsView.as_view('new_post'))

if __name__ == "__main__":
    app.run()


