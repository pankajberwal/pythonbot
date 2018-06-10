import json
import requests
import time
import urllib
from dbhelper import DBHelper

db=DBHelper()

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

def build_keyboard(items):
    keyboard=[[item] for item in items]
    reply_markup={"keyboard":keyboard , "one_time_keyboard":True}
    return json.dumps(reply_markup)

def handle_updates(updates):
    for update in updates["result"]:
        text=update["message"]["text"]
        chat=update["message"]["chat"]["id"]
        items=db.get_item(chat)
        if text=="/done":
            keyboard=build_keyboard(items)
            send_message("Select an Item to DELETE",chat,keyboard)
        elif text == "/start":
            send_message(
                "Welcome to your personal To Do list. Send any text to me and I'll store it as an item. Send /done to remove items",
                chat)
        elif text.startswith("/"):
            continue
        elif text in items:
            db.delete_item(text,chat)
            items=db.get_item(chat)
            keyboard = build_keyboard(items)
            send_message("Select an Item to DELETE", chat, keyboard)
        else :
            db.add_item(text,chat)
            items=db.get_item(chat)
            message="\n".join(items)
            send_message(message,chat)


def get_last_chatId_and_text(updates):
    numupdates=len(updates["result"])
    last_update=numupdates-1
    text=updates["result"][last_update]["message"]["text"]
    chat_id=updates["result"][last_update]["message"]["chat"]["id"]
    return  text,chat_id



def send_message(text,chat_id,reply_markup=None):
    text= urllib.parse.quote_plus(text)
    url=URL+"sendMessage?chat_id={}&text={}&parse_mode=Markdown".format(chat_id,text)
    if reply_markup:
        url+="&reply_markup={}".format(reply_markup)
    get_url(url)

def main():
    db.setup()
    last_updateid=None
    while True:
        updates=get_updates(last_updateid)
        if len(updates["result"]) > 0:
            last_updateid=get_last_update_id(updates)+1
            handle_updates(updates)
        time.sleep(0.5)

if __name__=='__main__':
    main()
