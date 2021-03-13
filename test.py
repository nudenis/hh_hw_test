import unittest
import requests
import json

from config import ACCESS_TOKEN, URL


class MyTestCase(unittest.TestCase):
    authorization = f"Bearer {ACCESS_TOKEN}"

    def test_the_connection_auth(self):
        headers = {'Authorization': self.authorization}
        response = requests.get(URL, headers=headers)
        assert response.ok, "Используемый токен не является валидным"

    def test_not_valid_auth(self):
        headers = {'Authorization': 'not valid auth TOKEN'}
        response = requests.get(URL, headers=headers)
        assert response.status_code == 403, "Некорректный TOKEN вернул ответ, который не ожидался"

    def test_smth_text_in_request_is_correct(self):
        texts = ["javascript", "", True, "''", 123123, " asdauygsu dfs", {"asd": 123}]
        headers = {'Authorization': self.authorization}
        for text in texts:
            response = requests.get(f"{URL}?text={text}", headers=headers)
            assert response.status_code // 100 == 2, f"Ошибка со текстом {text}"

    def test_word_in_first_vacancy_name(self):
        word = 'javascript'
        headers = {'Authorization': self.authorization}
        response = requests.get(f"{URL}?text={word}", headers=headers)
        assert word in response.json()['items'][0]['name'].lower(), f"Слово {word} не содержится в первой вакансии"

    def test_text_in_all_items_name(self):
        word = 'python'
        headers = {'Authorization': self.authorization}
        response = requests.get(f"{URL}?text={word}", headers=headers)
        for item in response.json()['items']:
            assert word not in json.dumps(item,
                                          ensure_ascii=False).lower(), f"Не все вакансии в своём описании содержат " \
                                                                       f"слово: {word} "

    def test_not_valid_text(self):
        text = 'йцукен12345'
        headers = {'Authorization': self.authorization}
        response = requests.get(f"{URL}?text={text}", headers=headers)
        assert len(response.json()['items']) == 0, f"Предположительно неверный запрос (text=йцукен12345) дал результат"


if __name__ == '__main__':
    unittest.main()
