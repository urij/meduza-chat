import json
import time

try:
	import websocket
except:
	print('''
	Для работы приложения необходима библиотека websocket-client.
	Установить её можно с помощью pip.
	''')
	exit()

try:
	import colorama
	colors = {
		'GREEN'		: colorama.Fore.GREEN,
		'GRAY'		: colorama.Fore.LIGHTBLACK_EX,
		'PURPLE'	: colorama.Fore.MAGENTA,
		'RED'		: colorama.Fore.LIGHTRED_EX,
		'BOLD'		: colorama.Style.BRIGHT,
		'RESETCL'	: colorama.Fore.RESET,
		'RESETAL'	: colorama.Style.RESET_ALL,
	}
except:
	print('''
	Цветной вывод отключён. Необходима библиотека colorama.
	Установить её можно с помощью pip.
	''')
	colors = {
		'GREEN'		: '',
		'GRAY'		: '',
		'PURPLE'	: '',
		'RED'		: '',
		'BOLD'		: '',
		'RESETCL'	: '',
		'RESETAL'	: '',
	}

class increaser():
     def __init__(self):
         self.i = 1
     def __call__(self):
         self.i += 1
         return self.i
ref = increaser()

def time_convert(unix_time):
	localtime = time.localtime(unix_time)
	h = localtime.tm_hour
	m = localtime.tm_min
	return '{:0>2}:{:0>2}'.format(h, m)

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
	for chat_id in chats_ids:
		chat = r['payload']['chats'][chat_id]
		messages_count = chat['messages_count']
		if messages_count == 0: continue
		title = chat['title']
		print('{:<4} {}  {GRAY}({}){RESETCL}'.format(
			chat_id + ')',
			title,
			messages_count,
			**colors
			))
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

# Функция, игнорирующая данные со списком чатов
# Этот список периодический отправляется сервером, и нам не нужен
def safe_recv(data):
	while True:
		data = json.loads(data)
		if data['topic'] == 'topic:lobby':
			data = ws.recv()
		else:
			return data

wss_addr = 'wss://meduza.io/pond/socket/websocket?token=no_token&vsn=1.0.0'
ws = websocket.WebSocket()
ws.connect(wss_addr)

topic_addr = get_topic_addr()
heart_time = time.time()
r = get_topic(topic_addr)
response = r['payload']['response']
print('—'*30)

while True:
	messages = response['messages']
	users = response['users']
	ids = response['messages_ids']
	for i in ids:
		message = messages[i]
		writer_name = users[message['user_id']]['name']
		writer_text = message['message']
		if message['status']:
			message_time = '[УДАЛЕНО]'
		else:
			message_time = '[{}]'.format(
				time_convert(message['inserted_at']))
		print('{GREEN}{BOLD}{:<9}{RESETCL}{:<20}{RESETAL}: {}'.format(
			message_time,
			writer_name,
			writer_text,
			**colors
			))

	while True:
		try:
			time.sleep(2)
			if (time.time() - heart_time) > 25:
				heart_time = time.time()
				data = {
					"topic":"phoenix",
					"event":"heartbeat",
					"payload":{},
					"ref":"{}".format(ref())
					}
				data = json.dumps(data)
				ws.send(data)
			r = json.loads(ws.recv())
			if r != '' and r['event'] == 'new_msg':
				response = r['payload']
				break
			else:
				continue
		except:
			ws.close()
			print('\rСоединение разорвано')
			exit()
