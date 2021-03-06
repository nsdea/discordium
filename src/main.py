# Local
import user as user_module
import channel as channel_module
import message as message_module

import os
import flask
import discord

from threading import Thread
from functools import partial
from discord.ext import commands
from dotenv import load_dotenv

# =========================== SETUP ======================================

load_dotenv()

app = flask.Flask(__name__)
app.config.from_object(__name__)
client = commands.Bot(command_prefix='!')

globals()['current_channel'] = f'<h1>Welcome to Discordium</h1>'
globals()['current_html'] = '<h1><a href="/">Click me</a></h1>'

# =========================== DISCORD =====================================

# @client.event
# async def on_message(message):
#     globals()['current_channel'] = f'<h1>{message.content}</h1>'

# ============================ FLASK ======================================

def channel_dropdown():
    html_dropdown = '\n'

    for guild in client.guilds:
        for channel in guild.channels:
            if isinstance(channel, discord.TextChannel) and channel.permissions_for(guild.get_member(client.user.id)).send_messages:
                html_dropdown += f'\n<option value="{channel.id}">[{guild.name}] {channel.name}</option>'

    return html_dropdown

def chat_loader(channel_id):
    html_chat = '\n'

    messages = list(channel_module.Channel(channel_id=channel_id).messages)[:10]

    for msg in messages:
        text = msg['content']
        author = msg['author']['username']

        html_chat += f'<h4>{author}</h5>\n<p>{text}</p>'

    return html_chat

@app.route('/', methods=['POST', 'GET'])
def home():
    if flask.request.method == 'GET':
        globals()['current_html'] = open('html/style_base.html').read().replace('<!-- %CODE% -->', globals()['current_channel']).replace('<!-- %CHANNEL_DROPDOWN% -->', channel_dropdown())
        return globals()['current_html']
    else:
        data = flask.request.form.to_dict()

        for guild in client.guilds:
            for channel in guild.channels:
                if channel.id == int(data['channel']):
                    c = channel_module.Channel(channel.id)
                    c.send(data['message'])

                    return globals()['current_html'].replace('<!-- %CHAT% -->', chat_loader(channel.id))
    
# ============================ RUN ========================================

partial_run = partial(app.run, host='localhost', port=2876, debug=True, use_reloader=False)

t = Thread(target=partial_run)
t.start()

client.run(os.getenv('DISCORD_TOKEN'))