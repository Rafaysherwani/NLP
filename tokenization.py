# importing required classes
# importing required classes
from pypdf import PdfReader
import fitz  # PyMuPDF
import nltk
from nltk.tokenize import word_tokenize

# Ensure you download the required data for tokenization
nltk.download('punkt')

# Load the PDF
reader = PdfReader('20L-1207_Case Studie.pdf')

# Printing the number of pages in the PDF file
print("Number of pages:", len(reader.pages))

# Creating a page object (first page in this case)
page = reader.pages[0]

# Extracting text from the page
text = page.extract_text()
if text:
    print("Text successfully extracted from the page.")

    # Tokenizing the extracted text
    tokens = word_tokenize(text)
    print("Tokens:", tokens)
else:
    print("No text extracted from the page. Please check the PDF.")
# importing required classes
from pypdf import PdfReader
import fitz  # PyMuPDF
import nltk
from nltk.tokenize import word_tokenize

# Ensure you download the required data for tokenization
nltk.download('punkt')

# Load the PDF
reader = PdfReader('20L-1207_Case Studie.pdf')

# Printing the number of pages in the PDF file
print("Number of pages:", len(reader.pages))

# Creating a page object (first page in this case)
page = reader.pages[0]

# Extracting text from the page
text = page.extract_text()
if text:
    print("Text successfully extracted from the page.")

    # Tokenizing the extracted text
    tokens = word_tokenize(text)
    print("Tokens:", tokens)
else:
    print("No text extracted from the page. Please check the PDF.")
