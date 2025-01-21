from fastapi import FastAPI, File, UploadFile, HTTPException
import fitz  # PyMuPDF
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import re
import os

# Ensure NLTK resources are downloaded
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Initialize FastAPI app
app = FastAPI()

# Add a root GET endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Lemmatization API!"}

# Function to map POS tags to WordNet-compatible POS tags
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

# Define the text pre-processing function
def process_document(file_path: str):
    # Open the PDF using fitz
    doc = fitz.open(file_path)

    # Extract text from the first page
    page = doc[0]
    text = page.get_text()

    if not text:
        raise ValueError("No text found in the uploaded document.")

    # Preprocessing: Add spaces between concatenated words (basic heuristic)
    text_preprocessed = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", text)

    # Tokenize the preprocessed text
    tokens = word_tokenize(text_preprocessed)

    # Perform POS tagging
    pos_tags = pos_tag(tokens)

    # Initialize the WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()

    # Lemmatize tokens using POS tags and convert to lowercase
    lemmatized_tokens = []
    for word, tag in pos_tags:
        wordnet_pos = get_wordnet_pos(tag) or wordnet.NOUN
        lemmatized_tokens.append(lemmatizer.lemmatize(word.lower(), pos=wordnet_pos))

    # Close the document
    doc.close()

    return {
        "tokens": tokens,
        "lemmatized_tokens": lemmatized_tokens
    }

# FastAPI route to upload and process the document
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    # Save the uploaded file temporarily
    file_location = f"temp_{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    try:
        # Process the uploaded document
        result = process_document(file_location)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up the temporary file
        if os.path.exists(file_location):
            os.remove(file_location)

    return result
