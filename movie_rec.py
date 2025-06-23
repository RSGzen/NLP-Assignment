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

def printResults(index, score_series, df):
    
    print("\n-------------------")
    for i in range(0, len(index)):

        movie_name = df.iloc[index[i]]['Movie Name']
        similarity_percentage = score_series[i] * 100

        print(f"{i+1}. {movie_name} | Score: {similarity_percentage:.2f}%")
    print("-------------------")

def recommending_movies(movie_description, df):
    # Read saved preprocessed BagOfWords
    boW = readBoW_from_file("ori_BoW.json")
    
    index, score_series = preprocessing_and_similarity_calculation(boW, movie_description)

    num_results = 5

    printResults(index[0:5], score_series[0:5], df)
    
    while True:
        loop_check = user_input_loop()
        
        if (loop_check):
            num_results += 5

            # If reaches the end of the dataset
            if (num_results > 100):
                print("\nReached end of results")
                break

            printResults(index[num_results-5: num_results], score_series[num_results-5: num_results], df)

        else:
            break

def check_moviesName(movie_name_description, df):
    
    # Read saved preprocessed movie names
    boW = readBoW_from_file("names_BoW.json")

    index, score_series = preprocessing_and_similarity_calculation(boW, movie_name_description)
    
    num_results = 5

    printResults(index[0:5], score_series[0:5], df)
    
    while True:
        loop_check = user_input_loop()
        
        if (loop_check):
            num_results += 5

            # If reaches the end of the dataset
            if (num_results > 100):
                print("\nReached end of results")
                break
            
            printResults(index[num_results-5: num_results], score_series[num_results-5: num_results], df)

        else:
            break

def main():
    run_flag = True

    df = readCSV("cleanedAnimation.csv")

    while run_flag:
        print("\n========================================")
        print("Welcome to The Movie Recomender!")
        print("\nMenu: ")
        print("\t1. Find a movie via description")
        print("\t2. Check movies available via description")
        print("\t3. Exit")
        print("\nEnter your choice (1-3): ", end="")

        user_input = input()

        # Check if user input contains digit
        if (user_input.isdigit() == False):
            print("\nError. You can only enter digits.")
            continue

        print("\n========================================")
        
        user_num = int(user_input)

        match user_num:
            
            case 1:    
                print("\nEnter the description of a movie that you are searching for: ")
                
                movie_description = input()
                
                recommending_movies(movie_description, df)
                
            case 2:
                print("\nEnter the description of a movie that you are searching for: ")
                
                movie_name_description = input()

                check_moviesName(movie_name_description, df)

            case 3:
                print("\nThank you for your visit.\nHope you have a nice day!")
                run_flag = False

            case _:
                print("\nInput incorrect. You can only enter numbers from 1 - 3.\nPlease try again.")

main()
