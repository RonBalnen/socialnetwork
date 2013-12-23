__author__ = 'ron'
from flask import Flask
from selenium import webdriver
import vkontakte
import vk_auth
import json
import time
from urlparse import urlparse

app = Flask(__name__)

@app.route('/vkontakte/friends/get/all/<string:token>', methods=['GET'])
def vkontakte_get_all_friends(token):
    vk = vkontakte.API(token=token)
    friends = vk.get('friends.get', fields='sex, photo_100, photo_50, bdate')
    return json.dumps(friends)

@app.route('/vkontakte/friends/get/all/<string:token>/<int:owner_id>', methods=['GET'])
def vkontakte_get_all_friends_by_userid(token, owner_id):
    vk = vkontakte.API(token=token)
    friends = vk.get('friends.get', user_id=owner_id, fields=['sex','bdate', 'photo_100'])
    return json.dumps(friends)

@app.route('/vkontakte/wall/post/<string:token>/<int:recp_user_id>')
def vkontate_post_wall_by_recp_user_id(token,recp_user_id):
    vk = vkontakte.API(token=token)
    message = 'Invitation to the event'
    wall = vk.get('wall.post', owner_id=recp_user_id, message=message)
    return json.dump(wall)

@app.route('/vkontakte/token/getstandalone')
def vkontakte_get_standalone_token():
    browser = webdriver.Firefox()
    url = "http://oauth.vk.com/oauth/authorize?" + \
        "redirect_uri=http://oauth.vk.com/blank.html&response_type=token&" + \
        "client_id=4009955&scope=friends,wall,messages&display=wap"
    browser.get(url)
    while url == browser.current_url:
        time.sleep(1)
    url_token = browser.current_url
    o = urlparse(url_token)
    answer = dict()
    for item in o.fragment.split('&'):
        item_list = item.split('=')
        answer[item_list[0]] = item_list[1]

    return json.dumps(answer["access_token"])

@app.route('/open_browser')
def open_browser():
    browser = webdriver.Firefox()
    url = "http://oauth.vk.com/oauth/authorize?" + \
        "redirect_uri=http://oauth.vk.com/blank.html&response_type=token&" + \
        "client_id=4009955&scope=friends,wall,messages&display=wap"
    browser.get(url)
    while url == browser.current_url:
        time.sleep(1)
    url_token = browser.current_url
    o = urlparse(url_token)
    answer = dict()
    for item in o.fragment.split('&'):
        item_list = item.split('=')
        answer[item_list[0]] = item_list[1]

    return json.dumps(answer["access_token"])

if __name__ == '__main__':
    app.run(debug = True)
