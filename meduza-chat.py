import websocket
import json
from time import sleep

class increaser():
     def __init__(self):
         self.i = 1
     def __call__(self):
         self.i += 1
         return self.i
ref = increaser()

def get_topic_addr():
	data = {
		"topic":"topic:lobby",
		"event":"phx_join",
		"payload":{},
		"ref":"{}".format(ref())
		}
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
	while True:
		chats_id = input('> Введите номер чата: ')
		try:
			return r['payload']['chats'][chats_id]['key']
		except:
			print('Вы ввели недопустимый номер')


def get_topic(topic_addr):
	data = {
		"topic":"topic:{}".format(topic_addr),
		"event":"phx_join",
		"payload":{},
		"ref":"{}".format(ref())
		}
	data = json.dumps(data)
	ws.send(data)
	return safe_recv(ws.recv())

def safe_recv(data):
	if json.loads(data)['topic'] == 'topic:lobby':
		return ws.recv()
	else:
		return data

wss_addr = 'wss://meduza.io/pond/socket/websocket?token=no_token&vsn=1.0.0'
ws = websocket.WebSocket()
ws.connect(wss_addr)

topic_addr = get_topic_addr()

result = get_topic(topic_addr)
r = json.loads(result)

while True:
	messages = r['payload']['response']['messages']
	users = r['payload']['response']['users']
	ids = r['payload']['response']['messages_ids']
	for i in ids:
		message = messages[i]
		writer_name = users[message['user_id']]['name']
		writer_text = message['message']
		print('{:<20} {}'.format(writer_name + ':', writer_text))
	ws.close()
	exit()
	
	while True:
		sleep(5)
		try:
			result = get_topic(topic_addr)
			if result:
				print(result)
				break
		except:
			ws.close()
			print('Соединение разорвано')
			exit()
