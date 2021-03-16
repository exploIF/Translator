import requests
from bs4 import BeautifulSoup
import sys

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'}
languages = ('all', 'arabic', 'german', 'english', 'spanish', 'french', 'hebrew', 'japanese', 'dutch', 'polish', 'portuguese', 'romanian', 'russian', 'turkish')


def writing(first_language, word, i, my_file):
    soup = send_request(first_language, languages[i], word.lower())
    translated_words = searching_translations(soup, word)
    translated_examples = searching_examples(soup, word)
    print()
    print('{} Translations:'.format(languages[i].capitalize()))
    print(translated_words)
    print('{} Examples:'.format(languages[i].capitalize()))
    print(translated_examples)
    my_file.write('\n{} Translations:\n'.format(languages[i].capitalize()))
    my_file.write(translated_words)
    my_file.write('\n{} Examples:\n'.format(languages[i].capitalize()))
    my_file.write(translated_examples + '\n')


def send_request(l_1, l_2, word):
    url = 'https://context.reverso.net/translation/' + l_1 + '-' + l_2 + '/' + word
    try:
        r = requests.get(url, headers=HEADERS)
    except ConnectionError:
        print("Something wrong with your internet connection")
        exit()
    else:
        return BeautifulSoup(r.content, 'html.parser')


def searching_translations(soup, word):
    try:
        translations = soup.find_all('a', {'class': 'translation'})
        if not translations:
            raise ValueError("Sorry, unable to find {}".format(word))
    except ValueError as e:
        print(e)
        exit()
    else:
        translated = []
        for t in translations:
            ted = t.text.strip()
            translated.append(ted + '\n')
        del translated[0]
        return "".join(translated[:1])


def searching_examples(soup, word):
    try:
        examples = soup.find_all('div', {'class': 'example'})
        if not examples:
            raise ValueError("Sorry, unable to find {}".format(word))
    except ValueError as e:
        print(e)
        exit()
    else:
        exampled = []
        for e in examples:
            eed = e.text.strip()
            eed = eed.replace('[', '')
            eed = eed.replace(']', '')
            eed = eed.replace('\n\n\n\n\n          ', ":\n")
            exampled.append(eed)
        return "\n\n".join(exampled[:1])


def translating(language_1, language_2, word):
    first_language = languages[language_1]
    my_file = open('{}.txt'.format(word), 'w', encoding='UTF-8')

    if language_2 == 0:
        for i in range(1, len(languages)):
            if languages[i] == first_language:
                continue
            else:
                writing(first_language, word, i, my_file)
    else:
        writing(first_language, word, language_2, my_file)

    my_file.close()


# for running as a script from cli

def main():
    args = sys.argv
    first_language_m = args[1]
    second_language_m = args[2]
    try:
        first = languages.index(first_language_m)
    except ValueError:
        print("Sorry, the program doesn't support {}".format(first_language_m))
        exit()
    try:
        second = languages.index(second_language_m)
    except ValueError:
        print("Sorry, the program doesn't support {}".format(second_language_m))
        exit()
    else:
        word_m = args[3]
        translating(first, second, word_m)


"""""
For running as a program

def main():
    language_1 = int(input(
        "Hello, you're welcome to the translator. Translator supports:\n1. Arabic\n2. German\n3. English\n4. Spanish\n5. French\n6. Hebrew\n7. Japanese\n8. Dutch\n9. Polish\n10. Portuguese\n11. Romanian\n12. Russian\n13. Turkish\n"))
    language_2 = int(input("Type the number of language you want to translate to or '0' to translate to all languages:\n"))
    word = input("Type the word you want to translate: ")
    translating(language_1, language_2, word)
    """""


if __name__ == '__main__':
    main()

