from sys import argv
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

colors = {
	'GREEN'		: '',
	'GRAY'		: '',
	'PURPLE'	: '',
	'RED'		: '',
	'BOLD'		: '',
	'RESETCL'	: '',
	'RESETAL'	: '',
}

def associate_colors():
	try:
		import colorama
		colors['GREEN']		= colorama.Fore.GREEN
		colors['GRAY']		= colorama.Fore.LIGHTBLACK_EX
		colors['PURPLE']	= colorama.Fore.MAGENTA
		colors['RED']		= colorama.Fore.LIGHTRED_EX
		colors['BOLD']		= colorama.Style.BRIGHT
		colors['RESETCL']	= colorama.Fore.RESET
		colors['RESETAL']	= colorama.Style.RESET_ALL
	except:
		print('''
	Цветной вывод отключён. Необходима библиотека colorama.
	Установить её можно с помощью pip.
	Для принудительного запуска без цветов используйте параметр --no-colors
		''')

def ref(j = [0]):
	j[0] += 1
	return j[0]

def help():
	print('''
Консольная читалка чатов с https://meduza.io
Для обычного запуска и чтения последних чатов параметры не требуются.

Для чтения определённого чата необходимо указать полную ссылку на страницу новости, с которой связан чат.
meduza-chat.py [ссылка на новость]

      --no-colors       отключение цветного вывода
  -h  --help            показать эту справку
	''')

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

# Функция, игнорирующая данные со списком чатов (topic lobby)
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

	reply_to = message['reply_to_user_id']
	writer_reply_to = (reply_to and '@'+users[reply_to]['name']) or ''

	# id 60081 — Meduza Bot
	writer_is_admin = users[writer_id]['admin'] or writer_id == '60081'
	if message['status']:
		writer_time = '[УДАЛЕНО]'
	else:
		writer_time = '[{}]'.format(
			time_convert(message['inserted_at']))
	return '{GREEN}{BOLD}{0:<9}{RESETCL}{1}{2:<20}{3}{RESETAL}: {BOLD}{4}{RESETAL} {5}'.format(
		writer_time,
		(writer_is_admin and colors['RED']) or '',
		writer_name,
		(writer_is_admin and colors['RESETCL']) or '',
		writer_reply_to,
		writer_text,
		**colors
		)
# Разорвать соединение с сервером, вывести сообщение и выйти из приложения
def close_app():
	ws.close()
	print('\rСоединение разорвано')
	exit()

# Посылает команду о закрытии и прекращении отслеживания чата
# По умолчанию закрывает список чатов (topic lobby)
def topic_close(topic_addr = 'lobby'):
	data = {
		"topic":"topic:{}".format(topic_addr),
		"event":"close",
		"payload":{"reason":"close"},
		"ref":"{}".format(ref())
		}
	data = json.dumps(data)
	ws.send(data)
	ws.recv()
	data = {
		"topic":"topic:{}".format(topic_addr),
		"event":"phx_leave",
		"payload":{},
		"ref":"{}".format(ref())
		}
	data = json.dumps(data)
	ws.send(data)
	ws.recv()
	ws.recv()

# Процедура принимает адрес чата, выводит последние сообщения
# и переходит в режим ожидания новых сообщений (мониторинга)
def topic_monitoring(topic_addr):
	heart_time = time.time()
	r = get_topic(topic_addr)
	if r['payload']['status'] == 'error':
		print('{RED}[[[ЧАТ НЕ СУЩЕСТВУЕТ или ССЫЛКА НЕ ВЕРНА]]]{RESETCL}'.format(**colors))
		return
	response = r['payload']['response']
	chat_id = str(response['chat_id'])
	chat_title = response['chats'][chat_id]['title']
	chat_second_title = response['chats'][chat_id]['second_title']

	print('Чат #{}: {BOLD}{}{RESETAL}\n{}'.format(
		chat_id,
		chat_title,
		chat_second_title or '',
		**colors
		))

	if response['chats'][chat_id]['messages_count'] == 0:
		print('{RED}[[[ЧАТ НЕ СОДЕРЖИТ СООБЩЕНИЙ]]]{RESETCL}'.format(**colors))
		return

	is_monitoring = True
	while is_monitoring:
		messages = response['messages']
		ids = response['messages_ids']
		# В некоторых случаях, когда автор нового сообщения Meduza Bot
		# в ответе отсутствует users с необходимыми данными
		try:
			users = response['users']
		except KeyError:
			users = {
				'id':"60081",
				'name':"Meduza Bot"
				}
		for i in ids:
			message = messages[i]
			print(message_format(message, users))
		try:
			chat_active = response['chats'][chat_id]['active']
		except:
			pass
		else:
			if not chat_active:
				print('{RED}[[[ЧАТ ЗАКРЫТ]]]{RESETCL}'.format(**colors))
				break

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
			except KeyboardInterrupt:
				is_monitoring = False
				break
			except websocket._exceptions.WebSocketTimeoutException:
				continue
			except:
				raise

wss_addr = 'wss://meduza.io/pond/socket/websocket?token=no_token&vsn=1.0.0'
ws = websocket.WebSocket()
ws.settimeout(5.0)
ws.connect(wss_addr)
args = argv[1:]
if args:
	if not args.count('--no-colors'):
		associate_colors()
	if args.count('-h') or args.count('--help'):
		help()
		exit()
	elif args[0].count('meduza.io/'):
		url = args[0]
		topic_addr = url[url.index('meduza.io/')+10:]
		topic_monitoring(topic_addr)
		close_app()
else:
	associate_colors()

try:
	while True:
		topic_addr = get_topic_addr()
		topic_close()
		print('\r' + '—'*30)
		topic_monitoring(topic_addr)
		print('\r' + '—'*30)
		topic_close(topic_addr)
except KeyboardInterrupt:
	close_app()
except:
	raise
