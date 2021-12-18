from PyQt5 import QtWidgets, QtCore
import client
import requests
from datetime import datetime


class MessengerApp(QtWidgets.QMainWindow, client.Ui_MainWindow):
    '''Класс MessengerApp используется для описания мессенждера.

        Objects
        _______
        QtWidgets.QMainWindow
            Объект QMainWindow из библиотеки QtWidgets
        client.Ui_MainWindow
            Класс Ui_MainWindow из файла client.py

        Attributes
        __________
        host : str
            локал-хост компьютера, на котором находится сервер

        Methods
        __________
        send_message()
            Отправляет сообщения.
        get_messages()
            Выводит сообщения на экран.
        '''
    def __init__(self, host='http://127.0.0.1:5000'):
        super().__init__()
        self.setupUi(self) # вызываем для того, чтобы настроить приложение
        self.host = host
        self.pushButton.pressed.connect(self.send_message) # кнопка
        # Каждые 1000 мс запускаем get_messages:
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_messages)
        self.timer.start(1000)

        self.after = 0

    def send_message(self):
        '''Метод для отправки сообщения каждый раз, когда нажимается кнопка "Отправить".
        Считывает имя и сообщения из ячеек в окне приложения, отправляет post-запрос на сервер по эндпоинту /send

        ________
        Exeption
            Обработка исключения при отключении сервера.
        '''
        name = self.textEdit.toPlainText() # имя считывается из первой ячейки ввода
        message = self.textEdit_2.toPlainText() # сообщение считывается из второй ячейки ввода
        try:
            # отправляем post-запрос на сервер:
            r = requests.post(self.host + '/send', json={"name": name, "msg": message})
        except requests.exceptions.ConnectionError: # если сервер недоступен
            self.textBrowser.append('Сервер временно не отвечает')
            return
        self.textEdit_2.clear() # очищаем поле ввода

    def get_messages(self):
        '''Метод добавляет все сообщения из базы в текстовое поле.
        Отправляет get-запрос на сервер по эндпоинту /receive.

        ________
        Exeption
            Обработка исключения при отключении сервера.
        '''
        try:
            # отправляем get-запрос на сервер:
            r = requests.get(self.host + '/receive', params={"after": self.after})
        except requests.exceptions.ConnectionError:
            self.textBrowser.append('Сервер временно не отвечает')
            return
        dbase = r.json()
        if len(dbase['messages']) > 0:
            self.after = dbase['messages'][-1]['datetime']
            print(r.text)
        for i in dbase['messages']:
            self.textBrowser.append(datetime.fromtimestamp(i['datetime']).strftime('%d.%m.%Y %H:%M:%S'))
            self.textBrowser.append(i['name'])
            self.textBrowser.append(i['msg'])
            self.textBrowser.append('\n')
            self.textBrowser.append('___________________________')
            self.textBrowser.append('\n')


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MessengerApp()
    #отображаем приложение:
    window.show()
    app.exec()
