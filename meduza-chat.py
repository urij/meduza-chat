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

# Функция, принимающая объект с сообщением и данными пользователей
# возвращающая отформатированный текст сообщения
def message_format(message, users):
	writer_id = message['user_id']
	writer_name = users[writer_id]['name']
	writer_text	= message['message']
	writer_is_admin = users[writer_id]['admin'] or writer_name == 'Meduza Bot'
	if message['status']:
		writer_time = '[УДАЛЕНО]'
	else:
		writer_time = '[{}]'.format(
			time_convert(message['inserted_at']))
	return '{GREEN}{BOLD}{time:<9}{RESETCL}{adm_l}{name:<20}{adm_r}{RESETAL}: {text}'.format(
		**{
			'name': writer_name,
			'time': writer_time,
			'text': writer_text,
			'adm_l': (writer_is_admin and colors['RED']) or '',
			'adm_r': (writer_is_admin and colors['RESETCL']) or '',
		},
		**colors
		)

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
		print(message_format(message, users))

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
