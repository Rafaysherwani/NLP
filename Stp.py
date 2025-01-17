import fitz # PyMuPDF
print(fitz.__doc__)  # Optional: Check if fitz loads successfully

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import re

# Ensure required NLTK data is downloaded
nltk.download('punkt_tab')
nltk.download('stopwords')

# Load the PDF
pdf_document = "20L-1207_Case Studie.pdf"
doc = fitz.open(pdf_document)

# Extract text from all pages
text = ""
for page in doc:
    text += page.get_text()

# Debug: Print the first 500 characters of the extracted text
print(f"Extracted text: {text[:500]}")

# Fix missing spaces in concatenated words
text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # Add space between lowercase and uppercase letters
text = re.sub(r'(\d)([A-Za-z])', r'\1 \2', text)  # Add space between numbers and letters
text = re.sub(r'([A-Za-z])(\d)', r'\1 \2', text)  # Add space between letters and numbers

# Tokenize the cleaned text
tokenizer = RegexpTokenizer(r'\w+')
tokens = tokenizer.tokenize(text)

# Remove stopwords
stop_words = set(stopwords.words('english'))
filtered_tokens = [token.lower() for token in tokens if token.lower() not in stop_words]

# Print the filtered tokens
print("Filtered Tokens:", filtered_tokens)
