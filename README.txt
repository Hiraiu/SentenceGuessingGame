Sentence Guessing Game

This file contains a sentence guessing game written in Python 3.8.

Necessary libraries
- io
- re 
- nltk
- random

Packages to install for running the code:
- nltk.download('punkt')
- nltk.download('averaged_perceptron_tagger')
- nltk.download('universal_tagset')
*In order to install them, open your Python interpretor, import the nltk library and run the above commands once.

Files needed to run the game:
"en_ewt-ud-train.conllu" - the sentences are extracted from this file
'en_ewt-ud-train_preproc.conllu' - the words are extracted from this file

Game Mechanics:
The game starts with a message containing some brief instructions, followed by the encoded sentence that must be guessed.
Each word from the sentence is replaced by an underscore, however, punctuation and numbers remain unchanged. 
For every word, the user has 5 tries, if he/she didn't guessed after 5 tries, the word will be revealed and 10 points will be 
deducted from the final score. The user can request up to 3 hints. The first hint is the POS tag and the length of the word.
The second hint contains up to 5 words from similar contexts. The third hint reveals the first and last letter of the word.
Hints do not count as attempts.
If the sentence has been guessed, the game stops and displays the final score.
** Mentions: In order to guess contractions(like I've) and compound words(separated by -) one must guess the word before 
the special character and the word after the special character.

Scoring system:
+ 30 points if the word was guessed within the 5 attemps
+ 20 points if the word was guessed after one hint
+ 15 points if the word was guessed after two hints
+ 10 points if the word was guessed after three hints
- 10 points for each word not guessed

Steps to play:
- set the working directory into the folder where the contents of the archive were extracted
- open the file main.py in your Python interpreter
- run the code


Credit:
Universal Dependencies Project

Author:
Irina Stroescu - stroescu@uni-potsdam.de