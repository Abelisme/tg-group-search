from telethon import TelegramClient, sync, utils
import asyncio, datetime,configparser
from flask import Flask, jsonify, render_template, request,redirect, url_for
# import Message
from model.models import Message
app = Flask(__name__, template_folder = 'templates')

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
api_id = 4190078
api_hash = '1b8b4ebef76ebd1a2f469884694d2940'
client = TelegramClient('session_name', api_id, api_hash)
client.start()
#create a listener
loop = asyncio.get_event_loop()

@app.route('/search', methods = ['GET'])
def loopRun():
    # api_id = request.args.get('api_id', 0, type=str)
    # api_hash = request.args.get('api_hash', 0, type=str)
    headings = ("訊息","時間","URL")
    search_word = request.args.get('search_word', 0, type=str)
    target_group = request.args.get('target_group', 0, type=str)
    messages = loop.run_until_complete(main(search_word, target_group))
    # messages = main(search_word, target_group)
    return render_template('index.html', headings = headings,
                           messages = messages)
    # return redirect(url_for('.bootstrapTable', headings = headings, messages=messages))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/table')
def bootstrapTable():
    return render_template('bootstrap_table.html')

async def main(search_word, target_group):
    #get messages from speci username
    list = []
    channel_records = await client.get_entity(target_group)
    date_of_post = datetime.datetime(2020, 6, 6)
    # reverse = True -> From oldest to most-recent
    async for message in client.iter_messages(channel_records, offset_date = date_of_post, reverse = True, limit = 1000):
        # if(str(message.message).find(search_word) > -1):
        if(search_word in str(message.message)):
            # print(message.message, message.date)
            messages = Message(message.message,message.date,message.id)
            list.append(messages)
    
    return list

# app.run(debug=True)
