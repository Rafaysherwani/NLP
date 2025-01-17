import pdfplumber

# Path to your PDF file
pdf_path = "20L-1207_Case Studie.pdf"

# Open and extract text from the PDF
with pdfplumber.open(pdf_path) as pdf:
    text = ""
    for page in pdf.pages:
        text += page.extract_text()

print("Extracted Text:")
print(text)
