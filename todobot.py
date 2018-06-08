import json
import requests
import time
import urllib

TOKEN="608570150:AAF3y6w9KgM7tATrYsMN6u0KxY7DCFNe6eE"
URL="https://api.telegram.org/bot{}/".format(TOKEN)

def get_url(url):
    response=requests.get(url)
    content=response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content=get_url(url)
    js=json.loads(content)
    return js

def get_updates(offset=None):
    url=URL+"getupdates?timeout=100"
    if offset:
        url=url+"&offset={}".format(offset)
    js=get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids=[]
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def echo_all(updates):
    for update in updates["result"]:
        try:
            text=update["message"]["text"]
            chat_id=update["message"]["chat"]["id"]
            send_message(text,chat_id)
        except Exception as e:
            print(e)

def get_last_chatId_and_text(updates):
    numupdates=len(updates["result"])
    last_update=numupdates-1
    text=updates["result"][last_update]["message"]["text"]
    chat_id=updates["result"][last_update]["message"]["chat"]["id"]
    return  text,chat_id

def send_message(text,chat_id):
    text= urllib.parse.quote_plus(text)
    url=URL+"sendMessage?chat_id={}&text={}".format(chat_id,text)
    get_url(url)

def main():
    last_updateid=None
    while True:
        updates=get_updates(last_updateid)
        if len(updates["result"]) > 0:
            last_updateid=get_last_update_id(updates)+1
            echo_all(updates)
        time.sleep(0.5)

if __name__=='__main__':
    main()
