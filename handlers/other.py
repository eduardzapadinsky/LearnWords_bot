import json
import requests
from bs4 import BeautifulSoup


def synonyms(term):
    """Парсинг синонімів"""
    response = requests.get(f'https://www.thesaurus.com/browse/{term}')
    soup = BeautifulSoup(response.text, 'lxml')
    # soup.find('section', {'class': 'css-17ofzyv e1ccqdb60'})
    synonym_words = soup.findAll('a', {'class': 'css-1kg1yv8 eh475bn0'})
    if synonym_words:
        return [span.text for span in synonym_words]  # 'css-1gyuw4i eh475bn0' for less relevant synonyms


def words_by_level(word):
    """Перевірка, до якого рівня англійської належить слово"""
    with open(r"C:\Python\TelegramBot\Learn_English_by_levels\words_by_levels.json", "r") as file:
        words_level = json.load(file)
    for level, words in words_level.items():
        if word in words:
            return level
    return ""


def word_example(word: str):
    """Парсинг прикладів"""
    response = requests.get(f'https://www.thesaurus.com/browse/{word}')
    soup = BeautifulSoup(response.text, 'lxml')
    examples = soup.findAll('div', {'class': 'css-8xzjoe e15rdun50'})
    if len(examples) >= 3:
        return [span.text.replace(f'{word}', f"<b>{word}</b>").replace(f'{word.capitalize()}',
                                                                       f"<b>{word.capitalize()}</b>") for span in
                examples][:3]


def word_audio(word: str):
    """Парсинг озвучки"""
    response = requests.get(f'https://www.thesaurus.com/browse/{word}')
    soup = BeautifulSoup(response.text, 'lxml')
    audio = soup.find('audio')
    if audio:
        audio = audio.find_all('source')
        return audio[1].get('src')


def word_image(word: str):
    """Парсинг зображень"""
    response = requests.get(
        # f'https://www.google.com/search?q={word}&tbm=isch&tbs=itp:animated&hl=uk&sa=X&ved=0CAQQpwVqFwoTCLjo_-z53_oCFQAAAAAdAAAAABAD&biw=1519&bih=722')
        f'https://www.google.com/search?q={word}&sxsrf=ALiCzsYukfkA2_pfD5ftIegG2FM366slPQ:1665664481802&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjproLem936AhWKraQKHbz-DtkQ_AUoAXoECAEQAw&biw=1536&bih=722&dpr=1.25')
    soup = BeautifulSoup(response.text, 'lxml')
    image = soup.find_all('img')
    return image[1].get('src')
