# Читалка чатов на Meduza.io

#### Что случилось?
23 июня 2016 на сайте [Медузы](https://meduza.io) была добавлена возможность комментирования и обсуждения новостей в виде чата.

##### [Чаты на «Медузе»? Зачем?](https://meduza.io/cards/chaty-na-meduze-zachem)

#### Эта программа позволяет спамить в чат?
Нет, это просто консольное приложение, позволяющее читать сообщения из чата.

#### Но зачем мне оно, я ведь могу читать чат на сайте?
 - Just for Fun
 - На примере этого кода кто-то сможет создать действительно полезное приложение
 - Не у всех ОС есть графическая оболочка, это приложение поможет читать чаты и без неё

##### Кроме того в приложении доступны функции, которых нет в чате на сайте:
 + Чтение закрытых («удалённых») каналов
 + Чтение удалённых сообщений
 + *Подсветка администраторов чата* (уже такая возможность появилась и на сайте)

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

Для чтения канала определённого материала (даже если канал уже закрыт):
``` bash
python3 meduza-chat.py [ссылка]
# например
python3 meduza-chat.py https://meduza.io/feature/2016/06/24/strana-podozrevaemyh
```

#### Какой функционал у приложения?
Функции, реализованные в приложении:
+ Вывод последних материалов, у которых есть сообщения в канале
  * Напротив каждого материала указывается количество сообщений
  * Навигация осуществляется с помощью ввода id канала
+ Вывод сообщений из каналов
  * Время сообщений
  * Удалённые сообщения так же выводятся, но с соответствующей пометкой
  * Администраторы и официальный бот подсвечиваются
  * Смайлы отображаются, если это поддерживает шрифт терминала
  * После вывода последних сообщений, приложение ожидает новые, и выводит их по мере поступления
+ Вывод закрытых каналов
  * Всё то же, что и у обычных, но не ожидает новые сообщения

Работоспособность протестирована на Linux и macOS, Python версии ≥3.4.

![Демонстрация](media/show.gif)
