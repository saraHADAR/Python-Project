from BaseFileAnalyzer import BaseFileAnalyzer
from collections import Counter
import re
import json
import string

class JSONFileAnalyzer(BaseFileAnalyzer):
    def __init__(self, file_path):
        self.file_path = file_path
        self.content = None
        self.word_counter = Counter()
        self.word_count = 0
        self.word_locations = []

    def load_file(self):
        """טוען את הקובץ JSON ומוודא שהוא קיים."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.content = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"הקובץ {self.file_path} לא נמצא.")
        except json.JSONDecodeError:
            raise ValueError(f"הקובץ {self.file_path} אינו קובץ JSON תקין.")

    def analyze(self):
        """סופר את מספר המילים בקובץ JSON ומחשב את המילים הנפוצות."""
        texts = []
        if isinstance(self.content, dict):
            for value in self.content.values():
                if isinstance(value, str):
                    texts.append(value)
        elif isinstance(self.content, list):
            for item in self.content:
                if isinstance(item, dict):
                    for value in item.values():
                        if isinstance(value, str):
                            texts.append(value)
        # הסרת סימני פיסוק וספירת מילים
        all_text = ' '.join(texts)
        translator = str.maketrans('', '', string.punctuation)
        cleaned_content = all_text.translate(translator)
        words = cleaned_content.split()
        self.word_counter = Counter(words)
        self.word_count = len(words)

    def search_word(self, word: str, field: str = None):
        """מחפש את כל המיקומים של המילה בשדה מסוים (או בכל השדות) בקובץ JSON."""
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        self.word_locations = []
        if isinstance(self.content, dict):
            for key, value in self.content.items():
                if isinstance(value, str):
                    for m in pattern.finditer(value):
                        self.word_locations.append({'field': key, 'start': m.start(), 'end': m.end()})
        elif isinstance(self.content, list):
            for idx, item in enumerate(self.content):
                if isinstance(item, dict):
                    for key, value in item.items():
                        if isinstance(value, str):
                            for m in pattern.finditer(value):
                                self.word_locations.append({'item': idx, 'field': key, 'start': m.start(), 'end': m.end()})

    def get_result(self) -> dict:
        """מחזיר את התוצאה כקובץ JSON."""
        most_common = self.word_counter.most_common(5) if self.word_counter else []
        return {
            'total_words': self.word_count,
            'unique_words': len(self.word_counter),
            'most_common': most_common,
            'word_locations': self.word_locations
        }

    def save_result(self, output_path: str):
        """שומר את התוצאה לקובץ JSON."""
        result = self.get_result()
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(result, file, ensure_ascii=False, indent=4)