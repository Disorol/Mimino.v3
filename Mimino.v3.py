import datetime
import sys
import csv
import webbrowser
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

    def bot_answer(self, phrase):  # Ответы бота
        phrase = phrase.lower()
        if ('прив' in phrase) or ('здравствуй' in phrase) or ('хай' in phrase) \
                or ('хеллоу' in phrase) or ('здаров' in phrase):
            return choice(['Привет', 'Приветик', 'Здравствуйте', 'Приветствую',
                           'Здравствуй'])
        elif 'время' in phrase or ('котор' in phrase and 'ча' in phrase):
            return str(datetime.datetime.now()).split()[1].split('.')[0]
        elif ('как' in phrase and 'дела' in phrase) or \
                (('чё' in phrase or 'че' in phrase) and 'как' in phrase):
            self.flag_how_are_you = True
            return choice(['Всё в порядке.', 'Просто отлично!', 'Волшебно!',
                           'Феерично!', 'Всё классно.']) + ' А у вас как?'
        elif 'хорошо' in phrase or 'нормально' in phrase or 'тоже' in phrase \
                or 'феерично' in phrase or 'волшебно' in phrase or 'отлично' \
                in phrase or 'классно' in phrase or 'прекрасно' in phrase or \
                ':)' in phrase or 'дельно' in phrase or 'аналогично' in phrase \
                or 'намана' in phrase or 'норм' in phrase or 'живу' in phrase \
                or ('кушать' in phrase and 'хочу' in phrase):
            if self.flag_how_are_you:
                self.flag_how_are_you = False
                return choice(['Я за вас рада!', 'Как же это прекрасно!',
                               'Вот и чудненько!'])
            else:
                return choice(['Что вы имеете ввиду?', 'Что, что?'])
        elif 'плохо' in phrase or 'отвратительно' in phrase or 'ужасно' in \
                phrase or ':(' in phrase or 'плоховато' in phrase or \
                ('так' in phrase and 'себе' in phrase):
            return 'Не беспокойтесь, всё будет хорошо.'
        elif ('завтра' in phrase or 'планируешь' in phrase or 'хочешь' in
              phrase or 'думаешь' in phrase) or ('заняться' in phrase or
                                                 'занимаешься' in phrase
                                                 or 'заниматься' in phrase) \
                and 'чем' in phrase:
            return choice(['Мне охото', 'Я думаю', 'Я планирую', 'Я собираюсь',
                           'Я хочу']) + choice([' отдохнуть на диванчике!',
                                                ' ничего не делать...',
                                                ' дома сидеть', ' пойти гулять',
                                                ' пойти на пробежку',
                                                ' приготовить вкусный ужин',
                                                ' работать над проектом',
                                                ' спать весь день', ' учить PyQT'])
        elif (('как' in phrase or 'какое' in phrase) and
              ('тебя' in phrase or 'ты' in phrase) and (
                      'зовут' in phrase, 'имя' in phrase, 'название' in phrase)) \
                or ('кто' in phrase and 'ты' in phrase):
            return choice(
                ['А как вы думаете?', 'Меня зовут Mimino', 'Я Mimino',
                 'Моё имя Mimino'])
        elif 'мне' in phrase and 'скучно' in phrase:
            return 'Попробуйте ' + choice(['погулять', 'поиграть', 'отдохнуть',
                                           'заняться программированием'])
        elif 'ты' in phrase and 'человек' in phrase:
            return choice(['Нет, я бот', 'Конечно же нет', 'Нет, спасибо',
                           'Нетушки', 'Неа, я не человек'])
        elif ('твой' in phrase and 'создатель' in phrase) or \
                ('кто' in phrase and 'твой' in phrase and 'создатель' in phrase) \
                or ('кто' in phrase and 'тебя' in phrase and 'создал' in phrase):
            return choice(['Disorol', 'Disik', 'Dis', 'Тимур', 'Величайший программист',
                           'Человек']) + choice([', естевственно', ', конечно', ''])
        elif 'мне' in phrase and 'скучно' in phrase:
            return 'Тогда попробуйте ' + choice(['пойти на прогулку', 'поработать',
                                                 'заняться программированием'])
        elif ('рандомн' in phrase or 'случайн' in phrase or 'любо' in phrase) and \
                ('числ' in phrase or 'цифр' in phrase):
            return str(randint(1, int(randint(1, 30) * '9')))
        elif ('рандомн' in phrase or 'случайн' in phrase or 'любо' in phrase) and \
                ('цвет' in phrase or 'квадрат' in phrase):
            self.dr = Drawer()
            self.dr.show()
            return choice(['Держите', 'Вот', 'Вам должно понравиться',
                           'Ваши случайные цвета']) + ', просто кликайте по окну'
        elif 'откр' in phrase or 'включ' in phrase or 'запус' in phrase:
            return self.open_website(phrase)
        elif ('очисти' in phrase or 'почисти' in phrase or 'очисть' in phrase
              or 'почисть' in phrase or 'удали' in phrase) and \
                ('чат' in phrase or 'чата' in phrase or 'историю' in phrase
                 or 'переписку' in phrase or 'переписки' in phrase):
            with open('chat.txt', 'w') as file:
                file.write('')
                return choice(['Готово', 'Всё', 'Держите'
                               ]) + choice([', чистый чат!',
                                            ', чат очищен!'])
        else:
            return 'Простите, я вас не поняла'

    def open_website(self, phrase):  # Открытике сайтов
        run = choice(['Запускаю', 'Включаю', 'Открываю',
                      'Уже открываю', 'Запускаю сайт', 'Нашла', 'Перехожу по ссылке',
                      'Без проблем', 'Ок',
                      'Сайт уже ждёт вас', 'Держите', 'Ой, что-то нашла'])
        if 'http' in phrase:
            p_lst = phrase.split()
            for i in p_lst:
                if 'http' in i:
                    link = i
                    break
            webbrowser.open(link)
            return run
        elif 'ютуб' in phrase or 'ютюб' in phrase or ('you' in phrase and 'tube'
                                                      in phrase):
            webbrowser.open('https://www.youtube.com')
            return run
        elif 'ок' in phrase or 'одноклассник' in phrase or ('ок' in phrase and
                                                            'ру' in phrase) or \
                ('ok' in phrase and 'ru' in phrase):
            webbrowser.open('https://ok.ru')
            return run
        elif 'вк' in phrase or 'vk' in phrase or ('в' in phrase and 'контакте'
                                                  in phrase):
            webbrowser.open('https://vk.com')
            return run
        elif 'переводчик' in phrase or 'translate' in phrase or \
                ('яндекс' in phrase and 'переводчик' in phrase) or (
                'yandex' in phrase and 'translate' in phrase):
            webbrowser.open('https://translate.yandex.ru/?lang=en-ru')
            return run
        elif 'эфир' in phrase or 'видео' in phrase:
            webbrowser.open('https://yandex.ru/portal/video?from=tableau_'
                            'yabro&redircnt=1572685958.1&stream_chann'
                            'el=649&stream_active=storefront')
            return run
        elif 'музыку' in phrase or 'музыка' in phrase or (
                'yandex' in phrase and 'music' in phrase):
            webbrowser.open('https://music.yandex.ru/home')
            return run
        elif 'лицей' in phrase or (
                'yandex' in phrase and 'lyceum' in phrase):
            webbrowser.open('https://lyceum.yandex.ru')
            return run
        elif 'облако' in phrase or ('яндекс' in phrase and 'диск' in phrase) or \
                ('yandex' in phrase and 'disc' in phrase):
            webbrowser.open('https://disk.yandex.ru')
            return run
        elif 'гугл' in phrase or 'google' in phrase:
            webbrowser.open('https://www.google.ru/')
            return 'Конечно, Яндекс лучше, но держите'
        elif 'тимур' in phrase or 'тимура' in phrase or \
                ('disorol' in phrase and 'development' in phrase) or 'дизорол' \
                in phrase:
            webbrowser.open('https://disoroldevelopment.000webhostapp.com/#sl_i4')
            return run
        elif 'yandex' in phrase or 'browser' in phrase or 'яндекс' in phrase \
                or 'браузер' in phrase:
            webbrowser.open('https://yandex.ru')
            return run
        elif 'твиттер' in phrase or 'twitter' in phrase or 'твитер' in phrase \
                or 'twitter' in phrase:
            webbrowser.open('https://twitter.com')
            return run
        elif ('гит' in phrase and 'хаб' in phrase) or ('git' in phrase and 'hub'
                                                       in phrase) or \
                ('гет' in phrase and 'хаб' in phrase):
            webbrowser.open('https://github.com')
            return run


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
