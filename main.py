import spacy # import NLP module library
from spacypdfreader import pdf_reader # import SpaCy add-on library that extracts text from a PDF 
from pathlib import Path # import library that will allow us to gather all PDFS in a folder
import csv # import library that will allow us to write data to a CSV file


nlp = spacy.load('en_core_web_sm') # this loads the SpaCy english NLP module for

def find_pdf_files_in_folder(folder):  # this function finds and returns all pdf files in the specified folder
  search = Path(folder).glob("*.pdf") 

  files = [file.absolute()for file in search]
  return files

pdf_files = find_pdf_files_in_folder('text_sources') # this calls the function defined above to return a list of all the pdfs in the specified folder


data_list = [['Text', 'Label', 'Source File']] # initialize a list with a header row, containing 3 columns (Text, Label, Source File)


for pdf in pdf_files: # for each pdf in the pdf list
  doc = pdf_reader(pdf, nlp) # analyse the pdf with SpaCy 
  for entity in doc.ents: #for each entity found by SpaCy
    data_list.append( [entity.text, entity.label_, doc._.pdf_file_name ]) # add to the data list, a "sub-list" containing: (1)the entity text,(2) the label(=category) assigned by SpaCy, and (3) the Pdf file it is found in. This "sub-list" corresponds to a row in the final exported CSV


def export_to_csv(data_list): # this function exports the data_list created earlier to a CSV file, where each SpaCy entry is a row with 3 columns
  with open('labels.csv', 'w', newline='') as file: #opens a file in 'write' mode, and gives it a name
     writer = csv.writer(file)  # creates a csv 'writer' object on the opened file
     writer.writerows(data_list) # adds the data to the csv

export_to_csv(data_list) # calls the function defined above to export the data_list to csv
