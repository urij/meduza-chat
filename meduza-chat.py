import websocket
import json
from time import sleep

def get_topic_addr():
	data = {"topic":"topic:lobby","event":"phx_join","payload":{},"ref":"1"}
	data = json.dumps(data)
	ws.send(data)
	ws.recv()
	result = ws.recv()
	r = json.loads(result)
	chats_ids = r['payload']['chats_ids']
	for i in chats_ids:
		chat = r['payload']['chats'][i]
		messages_count = chat['messages_count']
		if messages_count == 0: continue
		title = chat['title']
		print('{:<4} {}  ({})'.format(i + ')', title, messages_count))
	chats_id = input('> Введите номер чата: ')
	return r['payload']['chats'][chats_id]['key']


def get_topic(topic_addr):
	data = {
		"topic":"topic:{}".format(topic_addr),
		"event":"phx_join",
		"payload":{},
		"ref":"2"
		}
	data = json.dumps(data)
	ws.send(data)
	return ws.recv()

wss_addr = 'wss://meduza.io/pond/socket/websocket?token=no_token&vsn=1.0.0'
ws = websocket.WebSocket()
ws.connect(wss_addr)

topic_addr = get_topic_addr()

result = get_topic(topic_addr)

while True:
	r = json.loads(result)
	messages = r['payload']['response']['messages']
	users = r['payload']['response']['users']
	ids = r['payload']['response']['messages_ids']
	for i in ids:
		message = messages[i]
		writer_name = users[message['user_id']]['name']
		writer_text = message['message']
		print('{:<20} {}'.format(writer_name + ':', writer_text))
	while True:
		sleep(5)
		result = ws.recv()
		if not result: break

ws.close()
