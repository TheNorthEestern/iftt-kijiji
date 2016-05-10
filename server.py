from flask import Flask, request, abort, jsonify
app = Flask(__name__)

app.debug = False

@app.errorhandler(401)
def unauthorized(e):
    error = {'message' :'Unauthorized'}
    return jsonify(errors=[error]), 401

@app.before_request
def validate_channel_key():
    channel_key = request.headers.get("IFTTT-Channel-Key")
    if not app.debug and channel_key != 'qWxWsbxFo_0fcw6kjD6lluxjt2ydqyNBseYQ87DWGW1PEI1656eKG6pyLatkIobf':
        print channel_key, type(channel_key)
        abort(401)

@app.route("/ifttt/v1/status")
def status():
    return ""

if __name__ == "__main__":
    app.run()
