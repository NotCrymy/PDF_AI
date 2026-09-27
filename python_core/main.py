import pdf.PdfList as PdfList
import pdf.PdfDocument as PdfDocument
import pdf.PdfManager as PdfManager

if __name__ == "__main__":
    pdf_list = ["Compte_rendu_reunion_Maki.pdf", "Compte_rendu_reunion_Maki2.pdf", "diapo1.pdf"]
    pdf_lst = PdfList.PdfList(pdf_list)

    pdf_manager = PdfManager.PdfManager()
    
    documents = pdf_manager.parse_all(pdf_lst)
    pdf_manager.to_json_all(documents, "parsed_doc") 

    for document in documents:
        print(f"PDF Path: {document.path}")
        for page in document.pages:
            print(f"Page {page['page']}: {page['text'][:100]}...") 