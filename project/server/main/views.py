# project/server/main/views.py
import ast
import json

import flask
import redis
from flask import Blueprint, request
from werkzeug.utils import redirect

from project.server.main.utils import upload_images, request_job_status, request_uploaded_links

main_blueprint = Blueprint('main', __name__,)
redisClient = redis.StrictRedis(host='localhost',
                                    port=6379,
                                    db=0)

@main_blueprint.route('/', methods=['GET'])
def index():
   """

   :rtype: object
   """
   return '''
        <html>
            <body>
                <h1 style="color: #5e9ca0;">LeadIQ <span style="color:#2b2301;">challenge</span></h1>
                <form action="/echo" method="POST">
                    <input name="client_id" value="63bbb2cd9f0bf7c">
                    <input type="submit" value="Redirect">
                </form>
            </body>
        </html>'''


@main_blueprint.route("/echo", methods=['POST'])
def echo():
    """

    :rtype: object
    """
    return redirect("https://api.imgur.com/oauth2/authorize?client_id=" + request.form['client_id'] + "&response_type=token&state=sssss", code=302)


@main_blueprint.route('/oauth2/callback/', methods=['GET', 'POST'])
def callback():
    """

    :rtype: object
    """
    return '''
        <script type="text/javascript">
            var loc = window.location.toString() ;
            var res = loc.replace("#", "&");
            res = res.replace('http://localhost:5000/oauth2/callback/?','') ;

            var req = new XMLHttpRequest();  

            var params = res;
            //alert(res)
            var url = 'http://localhost:5000/' + 'app_response_token?'
            req.open('POST', url, true);

            req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

            req.onreadystatechange = function() {//Call a function when the state changes.
                if(http.readyState == 4 && http.status == 200) {
                    alert(http.responseText);
                }
            }
            req.send(params);
            //alert('http://' + window.location.host + '/app_response_token?' + res)
        </script>
        Access Token Acquired
'''


@main_blueprint.route('/app_response_token', methods=['POST'])
def app_response_token():
    """

    :rtype: object
    """
    tokens = {
        "access_token": request.form["access_token"],
        "refresh_token": request.form["refresh_token"],
        "token_type": request.form["token_type"],
        "account_username": request.form["account_username"],
        "account_id": request.form["account_id"]
    }

    tokens.update({"AlbumId": '58tq5Nw'})
    # url = 'https://api.imgur.com/3/account/' + tokens["account_username"] + '/albums/'
    # token = tokens["access_token"]
    # authentication = {'Authorization': 'Bearer {0}'.format(token)}
    # response = requests.request('GET', url, headers=authentication, data={}, allow_redirects=False, timeout=None)
    # tokens.update({"AlbumId": json.loads(response.content)["data"][0]["id"]})

    redisClient.hset("Hash", "1", str(tokens))
    return ""

@main_blueprint.route('/v1/images/upload', methods=['POST'])
def image_upload():
    """

    :rtype: object
    """
    credentials = ast.literal_eval(redisClient.hget("Hash", "1"))
    jobId = upload_images(request.json["urls"],credentials)
    return flask.Response(json.dumps({
        'jobId': jobId
    }), mimetype=u'application/json')

@main_blueprint.route('/v1/images/upload/<jobId>', methods=['GET'])
def job_status(jobId):
    """

    :rtype: object
    """
    status = request_job_status(jobId)
    return flask.Response(json.dumps(
        status
    ), mimetype=u'application/json')

@main_blueprint.route('/v1/images', methods=['GET', 'POST'])
def image_links():
    """

    :rtype: object
    """
    credentials = ast.literal_eval(redisClient.hget("Hash", "1"))
    return flask.Response(json.dumps(
        request_uploaded_links(credentials)
    ), mimetype=u'application/json')

