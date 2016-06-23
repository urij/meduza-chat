# Читалка чатов на Meduza.io

#### Что случилось?
23 июня 2016 на сайте [Медузы](https://meduza.io) была добавлена возможность комментирования и обсуждения новостей в виде чата.

#### Эта программа позволяет спамить в чат?
Нет, это просто консольное приложение, позволяющее читать сообщения из чата

#### Но зачем мне оно, я ведь могу читать чат на сайте?
 - Just for Fun
 - На примере этого кода кто-то сможет создать действительно полезное приложение

#### Окей, как мне его запустить?
Понадобится интерпретатор Python 3.
Так же потребуется установить библиотеку websocket
```
pip3 install websocket
```

#### Какой функционал у приложения?
Пока функционала как такового нет. Кроме того код содержит много недоработок и ошибок, т.к. писался на скорую руку.

Функции, хоть как-то да реализованные в приложении:
+ Вывод последних новостей, содержащих комментарии (записи в чате)
+ Вывод записей из чата у выбранной новости