import os

import pymupdf
import json

from . import PdfList
from . import PdfDocument

class PdfManager:

    def parse_all(self, pdf_list : PdfList.PdfList):
        """
        Parses all PDF documents in the provided PdfList and returns a list of PdfDocument objects.
        
        Args:
            pdf_list (PdfList): An instance of PdfList containing the PDF file paths to parse.

        Returns:
            list: A list of PdfDocument objects containing the parsed data.
        """
        documents = []

        for pdf_path in pdf_list.list:
            document = self.parse(pdf_path)
            documents.append(document)

        return documents

    def parse(self, pdf_path : str):
        """
        Parses a single PDF document and returns a PdfDocument object.
        
        Args:
            pdf_path (str): The file path of the PDF document to parse.

        Returns:
            PdfDocument: An instance of PdfDocument containing the parsed data.
        """
        document = PdfDocument.PdfDocument(pdf_path)

        with pymupdf.open(pdf_path) as pdf:
            for page_number in range(len(pdf)):
                page = pdf[page_number]
                text = page.get_text()
                text = text.replace('\n', ' ').replace('\r', ' ').strip()
                document.add_page(page_number + 1, text)

        return document

    def to_json(self, pdf_document : PdfDocument.PdfDocument, output_path : str):
        """
        Converts a PdfDocument object to a JSON file in the specified output path.
        
        Args:
            pdf_document (PdfDocument): An instance of PdfDocument to convert.
            output_path (str): The file path where the JSON will be saved.
        """
        json_data = {
            "path": pdf_document.path,
            "pages": pdf_document.pages
        }

        with open(f"./{output_path}/{pdf_document.name}.json", "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

    def to_json_all(self, pdf_documents : list[PdfDocument.PdfDocument], output_path : str):
        """
        Converts a list of PdfDocument objects to JSON files in the specified output path.
        
        Args:
            pdf_documents (list): A list of PdfDocument instances to convert.
            output_path (str): The directory path where the JSON files will be saved.
        """
        for pdf_document in pdf_documents:
            self.to_json(pdf_document, output_path)

    def get_page(self, pdf_document : PdfDocument.PdfDocument, page_number : int):
        """
        Retrieves the text content of a specific page from a PdfDocument.
        
        Args:
            pdf_document (PdfDocument): An instance of PdfDocument to retrieve the page from.
            page_number (int): The page number to retrieve (1-based index).

        Returns:
            str: The text content of the specified page.
        """
        return pdf_document.pages[page_number - 1]["text"] if 0 < page_number <= len(pdf_document.pages) else None

    def delete_document(self, pdf_document : PdfDocument.PdfDocument, output_path : str):
        """
        Deletes the PDF file corresponding to a PdfDocument.
        
        Args:
            pdf_document (PdfDocument): An instance of PdfDocument whose PDF file will be deleted.
            output_path (str): The directory path where the JSON file is located.
        """
        try:
            os.remove(pdf_document.path)
            os.remove(f"./{output_path}/{pdf_document.name}.json")
        except FileNotFoundError:
            print(f"File {pdf_document.path} not found.")

    def delete_all_documents(self, pdf_documents : list[PdfDocument.PdfDocument], output_path : str):
        """
        Deletes all PDF files corresponding to a list of PdfDocument objects.
        
        Args:
            pdf_documents (list): A list of PdfDocument instances whose PDF files will be deleted.
            output_path (str): The directory path where the JSON files are located.
        """
        for pdf_document in pdf_documents:
            self.delete_document(pdf_document, output_path)