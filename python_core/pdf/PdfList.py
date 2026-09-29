class PdfList:
    """A class to manage a list of PDF files."""

    def __init__(self, pdf_list : list):
        """
        Initializes the PdfList with a list of PDF file paths.
        
        Args:
            pdf_list (list): A list of PDF file paths.
        """
        self.list = pdf_list