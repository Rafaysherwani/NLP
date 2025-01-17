from pypdf import PdfReader
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Ensure required NLTK data is downloaded
nltk.download('punkt_tab')
nltk.download('stopwords')

# Load the PDF
reader = PdfReader('20L-1207_Case Studie.pdf')

# Print the number of pages in the PDF
print("Number of pages in the PDF:", len(reader.pages))

# Extract text from the first page
page = reader.pages[0]
text = page.extract_text()

# Ensure the text is not empty
if not text.strip():
    print("The page contains no extractable text.")
else:
    # Tokenize the extracted text
    tokens = word_tokenize(text)

    # Get the stopwords set
    stop_words = set(stopwords.words('english'))

    # Filter out stopwords from tokens
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

    print("Filtered Tokens:", filtered_tokens)
