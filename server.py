from flask import Flask, request, abort
from datetime import datetime
from random import choice
import time

app = Flask(__name__)


db = [
    # {'msg', 'name', 'datetime'} - база данных в виде списка из словарей
]

@app.route("/")
def hello_world():
    '''Функция ничего не принимает, выводит приветствие на главной странице сервера.
    '''
    return "<p>Hello, User!</p>"


@app.route("/status")
def status():
    '''Функция показывает название мессенджера, количество активных пользователей и время на сервере по эндпоинту /status
    '''

    users = set()
    for i in db:
        users.add(i['name'])
    return {"name": "My first messenger", "number_of_users": len(users), "time": datetime.now().strftime('%d.%m.%Y %H:%M:%S')}


def prediction(msg, name):
    """Вместо обычного сообщения, возвращает сообщение с предсказанием.
    В переменной answer находятся несколько предсказаний, одно из которых рандомным образом прибавляется к исходному сообщению.

    :param msg: полученное сообщение
    :param name: имя отправителя
    :return: возвращает новое сообщение
    """

    answers = ["Вы находитесь на верном пути.",
               "Прилив энергии поможет Вам справиться с большим объемом незапланированных работ.",
               "Пришло время действовать!", "Терпение! Вы почти у цели.",
               "Пришло время закончить старое и начать новое.",
               "Цель определяет успех.", "Вас ожидают перемены.", "Ждите перемен.",
               "Звезды к вам благосклонны.", "Вы — на верном пути!"]
    message_dict = {
        "msg": msg + '\n\n' + choice(answers),
        "name": name,
        "datetime": time.time()
    }
    return message_dict


@app.route("/send", methods=["POST"]) # POST-запрос, поскольку мы отправляем какие-то данные
def send_message(): # вызывается каждый раз, когда мы делаем запрос к эндпоинту /send
    '''Функция, необходимая для того, чтобы отправить сообщение от какого-либо человека.
    Все необходимые данные получаются с помощью объекта request.
    '''
    data = request.json # клиент отправляет запрос на сервер с данными, мы из request можем достать эти данные в форме json
    # обрабатываем исключения:
    if not isinstance(data, dict): # проверяем, что данные имеют тип dict
        abort(400)
    if "name" not in data or "msg" not in data: # проверяем наличие ключей
        abort(400)
    if len(data['msg']) == 0 or len(data['msg']) >= 100: # Длина сообщения от 1 до 99
        abort(400)
    if len(data['name']) == 0 or len(data['name']) >= 100: # Длина имени от 1 до 99
        abort(400)
    name = data["name"] # данные из json по ключу name
    msg = data["msg"] # данные из json по ключу msg
    # создаем новое сообщение в зависимости оттого, есть ли слово "предсказание" в нем:
    if 'предсказание' in msg.lower():
        message_dict = prediction(msg, name)
    else:
        message_dict = {
            "msg": msg,
            "name": name,
            "datetime": time.time()
        }
    db.append(message_dict) # добавляем сообщение в словарь
    return {"status": "OK"}


@app.route('/receive', methods=['GET'])
def get_messages():
    '''Функция, позволяющая получить все сообщения из базы данных начиная с какого-либо промежутка времени.
    С помощью объекта request получает параметры, которые передаются в get-запросе.
    Параметр after позволяет получать только новые сообщения (возвращаются только сообщения после after)
    '''
    data = request.args
    try:
        after = float(data['after'])
    except ValueError:
        abort(400)
    N = 10
    new_db = []
    for i in db:
        if i['datetime'] > after:
            new_db.append(i)
    return {'messages': new_db[:N]}


@app.route("/show")
def show():
    '''Функция выводит базу данных сервера по эндпоинту /show
    Так как json имеет тип dictionary, возвращаем базу данных как словарь по ключу 'data'
    '''
    return {"data": db}


if __name__ == "__main__":
    app.run(debug=False)
