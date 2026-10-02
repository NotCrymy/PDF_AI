class Conversation:
    _conversation_id_counter = 0
    def __init__(self):
        Conversation._conversation_id_counter += 1

        self.conversation_id = Conversation._conversation_id_counter
        self.question_counter = 0
        self.questions = []
        self.answer_counter = 0
        self.answers = []