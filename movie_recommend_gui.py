import customtkinter as ctk

import pandas as pd
import numpy as np
import os
import re
import contractions
import emoji
import json

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def readCSV(csvName):
    base_wd = os.getcwd()

    csv_path = os.path.join(base_wd, "data", csvName)

    df = pd.read_csv(csv_path)

    return df

def preprocess_text(text_str: str):

    """
    Remove characters that are not characters of 
        --> a - z
        --> A - Z
        --> 0 - 9
    """

    clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', text_str) 

    # Turns all uppercase alphabets to lowercase
    clean_text = clean_text.lower()

    # Tokenize string of text into individual units
    tokenized_text = word_tokenize(clean_text)

    # Remove stopwords which provide little to none useful information
    stop_words = set(stopwords.words('english'))
    
    filtered_text = [token for token in tokenized_text if token not in stop_words]

    # Lemmatization of tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_text = []

    for token in filtered_text:
        lemmatized_text.append(lemmatizer.lemmatize(token))
    
    # Process contractions (words with apostrophe) by replacing them with words of similar meaning
    expanded_text = [contractions.fix(token) for token in lemmatized_text]

    # Handle emojis and emoticons
    emoji_clean_text = [emoji.demojize(token) for token in expanded_text]

    # Rejoin into a BoW for each token in a movie information
    string_BoW = " ".join(emoji_clean_text)

    return string_BoW

def readBoW_from_file(jsonfile_name):

    base_wd = os.getcwd()
    
    jsonfile_path = os.path.join(base_wd, "data", jsonfile_name)

    if os.path.isfile(jsonfile_path):
        with open(jsonfile_path, 'r') as file:
            bagOfWords = json.load(file)

            return bagOfWords

    else:
        print("\nJson file is not found in directory. Please save it first.")

        return None

def feature_extraction(bagOfWords):
    vectorizer = CountVectorizer()

    vectorizer.fit(bagOfWords)

    # Encode document

    vector = vectorizer.transform(bagOfWords)

    return vector

def index_extraction(similarity_row):

    # Return descending index of the movies
    index = np.argsort(similarity_row)[:][::-1]

    # Return movies sorted with the descending similarity score
    score_series = similarity_row[index]

    return index, score_series

# Check whether user is satisfied with the results or want to see other results
def user_input_loop():
    
    while True:
        print("\nIs this what you are looking for?\n1. Yes\n2. I would like to see other results\nChoice: ");

        user_input = input()

        # Check if user input contains digit
        if (user_input.isdigit() == False):
            print("\nError. You can only enter digits.")
            continue

        user_num = int(user_input)

        match user_num:
            
            case 1:    
                return False;
                
            case 2:
                return True;

            case _:
                print("\nInput incorrect. You can only enter numbers of 1 or 2.\nPlease try again.")

# Preprocess user input and include in boW for similarity calculation
# Returns similarity scores and descending index
def preprocessing_and_similarity_calculation(boW, movie_description):
    # Preprocess user input string
    preprocessed_userInput = preprocess_text(movie_description)

    # Attach user input string into preprocessed BoW
    boW.append(preprocessed_userInput)

    indexOfUserInput = len(boW) - 1

    vector = feature_extraction(boW)

    pairwise_similarity = cosine_similarity(vector, vector)

    similarity_of_inputRow = pairwise_similarity[indexOfUserInput, :-1] # Only the last row similarity and excludes the personal ones

    index, score_series = index_extraction(similarity_of_inputRow)

    return index, score_series

def recommending_movies(movie_description):
    # Read saved preprocessed BagOfWords
    boW = readBoW_from_file("ori_BoW.json")

    index, score_series = preprocessing_and_similarity_calculation(boW, movie_description)

    return index, score_series

def check_moviesName(movie_name_description):
    
    # Read saved preprocessed movie names
    boW = readBoW_from_file("names_BoW.json")

    index, score_series = preprocessing_and_similarity_calculation(boW, movie_name_description)

    return index, score_series

class App():
    def __init__(self, window):
        self.master = window

        self.master.title("Movie Recommender - Animation Movies") 

        self.master.geometry('1200x800') # Set window size
        self.master.configure(fg_color = '#1b1e22') # Set background color 

        # For saving dataset
        self.df = readCSV("cleanedAnimation.csv")

        # For line drawing
        self.canvas = None

        # For result rendering
        self.result_frame = None

        ## For Main Title

        # Create font
        main_title_font = ctk.CTkFont(family="Fixedsys", size=44)

        self.main_title_label = ctk.CTkLabel(self.master, 
                                        width = 200,
                                        height = 40,
                                        text = " Movie Recommender - Animation Movies ",
                                        text_color='white',
                                        corner_radius=20,
                                        font=main_title_font)

        # Declares the position of the main title label with padding of (100, 10)
        self.main_title_label.pack(padx=30, pady=35)

        ## For Buttons to select the program function and exit button
        button_text_font = ctk.CTkFont(family="System", size=31)

        self.button_frame = ctk.CTkFrame(self.master,
                                    fg_color='transparent')

        self.button_frame.pack(padx = 0, pady=0)

        self.button_unpressed_color = "#4b586a"
        self.button_pressed_color = '#4d80d1'

        self.option_button_1 = ctk.CTkButton(self.button_frame, 
                                        width=100,
                                        height= 50,
                                        text="Find a movie via plot description",
                                        fg_color = self.button_unpressed_color,
                                        font=button_text_font,
                                        command=self.button_1_function)

        self.option_button_2 = ctk.CTkButton(self.button_frame, 
                                        width=100,
                                        height= 50,
                                        text="Check a movie via name",
                                        fg_color = self.button_unpressed_color,
                                        font=button_text_font,
                                        command=self.button_2_function)

        self.exit_button = ctk.CTkButton(self.button_frame,
                                    width=100,
                                    height= 50,
                                    text="Exit",
                                    text_color='#cbced2',
                                    fg_color="#4b586a",
                                    font=button_text_font,
                                    command=self.master.destroy)

        self.option_button_1.pack(side = 'left', padx = 10, pady = 30)
        self.option_button_2.pack(side = 'left', padx = 10, pady = 30)
        self.exit_button.pack(side = 'left', padx = 10, pady = 30)
    
    def show_result(self, current_idx, max_movies_per_result, index, score_series):
        
        # If the line has been rendered 
        if self.canvas != None:
            self.canvas.destroy()
        
        if self.result_frame != None:
            self.result_frame.destroy()
        
        # Create a border line
        self.canvas = ctk.CTkCanvas(self.master,
                               width = 1100,
                               height = 50,
                               bg = '#1b1e22',
                               bd = 0,
                               highlightthickness=0)
        
        self.canvas.pack()

        self.canvas.create_line(0, 25, 1100, 25, fill='white', width=1)

        self.result_frame = ctk.CTkFrame(self.master,
                                         width = 1000,
                                         height = 300,
                                         fg_color='transparent')
        
        self.result_frame.pack(padx = 0, pady = 2)

        result_font = ctk.CTkFont(family="System", size = 27)

        current_row = 0

        for i in range(current_idx, max_movies_per_result):
            movie_label = ctk.CTkLabel(self.result_frame,
                                              text = "Movie " + str(i+1) + ". ",
                                              text_color = 'white',
                                              font = result_font)

            movie_name_text = self.df.iloc[index[i]]['Movie Name']

            movie_name = ctk.CTkLabel(self.result_frame,
                                      text = movie_name_text,
                                      text_color = 'white',
                                      font = result_font)
            
            movie_year_text = self.df.iloc[index[i]]['Year']

            movie_year = ctk.CTkLabel(self.result_frame,
                                      text = movie_year_text,
                                      text_color = 'white',
                                      font = result_font)
            
            similarity_percentage_text = str(round(score_series[i] * 100, 2)) + "% " + "similar"

            similarity_percentage = ctk.CTkLabel(self.result_frame,
                                                 text = similarity_percentage_text,
                                                 text_color = 'white',
                                                 font = result_font)

            movie_label.grid(row = current_row, column = 0, padx = 5, pady = 10)
            movie_name.grid(row = current_row, column = 1, padx = 35, pady = 10)
            movie_year.grid(row = current_row, column = 2, padx = 20, pady = 10)
            similarity_percentage.grid(row = current_row, column = 3, padx = 30, pady = 10)

            current_row += 1

    def plot_description_search(self):
        user_string = self.user_entry1.get()

        index, score_series = recommending_movies(user_string)

        current_idx = 0

        self.show_result(current_idx, 5, index, score_series)

    def movie_name_search(self):
        user_string = self.user_entry2.get()

        index, score_series = check_moviesName(user_string)

        current_idx = 0

        self.show_result(current_idx, 5, index, score_series)

    # Function to encapsulate all GUI for predicting movie based on description
    def button_1_function(self):
        
        current_button_color = self.option_button_1.cget("fg_color")
        other_button_color = self.option_button_2.cget("fg_color")

        # If button has not been pressed and color has not changed
        # Other button has also not been pressed
        if (current_button_color == self.button_unpressed_color) and (other_button_color == self.button_unpressed_color):
            
            self.option_button_1.configure(fg_color = self.button_pressed_color)
            
            function1_font = ctk.CTkFont(family="System", size=25)

            self.user_entry1 = ctk.CTkEntry(window,
                                    width=908,
                                    height=100,
                                    placeholder_text="Enter description (genre, year, plot, director, stars):",
                                    font=function1_font)
            
            self.user_entry1.pack(padx = 0, pady = 2)

            self.search_button1 = ctk.CTkButton(window,
                                                width=80,
                                                height=20,
                                               corner_radius=20,
                                               font = function1_font,
                                               text = "Search",
                                               command=self.plot_description_search)
            
            self.search_button1.pack(padx = 100, pady = 4)
        
        # If button has been pressed and color has changed
        # Other button has not been pressed
        if (current_button_color == self.button_pressed_color) and (other_button_color == self.button_unpressed_color):

            self.option_button_1.configure(fg_color = self.button_unpressed_color)

            self.user_entry1.destroy()

            self.search_button1.destroy()

            if self.canvas != None:
                self.canvas.destroy()
                self.canvas = None

            if self.result_frame != None:
                self.result_frame.destroy()
                self.result_frame = None
        
        if (current_button_color == self.button_unpressed_color) and (other_button_color == self.button_pressed_color):

            self.option_button_1.configure(fg_color = self.button_pressed_color)
            self.option_button_2.configure(fg_color = self.button_unpressed_color)

            self.user_entry2.destroy()
            self.search_button2.destroy()

            if self.canvas != None:
                self.canvas.destroy()
                self.canvas = None

            if self.result_frame != None:
                self.result_frame.destroy()
                self.result_frame = None

            function1_font = ctk.CTkFont(family="System", size=25)

            self.user_entry1 = ctk.CTkEntry(window,
                                    width=908,
                                    height=100,
                                    placeholder_text="Enter description (genre, year, plot, director, stars):",
                                    font=function1_font)
            
            self.user_entry1.pack(padx = 0, pady = 2)

            self.search_button1 = ctk.CTkButton(window,
                                                width=80,
                                                height=20,
                                               corner_radius=20,
                                               font = function1_font,
                                               text = "Search",
                                               command=self.plot_description_search)
            
            self.search_button1.pack(padx = 100, pady = 4)

    # Function to encapsulate all GUI for checking movie based on name
    def button_2_function(self):
        current_button_color = self.option_button_2.cget("fg_color")
        other_button_color = self.option_button_1.cget("fg_color")

        # If button has not been pressed and color has not changed
        # Other button has also not been pressed
        if (current_button_color == self.button_unpressed_color) and (other_button_color == self.button_unpressed_color):
            
            self.option_button_2.configure(fg_color = self.button_pressed_color)
            
            function1_font = ctk.CTkFont(family="System", size=25)

            self.user_entry2 = ctk.CTkEntry(window,
                                    width=908,
                                    height=100,
                                    placeholder_text="Enter name of movie to find it:",
                                    font=function1_font)
            
            self.user_entry2.pack(padx = 0, pady = 2)

            self.search_button2 = ctk.CTkButton(window,
                                                width=80,
                                                height=20,
                                               corner_radius=20,
                                               font = function1_font,
                                               text = "Search",
                                               command=self.movie_name_search)
            
            self.search_button2.pack(padx = 100, pady = 4)
        
        # If button has been pressed and color has changed
        # Other button has not been pressed
        if (current_button_color == self.button_pressed_color) and (other_button_color == self.button_unpressed_color):

            self.option_button_2.configure(fg_color = self.button_unpressed_color)

            self.user_entry2.destroy()

            self.search_button2.destroy()

            if self.canvas != None:
                self.canvas.destroy()
                self.canvas = None

            if self.result_frame != None:
                self.result_frame.destroy()
                self.result_frame = None
        
        if (current_button_color == self.button_unpressed_color) and (other_button_color == self.button_pressed_color):

            self.option_button_2.configure(fg_color = self.button_pressed_color)
            self.option_button_1.configure(fg_color = self.button_unpressed_color)

            self.user_entry1.destroy()
            self.search_button1.destroy()

            if self.canvas != None:
                self.canvas.destroy()
                self.canvas = None

            if self.result_frame != None:
                self.result_frame.destroy()
                self.result_frame = None

            function1_font = ctk.CTkFont(family="System", size=25)

            self.user_entry2 = ctk.CTkEntry(window,
                                    width=908,
                                    height=100,
                                    placeholder_text="Enter name of movie to find it:",
                                    font=function1_font)
            
            self.user_entry2.pack(padx = 0, pady = 2)

            self.search_button2 = ctk.CTkButton(window,
                                                width=80,
                                                height=20,
                                               corner_radius=20,
                                               font = function1_font,
                                               text = "Search",
                                               command=self.movie_name_search)
            
            self.search_button2.pack(padx = 100, pady = 4)

if __name__ == "__main__":
    # Window for GUI
    window = ctk.CTk()
    
    application = App(window)

    window.mainloop()