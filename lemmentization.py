import fitz  # PyMuPDF
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import re

# Ensure you download the required NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')

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

    # Perform POS tagging
    pos_tags = pos_tag(tokens)

    # Initialize the WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()

    # Lemmatize tokens using POS tags and convert to lowercase
    lemmatized_tokens = []
    for word, tag in pos_tags:
        wordnet_pos = get_wordnet_pos(tag) or wordnet.NOUN  # Default to NOUN if no match
        lemmatized_word = lemmatizer.lemmatize(word.lower(), pos=wordnet_pos)  # Lowercase before lemmatizing
        lemmatized_tokens.append(lemmatized_word)

        # Debugging: Display the mapping process (optional)
        print(f"Original: {word}, POS Tag: {tag}, Mapped POS: {wordnet_pos}, Lemmatized: {lemmatized_word}")

    print("\nLemmatized Tokens:", lemmatized_tokens)

else:
    print("No text extracted from the page. Please check the PDF.")

# Close the document
doc.close()
