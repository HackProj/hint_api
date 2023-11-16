import random
import time
import argparse
import pickle

from typing import List
from glob import glob


def tokenize(text: str) -> List[str]:
    """
    :param text: Takes input sentence
    :return: tokenized sentence
    """
    for punctuation in r'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~':
        text = text.replace(punctuation, ' ' + punctuation + ' ')
    t = text.split()
    return t


def get_ngrams(n: int, tokens: list) -> list:
    """
    :param n: n-gram size
    :param tokens: tokenized sentence
    :return: list of ngrams ((previous words), word to predict)
    """
    tokens = (n - 1) * ['<blank>'] + tokens
    list_of_ngrams = [(tuple([tokens[i - p - 1] for p in reversed(range(n - 1))]), tokens[i]) for i in
                      range(n - 1, len(tokens))]
    return list_of_ngrams


class n_gram_model(object):

    def __init__(self, n):
        self.n = n
        self.context = {}  # candidates list related to context
        self.ngram_counter = {}  # amount of time each ngram appeared in the text

    def update(self, sentence: str) -> None:
        """
        Add new text to the model
        :param sentence: input text
        """
        n = self.n
        ngrams = get_ngrams(n, tokenize(sentence))
        for ngram in ngrams:
            if ngram in self.ngram_counter:
                self.ngram_counter[ngram] += 1.0
            else:
                self.ngram_counter[ngram] = 1.0

            prev_words, target_word = ngram
            if prev_words in self.context:
                self.context[prev_words].append(target_word)
            else:
                self.context[prev_words] = [target_word]

    def prob(self, context, token):
        """
        Probability calculation of a candidate to be generated in particular context
        :return: conditional probability
        """
        try:
            count_of_token = self.ngram_counter[(context, token)]
            count_of_context = float(len(self.context[context]))
            result = count_of_token / count_of_context
        except KeyError:
            result = 0.0
        return result

    def get_token(self, context):
        """
        Select next word for sequence
        :param context:
        :return:
        """
        r = random.random()
        probabilities = {}
        try:
            token_of_interest = self.context[context]
        except KeyError:
            if '<blank>' in context:
                raise Exception(
                    f'Please, use prefixes with length >= {self.n - 1}. It bases on amount of grams in the model')
            else:
                raise Exception(
                    f"Your prefix wasn't found in grams dictionary, try another or reduce ngrams")
        for token in token_of_interest:
            probabilities[token] = self.prob(context, token)
        s = 0
        for token in sorted(probabilities):
            s += probabilities[token]
            if s > r:
                return token

    def fit(self, path):
        """
        :param path: path to texts folder
        :return: -
        """
        paths = glob(path + '/*')
        for txt_path in paths:
            with open(txt_path, 'r', encoding='utf8') as f:
                text = f.read()
                text = text.split('.')
                for sentence in text:
                    sentence += '.'
                    self.update(sentence)

    def generate(self, token_count: int, context=''):
        """
        :param context: initial context
        :param token_count: amount of words to generate
        :return: generated text
        """
        n = self.n
        context_queue = (n - 1) * ['<blank>']
        res = []
        if context:
            tc = tokenize(context)  # [-n + 1:]
            res = tc.copy()
            tc = tc[-n + 1:]
            for i in range(len(tc)):
                context_queue[i] = tc[i]
        for _ in range(token_count):
            obj = self.get_token(tuple(context_queue))
            res.append(obj)
            if n > 1:
                context_queue.pop(0)
                if obj == '.':
                    context_queue = (n - 1) * ['<blank>']
                else:
                    context_queue.append(obj)
        return ' '.join(res)
