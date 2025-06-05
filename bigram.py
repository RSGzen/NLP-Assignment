import time
import os

from nltk.util import bigrams

def main():
    start = time.time()
    print("Starting to trigram process. Please wait patiently.......")

    word_bank = []

    raw_file_address = get_file_address("data", "tokens.txt")
    output_file_address = get_file_address("data", "bigram.txt")

    with open(raw_file_address, 'r', encoding='utf_8') as raw_file:

        with open(output_file_address, 'a', encoding='utf_8') as output_file:   
            
            for token_txt in raw_file:
                if token_txt == None:
                    continue
                
                token_txt = token_txt.rstrip()
                
                if len(word_bank) < 2:
                    word_bank.append(token_txt)

                if len(word_bank) >= 2:
                    bigram_list = list(bigrams(word_bank))
                    word_bank.pop(0)
                    
                    output_string = gen_output_string(bigram_list)

                    output_file.write(output_string)
                    
            output_file.close()

        raw_file.close()        

    end = time.time()
    length = end - start

    print(f"Bigram process completed in {length:.3f} seconds.")

def get_file_address(folder_name, file_name):

    current_wd = os.getcwd()
    file_address = os.path.join(current_wd, folder_name)

    final_address = os.path.join(file_address, file_name)

    return final_address

def gen_output_string(bigram_list):
    output_string = str(bigram_list)
    
    output_string = output_string.replace("(", "")
    output_string = output_string.replace(")", "")
    output_string = output_string.replace("'", "")
    output_string = output_string.replace(",", "")

    output_string = output_string.replace("[", "")
    output_string = output_string.replace("]", "\n")

    return output_string

main()