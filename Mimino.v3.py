import datetime
import sys
import webbrowser
from numpy import exp, array, random, dot
from random import choice, randint
import pyttsx3
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QLabel, QLineEdit, \
    QGridLayout, QCheckBox, QApplication, QWidget, QPushButton


class Bot(QWidget):  # y = 21, x = 63
    def __init__(self):
        self.flag_voice = True
        self.flag_how_are_you = False
        self.flag_q = False
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 500, 420)
        self.setFixedSize(500, 420)
        self.setWindowTitle('Mimino')

        for _ in range(4):
            coord_x = 0
            for __ in range(2):
                coord_y = 0
                for ___ in range(26):
                    self.frame = QLabel(self)
                    self.frame.setText("|")
                    self.frame.move(5 + coord_x, 59 + coord_y)
                    coord_y += 11
                coord_x += 485

        coord_y = 0
        for _ in range(2):
            coord_x = 0
            for __ in range(487):
                self.frame = QLabel(self)
                self.frame.setText(".")
                self.frame.move(5 + coord_x, 51 + coord_y)
                coord_x += 1
            coord_y += 285

        self.output_text = QLabel(self)
        self.output_text.setText(' ' * 63)
        self.output_text.move(70, 30)
        self.output_text.setWordWrap(True)

        self.layout = QGridLayout()
        self.layout.addWidget(self.output_text, 0, 0)
        self.setLayout(self.layout)

        self.cb = QCheckBox('Озвучивать фразы Mimino', self)
        self.cb.move(7, 25)
        self.cb.resize(150, 20)
        self.cb.toggle()
        self.cb.stateChanged.connect(self.changeTitle)

        self.input_text = QLineEdit(self)
        self.input_text.move(5, 370)
        self.input_text.resize(380, 20)

        self.send = QPushButton('Отправить', self)
        self.send.resize(104, 22)
        self.send.move(390, 369)

        self.send.clicked.connect(self.input_func)

    def input_func(self):  # Вводная функция
        inp_txt = self.input_text.text()
        if len(inp_txt) > 63:
            self.output_text.setText('- Ваше сообщение не может превышать 63 символа!')
            if self.flag_voice:
                self.send.setEnabled(False)
                engine = pyttsx3.init()
                engine.say('- Ваше сообщение не может превышать 63 символа!')
                engine.runAndWait()
                self.send.setEnabled(True)
        else:
            answer = self.bot_answer(inp_txt)
            inp_txt = ''.join(['\n', 'U: ', inp_txt, '\n', 'M: ', answer])
            with open('Chat.txt', 'a') as file:
                file.write(inp_txt)
            with open('Chat.txt', 'r') as file:
                read_txt = file.read().split('\n')
            if len(read_txt) > 21:
                reversed(read_txt)
                read_txt = read_txt[(len(read_txt) - 21):]
                reversed(read_txt)
            self.output_text.setText('\n'.join(read_txt))
            if self.flag_voice:
                self.send.setEnabled(False)
                engine = pyttsx3.init()
                engine.say(answer)
                engine.runAndWait()
                self.send.setEnabled(True)

    def changeTitle(self, state):  # Голос бота - вкл/выкл
        if state == Qt.Checked:
            self.flag_voice = True
        else:
            self.flag_voice = False

    def bot_answer(self, ph):  # Ответы бота
        ph = ph.lower()
        if ('прив' in ph) or ('здравствуй' in ph) or ('хай' in ph) \
                or ('хеллоу' in ph) or ('здаров' in ph):
            return choice(['Привет', 'Приветик', 'Здравствуйте', 'Приветствую',
                           'Здравствуй'])
        elif 'время' in ph or ('котор' in ph and 'ча' in ph):
            return str(datetime.datetime.now()).split()[1].split('.')[0]

        elif 'дата' in ph or ('какой' in ph and 'день' in ph):
            return '.'.join(str(datetime.datetime.now()).split()[0].split('-'))
        elif ('как' in ph and 'дела' in ph) or \
                (('чё' in ph or 'че' in ph) and 'как' in ph):
            self.flag_how_are_you = True
            return choice(['Всё в порядке.', 'Просто отлично!', 'Волшебно!',
                           'Феерично!', 'Всё классно.']) + ' А у вас как?'
        elif 'хорошо' in ph or 'нормально' in ph or 'тоже' in ph \
                or 'феерично' in ph or 'волшебно' in ph or 'отлично' \
                in ph or 'классно' in ph or 'прекрасно' in ph or \
                ':)' in ph or 'дельно' in ph or 'аналогично' in ph \
                or 'намана' in ph or 'норм' in ph or 'живу' in ph \
                or ('кушать' in ph and 'хочу' in ph):
            if self.flag_how_are_you:
                self.flag_how_are_you = False
                return choice(['Я за вас рада!', 'Как же это прекрасно!',
                               'Вот и чудненько!'])
            else:
                return choice(['Что вы имеете ввиду?', 'Что, что?'])
        elif 'плохо' in ph or 'отвратительно' in ph or 'ужасно' in \
                ph or ':(' in ph or 'плоховато' in ph or \
                ('так' in ph and 'себе' in ph):
            return 'Не беспокойтесь, всё будет хорошо.'
        elif ('завтра' in ph or 'планируешь' in ph or 'хочешь' in
              ph or 'думаешь' in ph) or ('заняться' in ph or
                                         'занимаешься' in ph
                                         or 'заниматься' in ph) \
                and 'чем' in ph:
            return choice(['Мне охото', 'Я думаю', 'Я планирую', 'Я собираюсь',
                           'Я хочу']) + choice([' отдохнуть на диванчике!',
                                                ' ничего не делать...',
                                                ' дома сидеть', ' пойти гулять',
                                                ' пойти на пробежку',
                                                ' приготовить вкусный ужин',
                                                ' работать над проектом',
                                                ' спать весь день', ' учить PyQT'])
        elif (('как' in ph or 'какое' in ph) and
              ('тебя' in ph or 'ты' in ph) and (
                      'зовут' in ph, 'имя' in ph, 'название' in ph)) \
                or ('кто' in ph and 'ты' in ph):
            return choice(
                ['А как вы думаете?', 'Меня зовут Mimino', 'Я Mimino',
                 'Моё имя Mimino'])
        elif 'мне' in ph and 'скучно' in ph:
            return 'Попробуйте ' + choice(['погулять', 'поиграть', 'отдохнуть',
                                           'заняться программированием'])
        elif 'ты' in ph and 'человек' in ph:
            return choice(['Нет, я бот', 'Конечно же нет', 'Нет, спасибо',
                           'Нетушки', 'Неа, я не человек'])
        elif ('твой' in ph and 'создатель' in ph) or \
                ('кто' in ph and 'твой' in ph and 'создатель' in ph) \
                or ('кто' in ph and 'тебя' in ph and 'создал' in ph):
            return choice(['Disorol', 'Disik', 'Dis', 'Тимур', 'Величайший программист',
                           'Человек']) + choice([', естевственно', ', конечно', ''])
        elif 'мне' in ph and 'скучно' in ph:
            return 'Тогда попробуйте ' + choice(['пойти на прогулку', 'поработать',
                                                 'заняться программированием'])
        elif ('рандомн' in ph or 'случайн' in ph or 'любо' in ph) and \
                ('числ' in ph or 'цифр' in ph):
            return str(randint(1, int(randint(1, 30) * '9')))
        elif ('рандомн' in ph or 'случайн' in ph or 'любо' in ph) and \
                ('цвет' in ph or 'квадрат' in ph):
            self.dr = Drawer()
            self.dr.show()
            return choice(['Держите', 'Вот', 'Вам должно понравиться',
                           'Ваши случайные цвета']) + ', просто кликайте по окну'
        elif 'откр' in ph or 'включ' in ph or 'запус' in ph:
            return self.open_website(ph)
        elif '//' in ph:
            try:
                ph = ph.split()
                ph.remove('//')
                return self.another_commands(ph)
            except Exception:
                return 'Возникла непредвиденная ошибка'
        elif ('очисти' in ph or 'почисти' in ph or 'очисть' in ph
              or 'почисть' in ph or 'удали' in ph) and \
                ('чат' in ph or 'чата' in ph or 'историю' in ph
                 or 'переписку' in ph or 'переписки' in ph):
            with open('chat.txt', 'w') as file:
                file.write('')
                return choice(['Готово', 'Всё', 'Держите'
                               ]) + choice([', чистый чат!',
                                            ', чат очищен!'])
        else:
            with open('The answers.csv', 'r') as file:
                read_answers = file.read().split('\n')
            for i in read_answers:
                if ph == i.split(';')[0]:
                    return i.split(';')[1]
            with open('Unknown phrases.txt', 'a') as file:
                file.write(ph + '\n')
            return 'Простите, я вас не поняла'

    def open_website(self, ph):  # Открытике сайтов
        run = choice(['Запускаю', 'Включаю', 'Открываю',
                      'Уже открываю', 'Запускаю сайт', 'Нашла', 'Перехожу по ссылке',
                      'Без проблем', 'Ок',
                      'Сайт уже ждёт вас', 'Держите', 'Ой, что-то нашла'])
        if 'http' in ph:
            p_lst = ph.split()
            for i in p_lst:
                if 'http' in i:
                    link = i
                    break
            webbrowser.open(link)
            return run
        elif 'ютуб' in ph or 'ютюб' in ph or ('you' in ph and 'tube'
                                              in ph):
            webbrowser.open('https://www.youtube.com')
            return run
        elif 'ок' in ph or 'одноклассник' in ph or ('ок' in ph and
                                                    'ру' in ph) or \
                ('ok' in ph and 'ru' in ph):
            webbrowser.open('https://ok.ru')
            return run
        elif 'вк' in ph or 'vk' in ph or ('в' in ph and 'контакте'
                                          in ph):
            webbrowser.open('https://vk.com')
            return run
        elif 'переводчик' in ph or 'translate' in ph or \
                ('яндекс' in ph and 'переводчик' in ph) or (
                'yandex' in ph and 'translate' in ph):
            webbrowser.open('https://translate.yandex.ru/?lang=en-ru')
            return run
        elif 'эфир' in ph or 'видео' in ph:
            webbrowser.open('https://yandex.ru/portal/video?from=tableau_'
                            'yabro&redircnt=1572685958.1&stream_chann'
                            'el=649&stream_active=storefront')
            return run
        elif 'музыку' in ph or 'музыка' in ph or (
                'yandex' in ph and 'music' in ph):
            webbrowser.open('https://music.yandex.ru/home')
            return run
        elif 'лицей' in ph or (
                'yandex' in ph and 'lyceum' in ph):
            webbrowser.open('https://lyceum.yandex.ru')
            return run
        elif 'облако' in ph or ('яндекс' in ph and 'диск' in ph) or \
                ('yandex' in ph and 'disc' in ph):
            webbrowser.open('https://disk.yandex.ru')
            return run
        elif 'гугл' in ph or 'google' in ph:
            webbrowser.open('https://www.google.ru/')
            return 'Конечно, Яндекс лучше, но держите'
        elif 'тимур' in ph or 'тимура' in ph or \
                ('disorol' in ph and 'development' in ph) or 'дизорол' \
                in ph:
            webbrowser.open('https://disoroldevelopment.000webhostapp.com/#sl_i4')
            return run
        elif 'yandex' in ph or 'browser' in ph or 'яндекс' in ph \
                or 'браузер' in ph:
            webbrowser.open('https://yandex.ru')
            return run
        elif 'твиттер' in ph or 'twitter' in ph or 'твитер' in ph \
                or 'twitter' in ph:
            webbrowser.open('https://twitter.com')
            return run
        elif ('гит' in ph and 'хаб' in ph) or ('git' in ph and 'hub'
                                               in ph) or \
                ('гет' in ph and 'хаб' in ph):
            webbrowser.open('https://github.com')
            return run
        else:
            return 'Такого я, к сожалению ' + choice(['открыть', 'запустить', 'включить']) + ' не могу'

    def another_commands(self, ph):
        if 'e-n' in ph:
            training_set_inputs = array([[0, 0, 1], [1, 1, 1], [1, 0, 1], [0, 1, 1]])
            training_set_outputs = array([[0, 1, 1, 0]]).T
            random.seed(1)
            synaptic_weights = 2 * random.random((3, 1)) - 1
            for iteration in range(10000):
                output = 1 / (1 + exp(-(dot(training_set_inputs, synaptic_weights))))
                synaptic_weights += dot(training_set_inputs.T, (training_set_outputs - output) * output * (1 - output))
            return str(1 / (1 + exp(-(dot(array([1, 0, 0]), synaptic_weights)))))
        elif 'cl-ph' in ph:
            with open('Unknown phrases.txt', 'w') as file:
                file.write('')
            return choice(['Готово', 'Всё', 'Держите'
                           ]) + choice([', память очищена',
                                        ', новых слов нет'])
        elif 'cl-ans' in ph:
            with open('The answers.csv', 'w') as file:
                file.write('')
            return choice(['Готово', 'Всё', 'Держите']) + ', файл очищен'
        elif 'wr-ans' in ph:
            try:
                del ph[0]
                with open('The answers.csv', 'a') as file:
                    file.write(' '.join(ph) + '\n')
                return choice(['Готово', 'Всё']) + ', ответ записан'
            except Exception:
                return 'Возникла непредвиденная ошибка'
        else:
            return choice(['Простите', 'Извините', 'Прошу прощения']) + ', но такой команды не существует'


class Drawer(QWidget):  # Рандомный цвет
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setMouseTracking(True)
        self.coords_ = []
        self.qp = QPainter()
        self.fg = False
        self.status = None

    def drawf(self):
        self.fg = True
        self.update()

    def paintEvent(self, event):
        if self.fg:
            self.qp = QPainter()
            self.qp.begin(self)
            self.draw()
            self.qp.end()

    def draw(self):
        self.qp.setBrush(QColor(randint(1, 255), randint(1, 255), randint(1, 255)))
        self.qp.drawRect(45, 45, 200, 200)

    def initUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.setFixedSize(300, 300)
        self.setWindowTitle('Случайный цвет')

        self.just = QLabel(self)
        self.just.setText("Просто кликайте по окну")
        self.just.move(80, 10)

    def mousePressEvent(self, event):
        self.drawf()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Bot()
    ex.show()
    sys.exit(app.exec())
