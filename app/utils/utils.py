import random
import string

import nltk
from nltk.corpus import wordnet as wn

from app.settings import AppSettings, get_app_settings

__APP_SETTINGS: AppSettings = get_app_settings()

try:
    wn.synsets("dog")
except LookupError:
    nltk.download("wordnet")


def get_word_lists():
    """
    Retrieves extensive lists of adjectives, nouns, and verbs using the NLTK WordNet corpus.
    Underscores in multiword expressions are removed and words are converted to lowercase.

    Returns:
        tuple: Three lists containing adjectives, nouns, and verbs respectively.
    """
    adjectives = set()
    nouns = set()
    verbs = set()

    # Extract adjectives from WordNet
    for syn in wn.all_synsets("a"):
        for lemma in syn.lemmas():
            word = lemma.name().replace("_", "")
            adjectives.add(word.lower())

    # Extract nouns from WordNet
    for syn in wn.all_synsets("n"):
        for lemma in syn.lemmas():
            word = lemma.name().replace("_", "")
            nouns.add(word.lower())

    # Extract verbs from WordNet
    for syn in wn.all_synsets("v"):
        for lemma in syn.lemmas():
            word = lemma.name().replace("_", "")
            verbs.add(word.lower())

    return list(adjectives), list(nouns), list(verbs)


def generate_password() -> str:
    """
    Generates a random password consisting of letters (both uppercase and lowercase) and digits.
    The password length is determined by the global setting __APP_SETTINGS.pass_length.

    Returns:
        str: A randomly generated password.

    References:
        - Python string module: https://docs.python.org/3/library/string.html
        - Python random module: https://docs.python.org/3/library/random.html
    """
    # Combine all uppercase and lowercase letters with digits into a single string.
    characters = string.ascii_letters + string.digits
    # Generate the password by randomly selecting characters from the combined string.
    # The number of characters selected is defined by __APP_SETTINGS.pass_length.
    return "".join(random.choice(characters) for _ in range(__APP_SETTINGS.pass_length))


def generate_complex_nickname() -> str:
    """
    Generates a complex gaming nickname composed of multiple randomly chosen words and
    appended numbers. The final nickname length is randomly determined to be between 23 and 27 characters.
    Extensive word lists are obtained from the NLTK WordNet corpus to ensure a large variety of unique words.

    Returns:
        str: The generated gaming nickname in lowercase.
    """
    adjectives, nouns, verbs = get_word_lists()

    # Combine all words into a single pool
    word_pool = adjectives + nouns + verbs

    # Choose a random final nickname length between 23 and 27 characters
    final_length = random.randint(23, 27)

    # Generate a list of candidate parts to build the nickname
    candidate_parts = []
    # Generate 15 candidate parts to ensure diversity
    for _ in range(15):
        part = random.choice(word_pool)
        # With a 50% probability, append a random number (from 0 to 99) to the word
        if random.random() < 0.5:
            part += str(random.randint(0, 99))
        candidate_parts.append(part)

    # Shuffle the candidate parts for additional randomness
    random.shuffle(candidate_parts)

    # Construct the nickname by sequentially adding parts until reaching the final length
    nickname = ""
    for part in candidate_parts:
        if len(nickname) + len(part) <= final_length:
            nickname += part
        else:
            # If there's room for only part of the word, add only the required number of characters
            remaining = final_length - len(nickname)
            if remaining > 0:
                nickname += part[:remaining]
            break

    # Ensure the nickname does not exceed the final length and is all in lowercase
    return nickname.lower()
