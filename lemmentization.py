# Importing required libraries
import fitz  # PyMuPDF
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re

# Ensure you download the required NLTK data
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Load the PDF using fitz
pdf_document = '20L-1207_Case Studie.pdf'
doc = fitz.open(pdf_document)

# Extract text from the first page
page = doc[0]
text = page.get_text()

if text:
    print("Text successfully extracted from the page.")

    # Preprocessing: Add spaces between concatenated words (basic heuristic)
    text_preprocessed = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", text)

    # Tokenize the preprocessed text
    tokens = word_tokenize(text_preprocessed)
    print("Tokens:", tokens)

    # Initialize the WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()

    # Lemmatize each token
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]

    print("Lemmatized Tokens:", lemmatized_tokens)
else:
    print("No text extracted from the page. Please check the PDF.")

# Close the document
doc.close()
