from TextFileAnalyzer import TextFileAnalyzer
from JSONFileAnalyzer import JSONFileAnalyzer

def main():
    # נתיבים לדוגמה (שנה לפי מיקום הקבצים אצלך)
    text_path = r"C:\Users\This User\Desktop\מסלול פרונטאנד\שנה ב\Python\hw\project\sample.txt"
    json_path = r"C:\Users\This User\Desktop\מסלול פרונטאנד\שנה ב\Python\hw\project\sample.json"

    # ניתוח קובץ טקסט
    text_analyzer = TextFileAnalyzer(text_path)
    text_analyzer.load_file()
    text_analyzer.analyze()
    text_analyzer.search_word("python")  # דוגמה למילה לחיפוש
    text_result = text_analyzer.get_result()
    print("Text file analysis:")
    print(text_result)
    text_analyzer.save_result("text_result.json")

    print("\n----------------------\n")

    # ניתוח קובץ JSON
    json_analyzer = JSONFileAnalyzer(json_path)
    json_analyzer.load_file()
    json_analyzer.analyze()
    json_analyzer.search_word("article", field="body")  # דוגמה למילה לחיפוש בשדה מסוים
    json_result = json_analyzer.get_result()
    print("JSON file analysis:")
    print(json_result)
    json_analyzer.save_result("json_result.json")

if __name__ == "__main__":
    main()