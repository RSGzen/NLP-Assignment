import time
import nltk
import unicodedata
import os

def preprocess_txt(text):
    # Convert text to lowercase

    # Normalize unicode characters to ASCII
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')

    ## Replace punctuations
    text = text.replace(".", "") # Full stop
    text = text.replace(",", "") # Comma
    text = text.replace(":", " ") # Colon
    text = text.replace(";", "") # Semicolon
    text = text.replace("?", " ") # Question mark
    text = text.replace("(", "") # Round bracket start
    text = text.replace(")", "") # Round bracket end
    text = text.replace("[", "") # Square bracket start
    text = text.replace("]", "") # Square bracket end
    text = text.replace("'", "") # Apostrophe
    text = text.replace(")", "") # Exclamation mark
    text = text.replace("-", " ") # Hyphen
    text = text.replace("/", " ") # Slash
    text = text.replace("$", "") # Dollar sign

    return text

nltk.download('punkt_tab')

from nltk.tokenize import word_tokenize

current_wd = os.getcwd()
data_file_address = os.path.join(current_wd, "data")

if not os.path.isdir(data_file_address):
    os.mkdir(data_file_address)

raw_file_name = r"raw_sentences.txt"
output_file_name = r"tokens.txt"

raw_file_address = os.path.join(data_file_address, raw_file_name)
output_file_address = os.path.join(data_file_address, output_file_name)

start = time.time()
print("Starting to tokenize. Please wait patiently.......")

with open(raw_file_address, 'r', encoding='utf_8') as raw_file:

    with open(output_file_address, 'a', encoding='utf_8') as output_file:   

        for txt_line in raw_file:
            if txt_line == None:
                continue

            standardized_text = preprocess_txt(txt_line)
            tokenized_text = word_tokenize(standardized_text)
    
            for token in tokenized_text:
                output_file.write(token)
                output_file.write("\n")

        output_file.close()

    raw_file.close()        

end = time.time()
length = end - start

print(f"Tokenization process completed in {length:.3f} seconds.")