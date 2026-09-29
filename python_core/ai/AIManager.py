from ollama import chat
from .DocumentLoader import DocumentLoader


class AIManager:

    def __init__(
        self,
        model: str = "lfm2.5-local",
        document_context_path: str = "./python_core/parsed_doc/"
    ):
        self.model = model
        self.document_loader = DocumentLoader(document_context_path)

        self.documents = self.document_loader.load_all()

    def build_context(self) -> str:
        context = ""

        for document in self.documents:
            context += f"\n[DOCUMENT: {document['path']}]\n"

            for page in document["pages"]:
                context += (
                    f"\n[SOURCE: {document['path']} | PAGE: {page['page']}]\n"
                )
                context += page["text"]
                context += "\n"

        return context

    def ask(self, question: str) -> str:

        context = self.build_context()

        prompt = f"""
            Tu es un assistant spécialisé dans l'analyse de documents PDF.
            Réponds à partir des informations présentes dans les documents.
            Si l'information n'est pas présente dans les documents, tu peux répondre "Je ne sais pas".
            Lorsque tu utilises une information, indique le document et la page correspondante.
            Si des certains documents ne te semblent pas partinents pour répondre à la question, ignore-les simplement, tu n'es pas obligé de les mentionner ni de les utiliser.
            Tu peux répondre naturellement quand il ne s'agit pas d'une question lié aux documents.

            Voici les documents disponibles :
            {context}

            Question :
            {question}
        """

        response = chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.message.content