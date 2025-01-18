
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

    # Tokenize the text into sentences
    sentences = nltk.sent_tokenize(text)

    # Define a grammar for sentence-level chunking
    grammar = r"""
        SENTENCE: {<DT>?<JJ>*<NN.*>+<VB.*><DT>?<JJ>*<NN.*>+}  # Sentence: Noun Phrase + Verb + Noun Phrase
    """

    # Create a chunk parser for sentences
    chunk_parser = RegexpParser(grammar)

    print("Chunks:")
    for sentence in sentences:
        # Tokenize the sentence
        tokens = word_tokenize(sentence)

        # Perform POS tagging
        pos_tags = pos_tag(tokens)

        # Perform chunking at the sentence level
        tree = chunk_parser.parse(pos_tags)

        # Display the chunks
        for subtree in tree.subtrees(filter=lambda t: t.label() == "SENTENCE"):
            print(subtree)

else:
    print("No text extracted from the page. Please check the PDF.")

# Close the document
doc.close()
