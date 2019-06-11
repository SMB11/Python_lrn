from flask import Flask, render_template, redirect, request, url_for
from datetime import datetime
app = Flask(__name__)
import requests
import json
from urllib.parse import urlparse

# from urllib2 import urlopen
# from urlparse import urlparse

# url = urlparse(req.geturl())
# url.query


datas ={} 
url = 'https://api.instagram.com/v1/users/self/media/recent/?access_token='
token = ''
client_id = 'your clid'
client_secret='yout secret'









@app.route("/")
def index():
    if token == '':
        return redirect("https://api.instagram.com/oauth/authorize/?client_id=clinent_id&redirect_uri=http://localhost:5000/callback&response_type=code")
    else:
        return render_template('home.html',datas=datas)
    
@app.route("/callback")
def callback():
    code = request.args.get('code')

    payload = {'client_id': client_id,
    'client_secret': client_secret,
    'grant_type': 'authorization_code',
    'redirect_uri': 'http://localhost:5000/callback',
    'code': code}

    r = requests.post('https://api.instagram.com/oauth/access_token', data=payload)
    response = json.loads(r.text)
    print(response)
    global token
    token = response["access_token"]
    print("this is in callback" + token)
    return redirect(url_for('home'))

@app.route("/home")
def home():
    if token == '':
        return redirect('http://localhost:5000/')
    print(token)
    rs = requests.get(url+token)
    print(url+token)
    if rs.status_code == 200:
        response = json.loads(rs.text)
        global datas
        datas = response["data"]
        if len(datas)==0:
            return render_template('home.html')
        return render_template('home.html',datas=datas)
    else:
       return "Smth is wrong"

@app.route("/logout")
def logout():
    global token
    token = ''
    print(token+" This is in logout")
    return redirect('http://localhost:5000/')


if __name__ == '__main__':
    app.run(debug=True)
