import PyPDF2
from pathlib import Path
import csv
import spacy

def extract_text_from_all_pdfs(pdf_files):
  full_text = ''
  for pdf in pdf_files:
    full_text += extract_text_from_pdf(pdf)
  return full_text

def pdf_files(path):
  search = Path(path).glob("*.pdf")

  files = [file.absolute()for file in search]
  return files


def extract_text_from_pdf(pdf):
  text = ''
  reader = PyPDF2.PdfReader(pdf)
  for page in reader.pages:
    text += page.extract_text()
  return text


def process_with_spacy(text):
  nlp = spacy.load("en_core_web_trf") # accuracy
  # nlp = spacy.load("en_core_web_sm") # efficiency
  doc = nlp(full_text)
  return doc


def map_columns(doc):
  header_row = ['Text', 'Label']
  data_list = [header_row]
  for entity in doc.ents:
    data_list.append( [entity.text, entity.label_])
  return data_list

def export_to_csv(data_list):
  with open('labels.csv', 'w', newline='') as file:
     writer = csv.writer(file)
     writer.writerows(data_list)

full_text = extract_text_from_all_pdfs(pdf_files('text_sources'))
doc = process_with_spacy(full_text)
data = map_columns(doc)
export_to_csv(data)
