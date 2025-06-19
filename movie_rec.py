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

def readBoW_from_file():

    base_wd = os.getcwd()

    jsonfile_name = "ori_BoW.json"
    
    jsonfile_path = os.path.join(base_wd, "data", jsonfile_name)

    if os.path.isfile(jsonfile_path):
        with open(jsonfile_path, 'r') as file:
            bagOfWords = json.load(file)

            return bagOfWords

    else:
        print("\nJson file is not found in directory. Please save it first.")

        return None

def readMovieNames_from_file():

    base_wd = os.getcwd()

    jsonfile_name = "names_BoW.json"
    
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

    # Take the index of movies of the top 5 similarity score
    index = np.argsort(similarity_row)[-5:][::-1]

    # Take only the top 5 similarity score
    score_series = similarity_row[index]

    return index, score_series

def recommending_movies(movie_description, df):
    # Read saved preprocessed BagOfWords
    boW = readBoW_from_file()
    
    # Preprocess user input string
    preprocessed_userInput = preprocess_text(movie_description)

    # Attach user input string into preprocessed BoW

    boW.append(preprocessed_userInput)

    indexOfUserInput = len(boW) - 1

    vector = feature_extraction(boW)

    pairwise_similarity = cosine_similarity(vector, vector)

    similarity_of_inputRow = pairwise_similarity[indexOfUserInput, :-1] # Only the last row similarity and excludes the personal ones

    index, score_series = index_extraction(similarity_of_inputRow)
    
    print("\n-------------------")
    for i in range(0, len(index)):

        movie_name = df.iloc[index[i]]['movie_name']
        similarity_percentage = score_series[i] * 100

        print(f"{i+1}. {movie_name} | Score: {similarity_percentage:.2f}%")
    print("-------------------\n")

def main():
    run_flag = True

    df = readCSV("cleanedAnimation.csv")

    while run_flag:
        print("\n========================================")
        print("Welcome to The Movie Recomender!")
        print("\nMenu: ")
        print("\t1. Find a movie")
        print("\t2. Does your movie exists in this database?")
        print("\t3. Exit")
        print("\nEnter your choice (1-3): ", end="")

        user_input = input()

        user_num = int(user_input)

        match user_num:
            
            case 1:    
                print("\nEnter the description of a movie that you are searching for: ")
                
                movie_description = input()
                
                recommending_movies(movie_description, df)
                
            case 2:
                pass

            case 3:
                print("\nThank you for your visit.\nHope you have a nice day!")
                run_flag = False

            case _:
                print("\nInput incorrect. You can only enter numbers from 1 - 3.\nPlease try again.")

main()
