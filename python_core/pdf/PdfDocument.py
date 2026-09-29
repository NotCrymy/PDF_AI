class PdfDocument:
    """A class to represent a PDF document with its path and pages."""
    
    def __init__(self, path : str):
        """Initializes the PdfDocument with a file path and an empty list of pages."""
        self.name = path.split('/')[-1].split('.')[0]  # Extracts the file name without extension
        self.path = path
        self.pages = []

    def add_page(self, page_number : int, text : str):
        """Adds a page to the PdfDocument with the given page number and text content."""
        self.pages.append({
            "page": page_number,
            "text": text
        })