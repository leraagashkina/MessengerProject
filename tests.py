import unittest
from datetime import datetime
from server import prediction
from server import hello_world
from server import status


class predictionTest(unittest.TestCase):
    def test_1(self):
        self.assertIn('Hi', prediction('Hi', 'Lera')['msg'])

    def test_2(self):
        self.assertEqual(prediction('Hi', 'Lera')['name'], 'Lera')

    def test_3(self):
        answers = ["Вы находитесь на верном пути.",
                   "Прилив энергии поможет Вам справиться с большим объемом незапланированных работ.",
                   "Пришло время действовать!", "Терпение! Вы почти у цели.",
                   "Пришло время закончить старое и начать новое.",
                   "Цель определяет успех.", "Вас ожидают перемены.", "Ждите перемен.",
                   "Звезды к вам благосклонны.", "Вы — на верном пути!"]
        self.assertIn(prediction('Hi', 'Lera')['msg'].split('\n\n')[1], answers)


class helloworldTest(unittest.TestCase):
    def test4(self):
        self.assertEqual(hello_world(), '<p>Hello, User!</p>')


class statusTest(unittest.TestCase):
    def test5(self):
        self.assertEqual(status()['number_of_users'], 0)

    def test6(self):
        self.assertEqual(status()['name'], 'My first messenger')

    def test7(self):
        self.assertEqual(status()['time'], datetime.now().strftime('%d.%m.%Y %H:%M:%S'))


if __name__ == "__main__":
    unittest.main()
