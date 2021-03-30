import numpy as np
import re

# build vocabulary

def get_word_embedding(vocab_size = 999999999, file = 'glove.6B.50d_shortened.txt'):
    '''
    Builds embedding dictionary of word -> numerical vector.
    :param vocab_size: The maximum number of words to be added into the dictionary before it stops. The function get embeddings from the beginning of the file onward.
    :param file: A string which contains the path to the file containing embeddings. (e.g. directory/directory/file_name.extention).
    :return: The embedding dictionary.
    '''


    embedding = {}

    with open(file, encoding="utf8") as file:
        i = 0
        for line in file:
            if i >= vocab_size:
                break
            values = line.split()

            word = values[0]

            coefs = np.asarray(values[1:], dtype='float32')

            embedding[word] = coefs

            i += 1
    return embedding


def embed_string(text: str, embedding: dict, max_words: int):
    '''
    Converts a string into an array where each word has been replaced by its value pair in a provided dictionary. Punctuations count as words. Case is ignored.
    :param text: The string which will be embedded.
    :param embedding: The dictionary such that string -> 1D numerical vector
    :param max_words: the maximum number of words in the output. If max_words is reached, no more words are embedded nor added to the output. If max_words is not reached, then zero vecotrs are padded.
    :return: A 2D array with vectors given by the provided embedding.
    '''
    # Get dimension of word vectors
    # There must be a better way of acomplishing this
    vector_dim = 0
    for _, value in embedding.items():
        vector_dim = len(value)
        break

    
    # 2D array which holds word vectors
    word_vectors = np.zeros((max_words, vector_dim))

    # For each word in the input text, place a vector representation of it into the
    # 'word_vectors' array
    # If an word is not contained in the embedding, it is embedded as a vector with all zeros
    skipped_words = 0
    for i, word in enumerate(re.split("(\\W)", text)):
            # Stop embedding words after the maximum words have been embedded
            if i - skipped_words == max_words:
                break
            
            if word in " ":
                skipped_words += 1
                continue
            
            word_vectors[i- skipped_words] = embedding.get(word.lower(), np.zeros(shape = (vector_dim,), dtype='float32'))

    return word_vectors

def embed_strings(strings: list, embedding: dict, max_words: int):
    '''
    Creates a 3D array of word-vector sentences.
    :param text: The strings which will be embedded.
    :param embedding: The dictionary such that string -> 1D numerical vector
    :param max_words: The maximum number of words in a sentence. If max_words is reached, no more words are embedded nor added to the output. If max_words is not reached, then zero vecotrs are padded. Punctuations count as words.
    :return: A 3D array with sentenses containing words represented by numerical vectors.
    '''

    vector_dim = 0
    for _, value in embedding.items():
        vector_dim = len(value)
        break

    sentences = np.ndarray(shape = (len(strings), max_words, vector_dim))

    for i, string in enumerate(strings):

        sentences[i] = embed_string(string, embedding, max_words)

    return sentences






