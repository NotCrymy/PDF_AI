from ollama import chat
from .DocumentLoader import DocumentLoader


class AIManager:

    def __init__(
        self,
        model: str = "lfm2.5-local",
        document_context_path: str = "./python_core/parsed_doc/",
        all_models: list[str] | None = None,
        initial_prompt: str = """
            Tu es un assistant spécialisé dans l'analyse de documents.

            Tu disposes d'un ensemble de documents PDF fournis par l'utilisateur.

            RÈGLES :

            - Cherche d'abord les informations pertinentes dans les documents.
            - Tu peux reformuler et synthétiser les informations trouvées.
            - Si plusieurs passages permettent de répondre à la question, combine-les.
            - Si la question demande une synthèse, produis une synthèse claire.
            - Si la question demande une explication, explique naturellement les informations présentes.
            - Ne refuse pas de répondre simplement parce que la formulation exacte n'apparaît pas dans les documents.
            - Si les documents ne permettent réellement pas de répondre, indique que l'information n'est pas disponible.
            - Lorsque tu utilises une information provenant d'un document, indique sa source sous la forme :
            [Nom du document, page X]
        """
    ):
        self.current_model = model
        self.all_models = all_models if all_models is not None else []

        if model not in self.all_models:
            self.all_models.append(model)

        self.document_loader = DocumentLoader(document_context_path)
        self.documents = self.document_loader.load_all()

        self.initial_prompt = initial_prompt

    def set_model(self, model: str):
        self.current_model = model

    def add_model(self, model: str):
        if model not in self.all_models:
            self.all_models.append(model)

    def build_context(self) -> str:
        """
        Build a context string from the loaded documents.
        
        Returns:
            str: A string containing the context from all documents.
        """
        self.documents = self.document_loader.load_all()

        context = ""

        for document in self.documents:
            context += f"\n[DOCUMENT: {document['name']}]\n"

            for page in document["pages"]:
                context += (
                    f"\n[SOURCE: {document['name']} | PAGE: {page['page']}]\n"
                )

                context += page["text"]
                context += "\n"

        return context

    def ask(self, question: str, conversation_messages: list[dict[str, str]]) -> str:
        context = self.build_context()

        messages = [
            {
                "role": "system",
                "content": self.initial_prompt
            },

            *conversation_messages, # indluding all previous conversation messages here by unpacking the list

            {
                "role": "user",
                "content": f"""
                DOCUMENTS :

                {context}

                QUESTION :

                {question}
                """
            }
        ]

        response = chat(
            model=self.current_model,
            messages=messages
        )

        return response.message.content