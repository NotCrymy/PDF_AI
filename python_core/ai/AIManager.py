from ollama import chat
from .DocumentLoader import DocumentLoader


class AIManager:

    def __init__(
        self,
        model: str = "lfm2.5-local",
        document_context_path: str = "./python_core/parsed_doc/",
        all_models: list[str] | None = None
    ):
        self.current_model = model
        self.all_models = all_models if all_models is not None else []

        if model not in self.all_models:
            self.all_models.append(model)

        self.document_loader = DocumentLoader(document_context_path)
        self.documents = self.document_loader.load_all()

    def set_model(self, model: str):
        self.current_model = model

    def add_model(self, model: str):
        if model not in self.all_models:
            self.all_models.append(model)

    def build_context(self) -> str:
        self.documents = self.document_loader.load_all()

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

            Voici les documents disponibles :
            {context}

            Question :
            {question}
        """

        response = chat(
            model=self.current_model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.message.content