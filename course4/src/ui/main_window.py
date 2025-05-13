from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QPushButton, QScrollArea, QLabel, QFileDialog
from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtGui import QPixmap
from .styles import GLASSMORPH_STYLE
import base64
from io import BytesIO
from PIL import Image

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Дневник кинофильмов")
        self.setStyleSheet(GLASSMORPH_STYLE)
        self.setMinimumSize(800, 600)

        # Главный контейнер
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)

        # Форма ввода
        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Название фильма")
        self.review_input = QTextEdit()
        self.review_input.setPlaceholderText("Ваш отзыв")
        self.cover_button = QPushButton("Выбрать обложку")
        self.submit_button = QPushButton("Добавить отзыв")
        input_layout.addWidget(self.title_input)
        input_layout.addWidget(self.review_input)
        input_layout.addWidget(self.cover_button)
        input_layout.addWidget(self.submit_button)

        # Поиск и фильтрация
        filter_widget = QWidget()
        filter_layout = QHBoxLayout(filter_widget)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по названию")
        self.filter_positive = QPushButton("Положительные")
        self.filter_negative = QPushButton("Отрицательные")
        filter_layout.addWidget(self.search_input)
        filter_layout.addWidget(self.filter_positive)
        filter_layout.addWidget(self.filter_negative)

        # Лента фильмов
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)

        main_layout.addWidget(input_widget)
        main_layout.addWidget(filter_widget)
        main_layout.addWidget(self.scroll_area)
        self.setCentralWidget(main_widget)

        self.cover_path = None

    def add_review_card(self, movie_title, review_text, sentiment, cover_data):
        card = QWidget()
        card.setObjectName("card")
        card_layout = QHBoxLayout(card)

        # Обложка
        cover_label = QLabel()
        img = Image.open(BytesIO(base64.b64decode(cover_data)))
        img = img.resize((100, 150), Image.LANCZOS)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        pixmap = QPixmap()
        pixmap.loadFromData(buffer.getvalue())
        cover_label.setPixmap(pixmap)
        card_layout.addWidget(cover_label)

        # Текст
        text_widget = QWidget()
        text_layout = QVBoxLayout(text_widget)
        title_label = QLabel(movie_title)
        review_label = QLabel(review_text)
        review_label.setWordWrap(True)
        sentiment_label = QLabel(sentiment)
        text_layout.addWidget(title_label)
        text_layout.addWidget(review_label)
        text_layout.addWidget(sentiment_label)
        card_layout.addWidget(text_widget)

        self.scroll_layout.addWidget(card)

        # Анимация появления
        anim = QPropertyAnimation(card, b"opacity")
        anim.setDuration(500)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.start()