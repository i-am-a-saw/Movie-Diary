from pymongo import MongoClient
from datetime import datetime
import base64
from PIL import Image
import io

class Database:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["movie_diary"]
        self.reviews = self.db["reviews"]

    def save_review(self, movie_title, review_text, sentiment, cover_path):
        with open(cover_path, "rb") as f:
            cover_data = base64.b64encode(f.read()).decode("utf-8")
        review = {
            "movie_title": movie_title,
            "review_text": review_text,
            "sentiment": sentiment,
            "cover_data": cover_data,
            "created_at": datetime.utcnow()
        }
        self.reviews.insert_one(review)

    def get_all_reviews(self):
        return list(self.reviews.find().sort("created_at", -1))

    def search_reviews(self, query):
        return list(self.reviews.find({"movie_title": {"$regex": query, "$options": "i"}}))

    def filter_reviews(self, sentiment):
        return list(self.reviews.find({"sentiment": sentiment}))

if __name__ == "__main__":
    db = Database()
    db.save_review("Оппенгеймер", "Отличный фильм!", "Положительный", "cover.jpg")
    print(db.get_all_reviews())