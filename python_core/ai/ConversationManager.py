from .Conversation import Conversation


class ConversationManager:

    def create_conversation(self):
        """Create a new conversation and return it.

        Returns:
            Conversation: The newly created conversation object.
        """
        return Conversation()

    def add_question(self, conversation: Conversation, question: str):
        """Add a question to a conversation."""
        conversation.questions.append(question)
        conversation.question_counter += 1

    def add_answer(self, conversation: Conversation, answer: str):
        """Add an answer to a conversation."""
        conversation.answers.append(answer)
        conversation.answer_counter += 1

    def get_questions(self, conversation: Conversation, id: int):
        """Retrieve a question from a conversation by its ID."""
        if id <= 0 or id > conversation.question_counter:
            raise ValueError("Invalid question ID.")

        return conversation.questions[id - 1]

    def get_answers(self, conversation: Conversation, id: int):
        """Retrieve an answer from a conversation by its ID."""
        if id <= 0 or id > conversation.answer_counter:
            raise ValueError("Invalid answer ID.")

        return conversation.answers[id - 1]

    def get_messages(self, conversation: Conversation):
        """Convert the conversation history to Ollama message format."""

        messages = []

        for question, answer in zip(
            conversation.questions,
            conversation.answers
        ):
            messages.append({
                "role": "user",
                "content": question
            })

            messages.append({
                "role": "assistant",
                "content": answer
            })

        return messages