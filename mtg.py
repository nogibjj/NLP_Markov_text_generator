import random
import numpy as np

# Backoff to n-1, n-2, ... 1-grams if n-grams are not found
def backoff(last_n_words, n, corpus):
    try:
        # Get n-grams
        words = np.array([])
        freqs = np.array([])
        for i in range(len(corpus)-n): # -n because we need n words to make an n-gram
            if corpus[i:i+n-1] == last_n_words: # -1 because we don't want to include the last word
                if np.isin(corpus[i+n-1], words) == False: # If the word is not already in the list
                    words = np.append(words, corpus[i+n-1]) # Add the word
                    freqs = np.append(freqs, 1) # Add a count of 1
                else:
                    freqs[words == corpus[i+n-1]] += 1 # If the word is already in the list, add 1 to its count
        return words, freqs # Return the words and their counts

    except:
        last_n_words_in_corpus = backoff(last_n_words, n-1, corpus) # If n-grams are not found, backoff to n-1-grams
    return last_n_words_in_corpus

# Finish a sentence with n-grams
def finish_sentence(tokens, n, corpus, deterministic): 
    
    for i in range(10):
        last_n_words = tokens[-(n-1):] # Get the last n-1 words
        last_n_words_in_corpus, freqs = backoff(last_n_words, n, corpus) # Get the n-grams that start with the last n-1 words
        if deterministic:
            next_words = last_n_words_in_corpus[np.argmax(freqs)] # Get the word with the highest count
        else:
            next_words = random.choice(last_n_words_in_corpus) # Get a random word
        tokens.append(next_words)
        if next_words in ['.', '!', '?']: # If the word is a punctuation mark, stop
            break
        elif len(tokens) == 10: # If the sentence is 10 words long, stop
            break

    return tokens