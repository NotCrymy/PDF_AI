import python_core.pdf.PdfList as PdfList
import python_core.pdf.PdfDocument as PdfDocument
import python_core.pdf.PdfManager as PdfManager

import python_core.ai.AIManager as AIManager

if __name__ == "__main__":
    model = "lfm2.5-local"  # Specify the model you want to use

    pdf_list = ["./pdf_files/Compte_rendu_reunion_Maki.pdf", "./pdf_files/Compte_rendu_reunion_Maki2.pdf", "./pdf_files/diapo1.pdf"]
    pdf_lst = PdfList.PdfList(pdf_list)

    pdf_manager = PdfManager.PdfManager()
    
    lst_documents = pdf_manager.parse_all(pdf_lst)
    pdf_manager.to_json_all(lst_documents, "./python_core/parsed_doc") 

    for document in lst_documents:
        print(f"PDF Path: {document.path}")
        for page in document.pages:
            print(f"Page {page['page']}: {page['text'][:100]}...") 

    print(pdf_manager.get_page(lst_documents[2], 1))

    ai = AIManager.AIManager(model = model)
    response = ai.ask("Quel est le sujet de la réunion ?")
    print("AI Response:", response)