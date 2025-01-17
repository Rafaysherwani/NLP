# Importing required libraries
from pypdf import PdfReader
import fitz  # PyMuPDF
import nltk
from nltk.tokenize import word_tokenize
import re

# Ensure you download the required NLTK data
nltk.download('punkt')

# Load the PDF using PyMuPDF
pdf_document = '20L-1207_Case Studie.pdf'
doc = fitz.open(pdf_document)

# Extract text from the first page using fitz
page = doc[0]
text = page.get_text()

if text:
    print("Text successfully extracted from the page.")

    # Preprocessing: Add spaces between concatenated words (heuristic)
    cleaned_text = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", text)

    # Tokenize the preprocessed text
    tokens = word_tokenize(cleaned_text)
    print("Tokens:", tokens)
else:
    print("No text extracted from the page. Please check the PDF.")

# Close the PDF document
doc.close()

