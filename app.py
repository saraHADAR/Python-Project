from flask import Flask, request, jsonify
from TextFileAnalyzer import TextFileAnalyzer
from JSONFileAnalyzer import JSONFileAnalyzer
import os

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_file():
    file = request.files.get('file')
    search_word = request.form.get('search_word', None)

    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    temp_path = os.path.join('temp_' + filename)
    file.save(temp_path)

    try:
        if ext == '.txt':
            analyzer = TextFileAnalyzer(temp_path)
        elif ext == '.json':
            analyzer = JSONFileAnalyzer(temp_path)
        else:
            return jsonify({'error': 'Unsupported file type'}), 400

        analyzer.load_file()
        analyzer.analyze()
        if search_word:
            analyzer.search_word(search_word)
        result = analyzer.get_result()
        if hasattr(result, 'to_dict'):
            result = result.to_dict()
        return jsonify(result)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == '__main__':
    app.run(debug=True)