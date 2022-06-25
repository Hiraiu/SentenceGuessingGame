"""
Created on Fri Feb 26 17:21:49 2021

@author: Irina Stroescu 

Python version: 3.8

Encoding: utf-8

This file contains a sentence guessing game that uses as source an English
corpus belonging to the Universal Dependencies project. 

"""

import io
import re
import nltk
import random
from nltk import pos_tag
from nltk import FreqDist
from nltk.text import Text
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from contextlib import redirect_stdout
from nltk.corpus.reader.conll import ConllCorpusReader


def get_len(string):
    """
    Takes as input a string with the encoded sentence and counts how many
    underscores it contains. Returns an int that is the number of words
    to be guessed. 
    
    """
    length = 0
    for word in hidden:
        if word == "_":
            length += 1
    return length


def guess(word, tokenized_sent, position):
    """
    
    Checks if the user's try is the correct word. If it is, it returns its 
    index. If it's not, displays a message.
    
    Parameters
    ----------
    word : str
        A word.
    tokenized_sent : list
        The chosen sentence to guess split into tokens.
    position: int
        The current word of the sentence that the user must guess.
    -------
    Returns
    -------
    result : int
        The index of the correct guessed word.
    
    """
    for element in tokenized_sent:
        if word == tokenized_sent[position]:
                return(position)
        elif word != "?" and word != tokenized_sent[position]:
            return(print("Wrong. Try again."))


def reveal_word(tokenized_sent, position):
    """ 
    Reveals the right word from the position the user is currently at.
    
    """
    return(tokenized_sent[position])


def special_char(tokenized_sent):
    """
    If there is a special character(.,' or -) in any of the words, 
    the function further splits the word having the character as a 
    separator in order to leave the special character unchanged.
    
    Parameters
    ----------
    tokenized_sent : list
        The selected sentence to be guessed split into tokens.

    Returns
    -------
    result : list
        A list with the special character element split into 3 elements. 
        
    """
    special_char_sentence = []
    for word in tokenized_sent:
        if "'" in word:
            word = word.replace("'", "+'+")
            char_word = word.split("+")
            for el in char_word:
                special_char_sentence.append(el.strip())
                
        elif "-" in word:
            word1 = word.replace("-", "+-+")
            char_word1 = word1.split("+")
            for el1 in char_word1:
                special_char_sentence.append(el1.strip())
                
        else:
            special_char_sentence.append(word)
    return special_char_sentence


def hidewords(tokenized_sent):
   '''
   
    Changing the words from the selected sentence to underscores while keeping 
    the digits and punctuation unchanged.
    
    Parameters
    ----------
    tokenized_sent : list
        The selected sentence to be guessed split into tokens.

    Returns
    -------
    result : string
        Returns a string with the encoded sentence.
        
   '''
   hidden_sentence = []
   for word in tokenized_sent:
        if word.isalpha():
            hidden_sentence.append(word.replace(word, "_"))
        else:
            hidden_sentence.append(word.strip())
   return " ".join(hidden_sentence)


def show_hint(word_to_guess, hint, text, tokenized_sent):
    """
    
    Shows hints to the user.

    Parameters
    ----------
    word_to_guess : str
        The current word that the user has to guess. 
    hint: integer
        The number of hints the user is at (the maximum number of hints is 3).
    text : nltk.text.Text
        A corpus as a nltk Text object.
    tokenized_sent : list
        The selected sentence to be guessed split into tokens.

    Returns
    -------
    result : string
        The corresponding hint that the user requested.

    """
    if hint == 1:
        tag = pos_tag(tokenized_sent,tagset = "universal")
        index = [x[0] for x in tag].index(word_to_guess)
        for element in tag:
            if word_to_guess == tag[index][0]:
                pos = tag[index][1]
        return(f"The word has {len(word_to_guess)} letter(s) and it's a {pos}")
    
    elif hint == 2:
        context = get_similar(word_to_guess, text)
        items =[]
        for item in context:
            items.append(item)
        final = ", ".join(items)
        return (f"Some similar words are: {final}")
    
    elif hint == 3:
        letters = []
        for letter in word_to_guess:
            letters.append(letter)
        return (f"First letter is {letters[0]} and the last letter is {letters[-1]}.")
    
    elif hint > 3:
        return ("No more hints left. Try to guess!")
    
def get_similar(word, text):
    """
    Gets words similar to the selected word based on its context in a corpus.

    Parameters
    ----------
    word : str
        A word.
    text : nltk.text.Text
        A corpus as a nltk Text object.

    Returns
    -------
    result : list
        A list of words occuring in similar contexts or an empty list if 
        no results were found.

    """
    with io.StringIO() as f, redirect_stdout(f):
        en_stopwords = set(stopwords.words('english'))
        text.similar(word, num=5)
        result = f.getvalue().replace('\n', ' ').strip(' ').split(' ')
        for element in result:
            if element in en_stopwords:
                result.remove(element)
        if result == ['No', 'matches']:
            result = []
    return result

#extracting the sentences and cleaning the line
sentences = []
with open("en_ewt-ud-train.conllu", encoding = "utf-8") as corpus:
    data = corpus.readlines()
    for line in data:
        if line.startswith("# text"):
            sentences.append(line.replace("\n", "").replace("# text = ","").rstrip())
    

#reading the corpus words
corpus = ConllCorpusReader('./', ['en_ewt-ud-train_preproc.conllu'], 
                            ['ignore', 'words', 'ignore', 'ignore', 
                             'ignore', 'ignore', 'ignore', 'ignore',
                             'ignore', 'ignore'])

text = Text(corpus.words())

#removing the sentences that have more than 20 words or less than 5
shortsen = [line for line in sentences if len(line.split()) >= 5 
            and len(line.split()) <= 20]

#finding the words that appear less than 10 times (rare_words) 
freqs = FreqDist(corpus.words())
rare_words = [word for word, freq in freqs.items() if freq <= 10] 

#removing rare words
tt = TweetTokenizer()
rare_words_dict= {}
for word in rare_words:
    rare_words_dict[word] = True
bad = []
good_sentences =[]
for sent in shortsen:
    tokenized_sents = tt.tokenize(sent)
    is_a_good_sent = True
    for el in tokenized_sents:
        if el in rare_words_dict:
            bad.append(sent)
            is_a_good_sent = False
            break
    if is_a_good_sent:
        good_sentences.append(sent)
        
#lowering the sentences
lower_sents = [element.lower() for element in good_sentences]

#remove duplicates using sets
game_sents = list(set(lower_sents)) 

#removes sentences with underlines that might interfere with the game
for sen in game_sents:
    if re.findall('_+',sen):
        game_sents.remove(sen)

#Picking a random sentence from the preprocessed dataset. 
random_element = random.sample(game_sents, 1)
    
#making the sentence a string
string = ""
for letter in random_element:
    string += letter

#tokenizing the sentence with the help of nltk.tokenize
tokenized_sent= tt.tokenize(string)

#changing the original sentence to display special characters properly
tokenized_sent_special_char = special_char(tokenized_sent)
tokenized_sent = tokenized_sent_special_char

#changing the words to _ keeping the digits and punctuation
hidden = hidewords(tokenized_sent)
    
# Print a welcome message and the number of words in the sentence to the 
#console using underscores but include punctuation and numerical characters.
print("""
Welcome to the guessing game!
You have 5 tries for every word. If you do not guess correctly, the word will be shown and you will get 10 points deducted.
You can ask for a total of 3 hints, but be careful as the hints will affect your final score!
Have fun!
""")
print(f"You have to guess {get_len(hidden)} word(s).\nThe sentence is {hidden}")
score = 0
hint = 0
position = 0
i = 0
words_to_guess = hidewords(tokenized_sent).split()

#get input from user and if the word is correct changes its index (_ form)
while i < 5:
    word = input("Try guessing: ")
#if the word is not one the user needs go guess, move to the next one
    while words_to_guess[position] != "_":
        position +=1
    index = guess(word, tokenized_sent, position)
#if the users asks for a hint for an unknown word, add the attempt to hints
    if word == "?" and words_to_guess[position] == "_":
        hint += 1
        print(show_hint(tokenized_sent[position], hint, text, tokenized_sent))
#if the users inserts the wrong word it sticks to the same word position for 5 tries
#adds the score based on the numbe of hints requested
    if index != "Wrong. Try again." and " " in word:
        print("Please only enter one word!")
    if index != "Wrong. Try again." and index == position:
        print("You guessed correctly! Next one!")
        i = 0
        if hint == 0:
            score += 30
        elif hint == 1:
            score += 20
        elif hint == 2:
            score += 15
        elif hint == 3:
            score += 10
        hint= 0
#moves to the next word after the word has been guessed and reveals the word
        position += 1
        words_to_guess[index] = word
#increases attempts without counting hints
    elif (word != "?"):
        i += 1
        print(f"You have attempted {i} time(s).")
#if user doesn't guess 5 times: shows word, moves to the next one
    if i == 5:
        score -= 10
        hint = 0
        i = 0
        print(f"Maximum tries reached. The word was {reveal_word(tokenized_sent,position)}.")
        words_to_guess[position] = reveal_word(tokenized_sent,position)
        position += 1
    print(" ".join(words_to_guess))
#stops the game if you guessed
    if "_" not in words_to_guess:
        print("\nGame over!")
        print(f"Final score: {score} points.")
        print("See you next time!")
        break  
    