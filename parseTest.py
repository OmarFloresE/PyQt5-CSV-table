import csv
from csv import DictReader

outfile = open("maleHumans.csv", "w") # Creating a CSV outfile to send filtered data to 

# outfileheader = "First Name, Sex\n" # Writing a top header manually to illustrate categories 
# outfile.write(outfileheader)


with open("humans.csv", 'r', encoding="utf8") as infile: # Opening the CSV file 

    csv_reader = DictReader(infile)
    reader = csv.reader(infile, delimiter = ",") # Creating a generator that uses ',' to denote the data, this is one method
    header = next(reader) # assigning the header of the data
    print(header) # Printing top headers of the data, can also print indexes of it i.e. - header[1]


    # for row in csv_reader:
    #     for col in row:
    #         print(col)
    


    for row in reader: # iterating using the reader variable! 

        userIndex = row[0]    # Printing out every row element 
        userID = row[1]
        firstName = row[2]
        lastName = row[3]
        sex = row[4]
        email = row[5]
        phone = row[6]
        birthday = row[7]
        jobTitle = row[8]
        
        if sex == "Male": # filtering the data to an outfile for only the males and their name 
            line = "{},{}\n".format(firstName, sex)
            outfile.write(line)
        print(userIndex,userID,firstName,lastName,sex,email,phone,birthday,jobTitle)

infile.close()
outfile.close()
