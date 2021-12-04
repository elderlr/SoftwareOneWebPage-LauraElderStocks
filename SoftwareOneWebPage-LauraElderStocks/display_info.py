# CS361 Assignment 7: Microservices Integration
# Author: Elaine Zamora
# Date: 11/11/2021
# 

import sys
import json
import requests
import wikipedia



def display_info(words, location):
    """
        Takes as input a query and writes result to a text file named search_result.txt
        Uses Wikipedia to search and return a summary of text related to search query
        """
    to_file = location

   # search wikipedia, parse data, and write summary to search_result.txt
    try: 
        summary = wikipedia.summary(words)
    except:
        temp = {'name':words, 'summary':'NULL'}
        with open(to_file, "w") as outfile:
            json.dump(temp, outfile)
        outfile.close()
        

    #create dictionary to store results for user to access
    r_dict = {'name':words, 'summary':summary}

    # write results of name, summary, image to json outfile
    with open(to_file, "w") as outfile:
        json.dump(r_dict, outfile)
    outfile.close()



def main():
    # example usage
    #user_query = 'oprah'
    #file_location = 'C:\\Users\\elain\\361\\search_result.txt'
    #display_info(user_query, file_location)

    if __name__ == "__main__":
        main()