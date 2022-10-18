from bs4 import BeautifulSoup
import json


def words_parser(level: str) -> list:
    """Формування списку слів з html файлу"""
    with open(rf"C:\Python\TelegramBot\Learn_English_by_levels\HTML\{level}.html", "r") as file:
        src = file.read()
    # Створюємо екземпляр класу, передаємо швидкий парсер
    soup = BeautifulSoup(src, "lxml")
    # Шукаємо всі слова для перекладу
    words = soup.find_all("p", class_="s4")
    cleaned_words = []
    for cleaned_word in words:
        cleaned_word = cleaned_word.text.split()[0].lower()
        cleaned_words.append(cleaned_word)
    return cleaned_words


# Формування словнику зі списками по всім рівням вивчення англійської
json_dict = {}
json_dict["A1"] = words_parser("A1")
json_dict["A2"] = words_parser("A2")
json_dict["B1"] = words_parser("B1")
json_dict["B2"] = words_parser("B2")
json_dict["C1"] = words_parser("C1")
json_dict["C2"] = words_parser("C2")

# Зберігання словника в файл json
with open(r"C:\Python\TelegramBot\Learn_English_by_levels\words_by_levels.json", "w") as file:
    json.dump(json_dict, file)

# import bs4.element
# import requests
# body = soup.body
# print(body)
# p_text = soup.find_all("p")


# words = soup.find("p", class_="s4")

# words_2 = soup.find_all("p", style="padding-left: 27pt;text-indent: 0pt;text-align: left;")


# def find_dictionary_sentences(word: bs4.element.Tag):
#     next_word = word.find_next_siblings()[:7]
#     # print(next_word)
#     for one_word in next_word:
#         if one_word.text == "Dictionary examples:":
#             ind = next_word.index(one_word)
#             dictionary_sentences = next_word[ind + 1].text
#             print(dictionary_sentences)
#             return dictionary_sentences
#     return ""


# for word in words:
#     single_word = word.text.split()[0]
#     cleaned_sentences = find_dictionary_sentences(word)
#     if cleaned_sentences:
#         cleaned_sentences = cleaned_sentences.replace("\n    ", " ")
#     words_dict[single_word] = cleaned_sentences
#
# print(words_dict)
# print("What's she talking about? I've got a book about\n    Jung.".replace("\n    ", " "))
# next_next_word = next_word.f

# print(type(next_word))
# print(next_word[1].text)
# print([i.text for i in words_2])
# HOST = r"C:\Python\TelegramBot\Learn_English_by_levels\HTML\A1.html"
# URL = r"C:\Python\TelegramBot\Learn_English_by_levels\HTML\A1.html"
# HEADERS = {
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
# }
#
#
# def get_html(url, params=''):
#     r = requests.get(url, headers=HEADERS, params=params)
#     return r
#
#
# def get_content(html):
#     soup = BeautifulSoup(html, 'html.parser')
#
#     words = []
#     # p = '<p data-testid="location-date" class="css-p6wsjo-Text eu5v0x0">'
#     # a = '<a class ="css-1bbgabe"'
#     # p = '<p class="s1"'
#     for item in soup.select("body"):
#         # full_data = item.a.get_text(strip=True)
#         words.append(
#             {
#                 'time': item.p.get_text(strip=True),  # Name parsing.
#                 # 'time': item.a.get_text(strip=True),  # Name parsing.
#                 # 'url': f"https://www.olx.ua{item.find('a')['href']}",  # Name parsing.
#             }
#         )
#     return words
#
#
# html = get_html(URL)
# content = get_content(html.text)
# print(content)
