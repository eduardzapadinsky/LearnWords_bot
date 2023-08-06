import json
import requests
from bs4 import BeautifulSoup


def synonyms(term):
    """
    Parse synonyms of a word.
    Args:
        term (str): The word for which synonyms will be parsed.
    Returns:
        list: A list of synonyms for the given word.
    """

    response = requests.get(f'https://www.thesaurus.com/browse/{term}')
    soup = BeautifulSoup(response.text, 'lxml')
    synonym_words = soup.findAll('a', {'class': 'css-1kg1yv8 eh475bn0'})
    if synonym_words:
        return [span.text for span in synonym_words]  # 'css-1gyuw4i eh475bn0' for less relevant synonyms


def words_by_level(word):
    """
    Check the English learning level of a word.
    Args:
        word (str): The word to check its level.
    Returns:
        str: The level to which the word belongs or an empty string if it is not found.
    """

    with open("data_bases/words_by_levels.json", "r") as file:
        words_level = json.load(file)
    for level, words in words_level.items():
        if word in words:
            return level
    return ""


def word_example(word: str):
    """
    Parse examples of word usage.
    Args:
        word (str): The word for which examples will be parsed.
    Returns:
        list: A list of examples of word usage.
    """

    response = requests.get(f'https://www.thesaurus.com/browse/{word}')
    soup = BeautifulSoup(response.text, 'lxml')
    examples = soup.findAll('div', {'class': 'css-8xzjoe e15rdun50'})
    if len(examples) >= 3:
        return [span.text.replace(f'{word}', f"<b>{word}</b>").replace(f'{word.capitalize()}',
                                                                       f"<b>{word.capitalize()}</b>") for span in
                examples][:3]


def word_audio(word: str):
    """
    Parse audio pronunciation of a word.
    Args:
        word (str): The word for which audio pronunciation will be parsed.
    Returns:
        str: The URL of the audio pronunciation or None if not found.
    """

    response = requests.get(f'https://www.thesaurus.com/browse/{word}')
    soup = BeautifulSoup(response.text, 'lxml')
    audio = soup.find('audio')
    if audio:
        audio = audio.find_all('source')
        return audio[1].get('src')


def word_image(word: str):
    """
    Parse images related to a word.
    Args:
        word (str): The word for which images will be parsed.
    Returns:
        str: The URL of the image or None if not found.
    """

    response = requests.get(
        f'https://www.google.com/search?q={word}&sxsrf=ALiCzsYukfkA2_pfD5ftIegG2FM366slPQ:1665664481802&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjproLem936AhWKraQKHbz-DtkQ_AUoAXoECAEQAw&biw=1536&bih=722&dpr=1.25')
    soup = BeautifulSoup(response.text, 'lxml')
    image = soup.find_all('img')
    return image[1].get('src')
