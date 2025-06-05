import csv

with open("Free_Proxy_List.csv") as file_obj:
    
    heading = next(file_obj)
    reader_obj = csv.reader(file_obj)

    ip_arr = []

    for row in reader_obj:
        ip_add = row[0] + ":" + row[6]
        ip_arr.append(ip_add)
    
    print("IP Address is read from CSV file")
    
    with open("proxies.txt", "a") as f:
        for j in range(0, len(ip_arr)):
            f.write(ip_arr[j])
            f.write("\n")
        
        print("Data is written into file")

    f.close()

file_obj.close()