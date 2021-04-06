import random
import sys
import os
import time 
import json
import requests
import speech_recognition as sr
import pyaudio


def start_game():

    response = requests.get("https://www.randomlists.com/data/words.json")
    choice = random.choice(json.loads(response.text)['data'])
    print(r'''

    ------------
    |          |
    |          |
 /----\  help  |  
| .   .|  /    |      
|  __  |       | 
\------/       |
   |           |
  /|\          |
 / | \         |
  / \          |
 /   \         |
               |  Hangman
               |  by Nathan Lintu
 ----------------------------------
    ''')  # A fun graphic to treat your eyes :)

    print('''Let's play hangman! \nType one letter at a time to try and guess the word or type guess answer to try and guess the full word. 
Beware! If you get the word wrong, you lose!
Type help to view all your previous guesses.
Make sure to press enter after every entry
Good Luck!
    ''')
    word_separation = []
    guessed_letters = []
    lives = 6
    x = 'none'
    reference_list = []
    if 3 <= len(choice) <= 4:
        x = "EASY"

    elif 5 <= len(choice) <= 7:
        x = "MEDIUM"

    elif len(choice) >= 8:
        x = 'HARD'
    underscore_maker(choice, word_separation, reference_list)
    main(lives, word_separation, choice, guessed_letters, reference_list, x)
    return reference_list, x


def game_lose():  # This runs if the user loses the game
    print(r'''

        ------------
        |          |
        |          |
     /----\ I died |  
    | x   x| /     |      
    |  __  |       | 
    \------/       |
       |           |
      /|\          |
     / | \         |
      / \          |
     /   \         |
                   |
                   |
     -----------------------------
        ''')
    print("Do you want to play again?(Say yes or no)")
    user_answer = get_audio()
    answer = user_answer.lower()
    if answer == 'yes':
        start_game()
    elif answer == 'no':
        print("Bye!")
        time.sleep(1)
        sys.exit()
    else:
        print('Input not recognized, please try again.')
        game_lose()


def game_win():  # If the player wins, they are shown the actual word and asked if they want to play again
    print(r'''
     /----\  Thx 4 
    | .   .| saving me     
    |  __  |    
    \------/      
     \ |  /       
      \| /        
       |           
      / \       
     /   \        

        ''')
    print("Do you want to play again?(Say yes or no)")
    answer = get_audio()
    if answer == 'yes':  # sees this: _ _ _ and not this:['_', '_', '_']
        start_game()
    elif answer == 'no':
        print("Bye!")
        time.sleep(1)
        sys.exit()  # Exits the program if the user does not want to play again
    else:
        print("Input not recognized. Please try again.")
        game_win()


# This function turns the letters in
def underscore_maker(choice, word_separation, reference_list):
    for letter in choice:                                       # the word to underscores
        word_separation.append('_ ')
    for letters in choice:
        reference_list.append(letters)


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
        except Exception as e:
            print("Not recognized" + str(e))

        return said


def main(lives, word_separation, choice, guessed_letters, reference_list, x):  # Main game loop
    while True:
        while lives >= 1:
            print(f"Difficulty: {x}")
            print(' '.join(word_separation))
            print("Lives left: " + str(lives) + "\n")
            print(">", end="")
            user_input = get_audio()
            guess = user_input.lower()

            if user_input == 'guess answer':  # This runs if the user wants to guess the full word
                print("Type the whole word here: ", end="")
                challenge = get_audio()

                if challenge.lower() == choice:
                    print("Congratulations! You guessed the right word!")
                    game_win()

                else:
                    print("Sorry, incorrect. The correct word was: " + choice)
                    game_lose()

            if user_input == 'help':  # The following if statements check for special cases when the user guesses a letter/word

                print("These are the letters you guessed: ", end="")
                if len(guessed_letters) == 0:
                    print("None")
                print(' '.join(guessed_letters))
                continue

            modified = guess[7:]
            guessed_letters.append(modified)
            letter_guess = modified.lower()
            print(letter_guess)

            if len(letter_guess) > 1:
                print("Too many letters")
                guessed_letters.pop()
                continue

            if not letter_guess.isalpha():
                print("Letters only. No numbers, decimals, or special characters")
                guessed_letters.pop()
                continue

            if guessed_letters.count(letter_guess) > 1:
                print("Letter already guessed!")
                guessed_letters.pop()
                continue

            if letter_guess not in choice and letter_guess != 'help':
                print("Letter not found!")
                lives -= 1
                # Code logic to match the letter starts here
            # We need to loop the guessed letter against all letters
            for i in range(len(choice)):
                # in the chosen word this is to check for duplicate letters
                if letter_guess in choice[i]:
                    word_separation[i] = letter_guess

            if word_separation == reference_list:  # If the chosen word is same as what got entered,

                print(choice)  # end the game and show the result
                print("You Won!")
                game_win()

            if lives == 0:  # if the lives is 0, stop the game and show the status
                print("Sorry, incorrect. The correct word was: " + choice)
                print("Game over")
                game_lose()


start_game()
