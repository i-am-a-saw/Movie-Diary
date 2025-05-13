from src.ui.main_window import MainWindow
from src.nlp.sentiment import SentimentAnalyzer
from src.database.db import Database
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
import sys

class MovieDiaryApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow()
        self.analyzer = SentimentAnalyzer()
        self.db = Database()

        # Подключение сигналов
        self.window.submit_button.clicked.connect(self.submit_review)
        self.window.cover_button.clicked.connect(self.choose_cover)
        self.window.search_input.textChanged.connect(self.search_reviews)
        self.window.filter_positive.clicked.connect(lambda: self.filter_reviews("Положительный"))
        self.window.filter_negative.clicked.connect(lambda: self.filter_reviews("Отрицательный"))

        self.load_reviews()

    def choose_cover(self):
        file_path, _ = QFileDialog.getOpenFileName(self.window, "Выбрать обложку", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.window.cover_path = file_path

    def submit_review(self):
        title = self.window.title_input.text()
        review = self.window.review_input.toPlainText()
        if not title or not review or not self.window.cover_path:
            QMessageBox.warning(self.window, "Ошибка", "Заполните все поля и выберите обложку")
            return

        sentiment = self.analyzer.analyze(review)
        self.db.save_review(title, review, sentiment, self.window.cover_path)
        self.window.add_review_card(title, review, sentiment, self.db.get_all_reviews()[0]["cover_data"])
        self.window.title_input.clear()
        self.window.review_input.clear()
        self.window.cover_path = None

    def load_reviews(self):
        for i in reversed(range(self.window.scroll_layout.count())):
            self.window.scroll_layout.itemAt(i).widget().deleteLater()
        for review in self.db.get_all_reviews():
            self.window.add_review_card(
                review["movie_title"], review["review_text"], review["sentiment"], review["cover_data"]
            )

    def search_reviews(self):
        query = self.window.search_input.text()
        for i in reversed(range(self.window.scroll_layout.count())):
            self.window.scroll_layout.itemAt(i).widget().deleteLater()
        for review in self.db.search_reviews(query):
            self.window.add_review_card(
                review["movie_title"], review["review_text"], review["sentiment"], review["cover_data"]
            )

    def filter_reviews(self, sentiment):
        for i in reversed(range(self.window.scroll_layout.count())):
            self.window.scroll_layout.itemAt(i).widget().deleteLater()
        for review in self.db.filter_reviews(sentiment):
            self.window.add_review_card(
                review["movie_title"], review["review_text"], review["sentiment"], review["cover_data"]
            )

    def run(self):
        self.window.show()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    app = MovieDiaryApp()
    app.run()