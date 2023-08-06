from bs4 import BeautifulSoup
import json


def words_parser(level: str) -> list:
    """
    Form a list of words from an HTML file.
    Args:
        level (str): The level for which the words are extracted from the HTML file.
    Returns:
        list: A list of cleaned words extracted from the HTML file.
    """

    with open(rf"C:\Python\TelegramBot\Learn_English_by_levels\HTML\{level}.html", "r") as file:
        src = file.read()
    # Create an instance of the BeautifulSoup class using the 'lxml' parser.
    soup = BeautifulSoup(src, "lxml")
    # Find all words for translation marked with the class "s4".
    words = soup.find_all("p", class_="s4")
    cleaned_words = []
    for cleaned_word in words:
        cleaned_word = cleaned_word.text.split()[0].lower()
        cleaned_words.append(cleaned_word)
    return cleaned_words


# Create a dictionary containing lists of words for each English learning level.
json_dict = {}
levels = ["A1", "A2", "B1", "B2", "C1", "C2"]

for level in levels:
    json_dict[level] = words_parser(level)


# Save the dictionary to a JSON file.
with open(r"C:\Python\TelegramBot\Learn_English_by_levels\words_by_levels.json", "w") as file:
    json.dump(json_dict, file)
