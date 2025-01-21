from fastapi import FastAPI, File, UploadFile, HTTPException
import fitz  # PyMuPDF
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.chunk import RegexpParser
import os

# Ensure required NLTK data is downloaded
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Initialize FastAPI app
app = FastAPI()

# Define grammar for chunking (e.g., noun phrases and verb phrases)
grammar = r"""
    NP: {<DT>?<JJ>*<NN.*>+}   # Noun Phrase: Optional determiner, adjectives, and nouns
    VP: {<VB.*><NP|PP>*}      # Verb Phrase: Verb followed by noun phrase or prepositional phrase
"""

# Define the chunking function
def extract_chunks_and_pos(file_path: str):
    # Load the PDF using fitz
    doc = fitz.open(file_path)

    # Extract text from the first page
    page = doc[0]
    text = page.get_text()

    if not text:
        raise ValueError("No text extracted from the uploaded document.")

    # Tokenize the text
    tokens = word_tokenize(text)

    # Perform POS tagging
    pos_tags = pos_tag(tokens)

    # Create a chunk parser
    chunk_parser = RegexpParser(grammar)

    # Perform chunking
    tree = chunk_parser.parse(pos_tags)

    # Extract chunks
    chunks = []
    for subtree in tree.subtrees(filter=lambda t: t.label() in ["NP", "VP"]):
        chunks.append(" ".join(word for word, _ in subtree.leaves()))

    # Close the document
    doc.close()

    return {
        "pos_tags": pos_tags,  # All tokens with POS tags
        "chunks": chunks       # Extracted noun phrases and verb phrases
    }

# Root GET endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Chunking API!",
        "instructions": "Use the /upload/ endpoint to upload a PDF file and extract POS tags and chunks."
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
        # Extract POS tags and chunks from the uploaded document
        result = extract_chunks_and_pos(file_location)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up the temporary file
        if os.path.exists(file_location):
            os.remove(file_location)

    return result
