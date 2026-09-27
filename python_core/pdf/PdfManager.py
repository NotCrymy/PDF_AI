import pymupdf
import json

import pdf.PdfDocument as PdfDocument
import pdf.PdfList as PdfList

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

    def to_json_all(self, pdf_documents : list, output_path : str):
        """
        Converts a list of PdfDocument objects to JSON files in the specified output path.
        
        Args:
            pdf_documents (list): A list of PdfDocument instances to convert.
            output_path (str): The directory path where the JSON files will be saved.
        """
        for pdf_document in pdf_documents:
            self.to_json(pdf_document, output_path)