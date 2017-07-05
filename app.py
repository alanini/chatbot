

'''
import os, sys
from flask import Flask, request
from utils import wit_response, get_news_elements
from pymessenger import Bot

app = Flask(__name__)

PAGE_ACCESS_TOKEN = ""

bot = Bot(PAGE_ACCESS_TOKEN)


@app.route('/', methods=['GET'])
def verify():
	# Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	log(data)

	if data['object'] == 'page':
		for entry in data['entry']:
			for messaging_event in entry['messaging']:

				# IDs
				sender_id = messaging_event['sender']['id']
				recipient_id = messaging_event['recipient']['id']

				if messaging_event.get('message'):
					# Extracting text message
					if 'text' in messaging_event['message']:
						messaging_text = messaging_event['message']['text']
					else:
						messaging_text = 'no text'

					categories = wit_response(messaging_text)
					#elements = get_news_elements(categories)
					elements = get_news_elements()
					bot.send_generic_message(sender_id, elements)

	return "ok", 200


def log(message):
	print(message)
	sys.stdout.flush()


if __name__ == "__main__":
	app.run(debug = True, port = 80)



'''

import os, sys
from flask import Flask, request
from utils import wit_response
from pymessenger import Bot
from feedparser import parse

app = Flask(__name__)

PAGE_ACCESS_TOKEN = ""

bot = Bot(PAGE_ACCESS_TOKEN)


@app.route('/', methods=['GET'])
def verify():
	# Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	log(data)

	if data['object'] == 'page':
		for entry in data['entry']:
			for messaging_event in entry['messaging']:

				# IDs
				sender_id = messaging_event['sender']['id']
				recipient_id = messaging_event['recipient']['id']

				if messaging_event.get('message'):
					# Extracting text message
					if 'text' in messaging_event['message']:
						messaging_text = messaging_event['message']['text']
					else:
						messaging_text = 'no text'

					response = None

					entity, value = wit_response(messaging_text)
					if entity == 'bienvenida':
						response = "Hola, en qué te puedo ayudar?"
					
					if entity == 'pizza':
							response = "Seguro, te voy a enviar una pizza de {} ".format(str(value))
							
					
					if entity == 'nombre':
							response = "me llamo  {} ".format(str(value))
					
					if entity == 'newstype':
						#url = 'https://news.google.com.ar/news?cf=all&hl=es&pz=1&ned=es_ar&topic=b&output=rss'
						url = 'https://news.google.com.ar/news?cf=all&hl=es&pz=1&ned=es_ar&topic={}&output=rss'.format(str(value))
						d = parse(url)
						#response = d['feed']['title']
						#element = {'title': d['entries'][0]['title']}								
						response = d['entries'][0]['title'] 
						#response = element
						#response = []
						#response = Element(title="test1", subtitle="subtitle", item_url="http://arsenal.com")
						#response.append(element)
 
						
					#if entity == 'newstype':
					#	response = "Ok, I will send you the {} news".format(str(value))
					
					
					elif entity == 'location':
						response = "Ok, so you live in {0}. Here are top headlines from {0}".format(str(value))

					if response == None:
						response = "I have no idea what you are saying!hola"
						
					bot.send_text_message(sender_id, response)
					#bot.send_generic_message(sender_id, response)

	return "ok", 200


def log(message):
	print(message)
	sys.stdout.flush()


if __name__ == "__main__":
	app.run(debug = True, port = 80)
