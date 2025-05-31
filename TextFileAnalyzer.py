from BaseFileAnalyzer import BaseFileAnalyzer
import string
from collections import Counter

class TextFileAnalysisResult:
    def __init__(self, total_words, unique_words, most_common, word_locations, word_counts):
        self.total_words = total_words
        self.unique_words = unique_words
        self.most_common = most_common
        self.word_locations = word_locations
        self.word_counts = word_counts

    def to_dict(self):
        return {
            'total_words': self.total_words,
            'unique_words': self.unique_words,
            'most_common': self.most_common,
            'word_locations': self.word_locations,
            'word_counts': self.word_counts
        }
    
    def to_text(self):
        text = f"Total words: {self.total_words}\n"
        text += f"Unique words: {self.unique_words}\n"
        text += "Most common words:\n"
        for word, count in self.most_common:
            text += f"  {word}: {count}\n"
        text += f"Word locations: {self.word_locations}\n"
        text += f"Word counts: {self.word_counts}\n"
        return text

class TextFileAnalyzer(BaseFileAnalyzer):

    def __init__(self, file_path):
        self.file_path = file_path
        self.content = ""
        self.word_counter = None
        self.word_locations = []
        self.word_count = 0

    def load_file(self):
        """טוען את הקובץ ומוודא שהוא קיים."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.content = file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"הקובץ {self.file_path} לא נמצא.")

    def analyze(self):
        """סופר את מספר המילים בקובץ לאחר הסרת סימני פיסוק באמצעות Counter."""
        translator = str.maketrans('', '', string.punctuation)
        cleaned_content = self.content.translate(translator)
        words = cleaned_content.split()
        self.word_counter = Counter(words)
        self.word_count = len(words)

    def search_word(self, word: str):
        """מחפש את כל המיקומים של המילה בקובץ (אחרי ניקוי סימני פיסוק)."""
        translator = str.maketrans('', '', string.punctuation)
        cleaned_content = self.content.translate(translator)
        words = cleaned_content.split()
        self.word_locations = [i for i, w in enumerate(words) if w.lower() == word.lower()]

    def get_result(self) -> TextFileAnalysisResult:
        """מחזיר את התוצאה כאובייקט."""
        most_common = self.word_counter.most_common(5) if self.word_counter else []
        word_counts = dict(self.word_counter) if self.word_counter else {}
        return TextFileAnalysisResult(
            total_words=self.word_count,
            unique_words=len(self.word_counter) if self.word_counter else 0,
            most_common=most_common,
            word_locations=self.word_locations,
            word_counts=word_counts
        )

    def save_result(self, output_path: str):
        """שומר את התוצאה לקובץ טקסט רגיל (לא JSON)."""
        result_obj = self.get_result()
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(result_obj.to_text())