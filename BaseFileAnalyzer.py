# מגדירה איזה פעולות צריכים לבצע
from abc import ABC, abstractmethod

# 	טעינת הקובץ – יש לבדוק שהקובץ קיים 
class BaseFileAnalyzer(ABC):
    
    @abstractmethod
    def load_file(self):
        pass
    
    # 	ספירת מס' המילים בקובץ – יש להסיר תחילה את סימני הפיסוק וכד' (translate) 
    @abstractmethod
    def analyze(self):
        pass

# 	חיפוש מילה בקובץ – כל המיקומים של המילה בקובץ (re)
    @abstractmethod
    def search_word(self, word: str):
        pass

# בקבצי JSON המילה המבוקשת מופיע במבנה של שם שדה:מילה מבוקשת, יש לחפש את המילה בשדה המבוקש.
    @abstractmethod
    def get_result(self) -> dict:
        pass

# 	החזרת נתוני הקובץ
    @abstractmethod
    def save_result(self, output_path: str):
        pass
