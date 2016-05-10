from flask import Flask, request, abort, jsonify
app = Flask(__name__)

app.debug = True
app.config['JSON_AS_ASCII'] = False

@app.errorhandler(401)
def unauthorized(e):
    error = {'message' :'Unauthorized'}
    return jsonify(errors=[error]), 401

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
    if not app.debug and channel_key != 'qWxWsbxFo_0fcw6kjD6lluxjt2ydqyNBseYQ87DWGW1PEI1656eKG6pyLatkIobf':
        #print channel_key, type(channel_key)
        abort(401)

@app.route("/ifttt/v1/status")
def status():
    return ""

@app.route('/ifttt/v1/test/setup', methods=['POST'])
def test_setup():
    """Required by the IFTTT endpoint test suite."""
    ret = {'samples': {'triggers': {}}}
    return jsonify(data=ret)

if __name__ == "__main__":
    app.run()
