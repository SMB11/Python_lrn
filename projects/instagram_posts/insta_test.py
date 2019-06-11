from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
app = Flask(__name__)
import requests
import json

client_id='d832ae3f1f1f448bbb8bc1ba6e6e1f1e'
client_secret="a7f815325e9748f9b1b8cf6a2469cea1"

@app.route('/authorize-instagram')
def authorize_instagram():
    from instagram import client
    redirect_uri = ("http://localhost:5000" + url_for('handle_instagram_authorization'))
    print(redirect_uri)
    instagram_client = client.InstagramAPI(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
    return redirect(instagram_client.get_authorize_url(scope=['basic']))

@app.route('/handle-instagram-authorization')
def handle_instagram_authorization():
    from instagram import client

    code = request.values.get('code')
    print(request.values)
    if not code:
        return "Message:Missing code", 400
    # try:
    redirect_uri = ("http://localhost:5000" + url_for('handle_instagram_authorization'))
    instagram_client = client.InstagramAPI(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
    access_token, instagram_user = instagram_client.exchange_code_for_access_token(code)
    if not access_token:
        return "Message:Could not get access token", 400
    g.user.instagram_userid = instagram_user['id']
    g.user.instagram_auth   = access_token
    g.user.save()
    deferred.defer(fetch_instagram_for_user, g.user.get_id(), count=20, _queue='instagram')
    # except Exception:
    #     return "Message:Error", 400
    return redirect(url_for('settings_data') + '?after_instagram_auth=True')






if __name__ == '__main__':
    app.run(debug=True)