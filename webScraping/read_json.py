import json

num_article_converted = 0

json_file_name_list = ["anandtech_cpus_out.json",
                       "anandtech_gpus_out.json",
                       "anandtech_mb_out.json",
                      "anandtech_mem_out.json",
                       "anandtech_ssd_out.json",
                       "gamernexus_out.json"
                       ]

print("Progress of Number of Articles Downloaded: ")

with open("raw_sentences.txt", 'a', encoding="utf_8") as text_file:

    for filename in json_file_name_list:
        
        print(f"\nI am now in file: {filename}\n")
        
        with open(filename, 'r', encoding="utf_8") as json_file:
            
            data = json.load(json_file)

            for article in data:

                para = ""
                for sentences in article["paragraph"]:
                    para = para + sentences

                text_file.write(para)
                text_file.write("\n")

                num_article_converted += 1
                print(f"{num_article_converted}", end=" ")

                if num_article_converted%10 == 0:
                    print("\n")

            json_file.close()
    
    text_file.close()