import openai
import random
import os
import ast

characters_dict = {}
characters_list = []
character = ""
hint_count = 3
lst_hints = []
is_done = False
previous_questions = {}


def clear_terminal():
    if os.name == 'nt':
        _ = os.system('cls') 
    else:
        _ = os.system('clear') 




def universe_picker():

    openai.api_key = #enter your openai API here.
    user_message = input("From which universe you want to get your characters from: ")
    print("It can take up to 20 seconds to load the game!")
    system_message = "Return a dictionary where the keys are the 25 most popular characters from the specified media (e.g., book, movie, series, game) or real life organization. Each key should map to a list of three descriptive strings which are just one words about the corresponding character. These strings should be clues of varying difficulty: the first string being the most abstract or challenging, and the last one being the most straightforward or revealing. This gradation helps in maintaining the guessing game aspect without giving away direct spoilers about the characters. Please ensure that the response strictly adheres to the dictionary format, as any deviation might disrupt the downstream processing of the data. And also please do not use any special characters in character names. Just use space. Note: The media source is represented as '{}'.".format(user_message)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Replace with your desired model
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
        )

        # Print the response
        return response.choices[0].message['content']



    except Exception as e:
        print(f"An error occurred: {e}")


def random_character_picker():
    global character
    global characters_list
    global characters_dict
    try:
        characters_list = list(characters_dict)
    except:
        print("Error converting dict to list!")

    character = characters_list[random.randrange(0, len(characters_list))]




def start_game():
    global characters_dict
    global is_done
    characters_dict = ast.literal_eval(universe_picker())
    print(characters_dict)
    clear_terminal()
    random_character_picker()
    while is_done == False:
        try:
            input_text = "enter 1 for asking a question about the character\nenter 2 to guess the character\nenter 3 to get hints\nPlease indicate what do you want to do: "
            print("*" * 51)
            user_input = input(input_text)
            print("*" * 51)
        except:
            print("You have done something wrong please try again!")
        if user_input == "1":
            questions(character)
        elif user_input == "2":
            if guess(character) == True:
                is_done = True
            else:
                pass
        elif user_input == "3":
            get_hint(character)
        else:
            clear_terminal()
            text = "Please enter only 1, 2 or 3!"
            print("*" * len(text))
            print(text)
            print("*" * len(text))


def get_hint(character_input):
    input_from_user = eval(input("There is 3 hints! Which one do you want to get?\n1, 2 or 3: "))
    clear_terminal()
    print("*" * 51)
    print("Here is your hint = {}".format(characters_dict[character][input_from_user - 1]))

def questions(character_input):
    clear_terminal()
    openai.api_key = #enter your openai API here.
    system_message = "answer the question based on this character = {}, and also just is yes or no. if the question is not answerable with yes or no warn the user saying this question is not a yes or no question. And also do not spoil the character, the user is going to guess the character. And please just use yes or no as answer.".format(character_input)
    user_message= input("Please enter your question: ")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Replace with your desired model
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
        )

        clear_terminal()
        print("*" * 51)
        print("The answer of your question '{}' is = {}".format(user_message, response.choices[0].message['content']))

        previous_questions[user_message] = response.choices[0].message['content']

    except Exception as e:
        print(f"An error occurred: {e}")


def guess(character_input):
    clear_terminal()
    choices = random.sample(characters_list, 3)
    choices.append(character_input)
    random.shuffle(choices)
    index_of_correct_answer = choices.index(character_input)
    labels = ["1-)", "2-)","3-)","4-)"]
    for i in range(4):
        print("{} {}".format(labels[i], choices[i]))


    user_input = input("Please select your answer\nenter 1,2,3 or 4: ")
    if user_input == str((index_of_correct_answer + 1)):
        clear_terminal()
        print("Congrulations you got it correct!")
        return True
    else:
        clear_terminal()
        print("sorry it is wrong, try again!")
        return False




start_game()
