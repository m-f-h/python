"""
Goal : extract matadata from a scientific article in PDF

*metadata = Title, Authors, Affiliations, Abstract, Keywords, MSC numbers ...

To extract the title, authors, and abstract from a PDF file of a scientific article, 
you can use Python with libraries such as PyMuPDF (fitz), PyPDF2, or pdfplumber for reading PDFs, 
and libraries like re for regular expressions to extract specific content. 
Example program using PyMuPDF to achieve this:

1. **Install the required libraries**:
   ```
  pip install PyMuPDF
   ```

2. **Create the Python script**:
   ```python
"""
if 1:
   import fitz  # PyMuPDF
   import re

   def extract_text_from_first_page(pdf_path):
       # Open the PDF file
       doc = fitz.open(pdf_path)
       # Extract text from the first page
       first_page = doc[0]
       text = first_page.get_text()
       return text

   def extract_title(text):
       # Assuming the title is the first line
       title = text.split('\n')[0].strip()
       return title

   def extract_authors(text):
       # Assuming authors are listed right after the title in the second line
       lines = text.split('\n')
       authors_line = lines[1].strip()
       return authors_line

   def extract_abstract(text):
       # Searching for 'Abstract' keyword and extracting text until the next section
       abstract = ""
       abstract_pattern = re.compile(r'(Abstract|ABSTRACT)(.*?)(Introduction|INTRODUCTION|1\.)', re.S)
       match = abstract_pattern.search(text)
       if match:
           abstract = match.group(2).strip()
       return abstract

   def extract_information(pdf_path):
       text = extract_text_from_first_page(pdf_path)
       title = extract_title(text)
       authors = extract_authors(text)
       abstract = extract_abstract(text)

       return {
           "title": title,
           "authors": authors,
           "abstract": abstract
       }

   if __name__ == "__main__":
       pdf_path = "path/to/your/pdf_file.pdf"  # Replace with your PDF file path
       info = extract_information(pdf_path)
       print("Title:", info["title"])
       print("Authors:", info["authors"])
       print("Abstract:", info["abstract"])
"""
This script assumes a common structure for scientific articles. Depending on the exact format of the PDFs you are working with, you might need to adjust the text extraction logic and regular expressions to suit your needs.
"""
# eof
