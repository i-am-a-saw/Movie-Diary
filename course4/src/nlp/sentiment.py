from transformers import pipeline

class SentimentAnalyzer:
    def __init__(self):
        self.model = pipeline(
            "sentiment-analysis",
            model="seara/rubert-tiny2-russian-sentiment",
            tokenizer="seara/rubert-tiny2-russian-sentiment"
        )

    def analyze(self, text):
        if not text.strip():
            return "Отрицательный"  # Пустой отзыв считается отрицательным
        result = self.model(text)[0]
        return "Положительный" if result["label"] == "positive" else "Отрицательный"

if __name__ == "__main__":
    analyzer = SentimentAnalyzer()
    print(analyzer.analyze("Мне не очень понравился сюжет, под конец стало совсем скучно"))  # Отрицательный
    print(analyzer.analyze("Фильм хорош, но актеров подобрали не самых лучших. Лучше бы играл Киану Ривз! Сюжет банальный, хотелось бы больше непредсказуемых моментов"))  # Отрицательный