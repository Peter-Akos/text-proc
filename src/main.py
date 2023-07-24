from flask import Flask, jsonify, request
import re
from nltk import word_tokenize
from nltk.util import ngrams
from collections import Counter
from pysbd import Segmenter

NEWLINES_RE = re.compile(r"\n{2,}")  # two or more "\n" characters


def split_paragraphs(input_text: str = ""):
    """
    Splits the input text into paragraphs and returns them in an array
    :param input_text: the string that we want to split
    :return: list[str]
    """
    no_newlines = input_text.strip("\n")  # remove leading and trailing "\n"
    split_text = NEWLINES_RE.split(no_newlines)  # regex splitting

    paragraphs = [p for p in split_text if p.strip()]
    # p.strip() == True if paragraph has other characters than whitespace

    return paragraphs


def get_most_common_bigrams(text: str, n: int = 5):
    """
    Returns a dictionary of the n most common bigrams that are present in the text.
    :param text:
    :param n: how many values should the function return
    :return:
    """
    # Tokenize the text into words
    words = word_tokenize(text.lower())

    # Generate bi-grams from the list of words
    bi_grams = list(ngrams(words, 2))

    # Count the occurrences of each bi-gram
    bi_gram_counts = Counter(bi_grams)

    # Get the n most common bi-grams
    most_common_bigrams = bi_gram_counts.most_common(n)
    # print(most_common_bigrams)
    ret = {}

    for bigram in most_common_bigrams:
        t = bigram[0][0] + " " + bigram[0][1]
        ret[t] = bigram[1]
        # print(bigram)

    # print(ret)

    return [ret]


app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


@app.get('/hc')
def check():
    return {'status': 'Healthy'}


@app.route('/words', methods=['POST'])
def get_words():
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({'error': 'Invalid JSON data or missing "text" field'}), 400

    text = data['text']
    words = text.split()

    return jsonify({'words': words})


@app.route('/sentences', methods=['POST'])
def get_sentences():
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({'error': 'Invalid JSON data or missing "text" field'}), 400

    text = data['text']
    segmenter = Segmenter(language='en', clean=True)
    pysbd_res = segmenter.segment(text)
    print(pysbd_res)

    return jsonify({'sentences': pysbd_res})


@app.route('/paragraphs', methods=['POST'])
def get_paragraphs():
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({'error': 'Invalid JSON data or missing "text" field'}), 400

    text = data['text']
    paragraphs = split_paragraphs(text)

    return jsonify({'paragraphs': paragraphs})


@app.route('/bigrams', methods=['POST'])
def get_bigrams():
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({'error': 'Invalid JSON data or missing "text" field'}), 400

    text = data['text']
    bigrams = get_most_common_bigrams(text, n=5)
    print(bigrams)

    return {'bigrams': bigrams}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
