import time
import unittest
import requests


class TestApp(unittest.TestCase):
    def test_hello_endpoint(self):
        time.sleep(1)
        response = requests.get('http://127.0.0.1:5000/')
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'Hello, World!')

    def test_health_check_endpoint(self):
        response = requests.get('http://127.0.0.1:5000/hc')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'Healthy'})

    def test_words_endpoint(self):
        input_data = {'text': 'This is a test sentence'}
        response = requests.post('http://127.0.0.1:5000/words', json=input_data)
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'words': ['This', 'is', 'a', 'test', 'sentence']})

    def test_get_sentences_endpoint(self):
        input_data = {'text': 'This is a test sentence. This is another sentence.'}
        response = requests.post('http://127.0.0.1:5000/sentences', json=input_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'sentences': ['This is a test sentence.', 'This is another sentence.']})

        input_data = {'text': 'This is a test sentence? This is another sentence!'}
        response = requests.post('http://127.0.0.1:5000/sentences', json=input_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'sentences': ['This is a test sentence?', 'This is another sentence!']})

    def test_bigrams_endpoint(self):
        input_data = {'text': 'json is what json is not'}
        response = requests.post('http://127.0.0.1:5000/bigrams', json=input_data)
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"bigrams": [{'json is': 2, 'is what': 1, 'what json': 1, 'is not': 1}]})

    def test_regular_sentences(self):
        input_data = {'text': "This is a sentence. And this is another one. The last sentence is here!"}
        response = requests.post('http://127.0.0.1:5000/sentences', json=input_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'sentences': ["This is a sentence.", "And this is another one.", "The last sentence is here!"]})

    def test_initials(self):
        input_data = {'text': "Mr. Johnson and Mrs. Smith went to the party."}
        response = requests.post('http://127.0.0.1:5000/sentences', json=input_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'sentences': ["Mr. Johnson and Mrs. Smith went to the party."]})

    def test_whitespace_after_punctuation(self):
        input_data = {'text': "Hello!  How are you?   I'm fine."}
        response = requests.post('http://127.0.0.1:5000/sentences', json=input_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'sentences': ["Hello!", "How are you?", "I'm fine."]})

    def test_no_whitespace_after_punctuation(self):
        input_data = {'text': "Hello!How are you?I'm fine."}
        response = requests.post('http://127.0.0.1:5000/sentences', json=input_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'sentences': ["Hello!", "How are you?", "I'm fine."]})


if __name__ == '__main__':
    unittest.main()
