
import fitz  # PyMuPDF
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.chunk import RegexpParser

# Ensure you download the required NLTK data
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')

# Load the PDF using fitz
pdf_document = '20L-1207_Case Studie.pdf'
doc = fitz.open(pdf_document)

# Extract text from the first page
page = doc[0]
text = page.get_text()

if text:
    print("Text successfully extracted from the page.")

    # Tokenize the text
    tokens = word_tokenize(text)

    # Perform POS tagging
    pos_tags = pos_tag(tokens)
    print("POS Tags:", pos_tags)

    # Define a grammar for chunking (example: noun phrases)
    grammar = r"""
        NP: {<DT>?<JJ>*<NN.*>+}   # Noun Phrase: Optional determiner, adjectives, and nouns
        VP: {<VB.*><NP|PP>*}      # Verb Phrase: Verb followed by noun phrase or prepositional phrase
    """

    # Create a chunk parser
    chunk_parser = RegexpParser(grammar)

    # Perform chunking
    tree = chunk_parser.parse(pos_tags)

    # Display the chunks
    print("Chunks:")
    for subtree in tree.subtrees(filter=lambda t: t.label() in ["NP", "VP"]):
        print(subtree)

else:
    print("No text extracted from the page. Please check the PDF.")

# Close the document
doc.close()
