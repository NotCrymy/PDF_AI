from .Conversation import Conversation

class ConversationManager:

    def create_conversation(self):
        """Create a new conversation and return it.
        
        Returns:
            Conversation: The newly created conversation object.
        """
        return Conversation()

    def add_question(self, conversation, question):
        """Add a question to the specified conversation.
        
        Args:
            conversation (Conversation): The conversation to which the question will be added.
            question (str): The question to add.
        """
        conversation.questions.append(question)
        conversation.question_counter += 1

    def add_answer(self, conversation, answer):
        """Add an answer to the specified conversation.
        
        Args:
            conversation (Conversation): The conversation to which the answer will be added.
            answer (str): The answer to add.
        """
        conversation.answers.append(answer)
        conversation.answer_counter += 1

    def get_questions(self, conversation, id):
        """Retrieve a question from the specified conversation by its ID.
        
        Args:
            conversation (Conversation): The conversation from which to retrieve the question.
            id (int): The ID of the question to retrieve.
            
        Returns:
            str: The question corresponding to the specified ID.
        Raises:
            ValueError: If the ID is invalid (less than or equal to 0 or greater than the number of questions)
        """
        if id <= 0 or id > conversation.question_counter:
            raise ValueError("Invalid question ID.")
        
        return conversation.questions[id - 1]


    def get_answers(self, conversation, id):
        """Retrieve an answer from the specified conversation by its ID.
        
        Args:
            conversation (Conversation): The conversation from which to retrieve the answer.
            id (int): The ID of the answer to retrieve.

        Returns:
            str: The answer corresponding to the specified ID.
        
        Raises:
            ValueError: If the ID is invalid (less than or equal to 0 or greater than the number of answers)
        """
        if id <= 0 or id > conversation.answer_counter:
            raise ValueError("Invalid answer ID.")
        
        return conversation.answers[id - 1]