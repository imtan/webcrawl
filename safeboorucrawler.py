from urllib.request import urlopen
import xml.dom.minidom
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.error import HTTPError
from urllib.error import URLError
import urllib.request
import requests
import re
import json
import io
import os



home_dir = os.environ['HOME']
danbooru_url = "http://safebooru.donmai.us/"

def return_IFTTT_value1(jsondata):
    payload = "{ 'value1' : '" + jsondata + "'}"
    requests.post("https://maker.ifttt.com/trigger/image_request/with/key/{secret_key}", data=payload)

def json_parse_print(parsed_json_datas):
    print (json.dumps(parsed_json_datas,sort_keys=True,indent=4))

def download_large_file(post,search_word):
    large_file_url = post['large_file_url']
    charactertag = post['tag_string_character']
    filename = post['id']
    fileext = post['file_ext']
    make_dir_if_not_exist(home_dir+"/Downloads/Images/{0}/{1}".format(search_word,charactertag,filename))
    urllib.request.urlretrieve('http://safebooru.donmai.us/' + large_file_url,home_dir + "/Downloads/Images/{0}/{1}/{2}.{3}".format(search_word,charactertag,filename,fileext))
    print("complete:{0}".format(filename))

def download_large_files(parsed_json_datas,search_word):
    posts = parsed_json_datas
    for post in posts:
        download_large_file(post,search_word)

def make_dir_if_not_exist(dir_name):
    if not (os.path.exists(dir_name)):
        os.mkdir(dir_name)


isUSE_PROXY = False
if isUSE_PROXY:
    proxies = {'http': 'http://cache.ccs.kogakuin.ac.jp:8080'}
url = "http://safebooru.donmai.us/posts.json?tags=kantai_collection&limit=100"

if isUSE_PROXY:
    html = urlopen(url,proxies = proxies)
else:
    html = urlopen(url)

word = input()
search_word = word.replace(" ","-")

make_dir_if_not_exist(home_dir+"/Downloads/Images")
make_dir_if_not_exist(home_dir+"/Downloads/Images/{0}".format(search_word))

print ("persing")

json_string = html.read().decode('utf-8')
safebooru_posts = json.loads(json_string)
#json_parse_print(safebooru_posts)
#print all character tags for limit

#download_large_file_url(safebooru_posts)

for post in safebooru_posts:
    charactertag = post['tag_string_character']
#    print (charactertag)
    download_large_files(safebooru_posts,search_word)
