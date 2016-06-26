# Читалка чатов на Meduza.io

#### Что случилось?
23 июня 2016 на сайте [Медузы](https://meduza.io) была добавлена возможность комментирования и обсуждения новостей в виде чата.

#### Эта программа позволяет спамить в чат?
Нет, это просто консольное приложение, позволяющее читать сообщения из чата

#### Но зачем мне оно, я ведь могу читать чат на сайте?
 - Just for Fun
 - На примере этого кода кто-то сможет создать действительно полезное приложение

###### Кроме того в приложении доступны функции, которых нет в чате на сайте:
 + Чтение закрытых («удалённых») чатов
 + Подсветка администраторов чата

#### Окей, как мне его запустить?
1. Понадобится интерпретатор языка Python 3.
2. Для работы приложения требуется библиотека [websocket-client](https://pypi.python.org/pypi/websocket-client).
3. Для работы цветного (красивого) вывода необходима библиотека [colorama](https://pypi.python.org/pypi/colorama).

Установить необходимые библиотеки можно с помощью pip:
``` bash
pip3 install websocket-client
```

Запустить приложение через консоль:
``` bash
python3 meduza-chat.py
```

Для чтения чата определённой статьи (даже если чат уже закрыт):
``` bash
python3 meduza-chat.py [ссылка]
# например
python3 meduza-chat.py https://meduza.io/feature/2016/06/24/strana-podozrevaemyh
```

#### Какой функционал у приложения?
Функции, реализованные в приложении:
+ Вывод последних новостей, у которых есть сообщения в чате
  * Напротив каждой новости указывается количество сообщений
  * Навигация осуществляется с помощью ввода id чата
+ Вывод сообщений из чата у выбранной новости
  * Время сообщений
  * Удалённые сообщения так же выводятся, но с соответствующей пометкой
  * Администраторы и официальный бот подсвечиваются
  * Смайлы отображаются, если это поддерживает шрифт терминала
  * После вывода последних сообщений, приложение ожидает новые, и выводит их по мере поступления
+ Вывод закрытых чатов
  * Всё то же, что и у обычных, но не ожидает новые сообщения

Будьте готовы к тому, что приложение содержит ошибки, и различные недоработки.

Работоспособность протестирована на Linux и macOS.

![Демонстрация](media/show.gif)
