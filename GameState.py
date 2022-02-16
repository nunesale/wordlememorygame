class GameState:

    def __init__(self, keyword, answer_list):
        # maximum amount of letters the user can enter
        self.word_length = 5

        # filo stack containing the letters the user has entered in order from left to right
        self.entered_letters = []

        # number of letters the user has currently entered
        self.num_entered = 0

        # the main word
        self.keyword = keyword

        # list of tuples in which the first element is an answer, and the second element is a string representing the
        # wordle feedback data from the keyword in which that answer would be optimal
        self.answer_list = answer_list

        # add a dummy value to answer list to avoid a crash at the end
        self.answer_list.append(("slane", "bbbbb"))

        # tracks what word the user is on, used as index into answer list
        self.counter = 0

        # number of words the used has solved correctly
        self.num_correct = 0

        # number of total words to guess
        self.total_answers = len(answer_list) - 1

        # true if all words have been attempted, false otherwise
        self.completed = False

        # current answer, initialized to first word in answer list
        self.current_answer = self.answer_list[self.counter][0]

        # current colour data, initialized to first colour data in answer list
        self.current_colour_data = self.answer_list[self.counter][1]

    # add a letter to entered_letters, if possible
    def enter_letter(self, letter):
        if self.num_entered < self.word_length:
            self.entered_letters.append(letter)
            self.num_entered += 1
        print(self.entered_letters)

    # remove the latest letter from entered_letters, if possible
    def delete_letter(self):
        if self.num_entered > 0:
            self.entered_letters.pop()
            self.num_entered -= 1

    # return true if the answer word is contained in entered_letters, false otherwise
    # also increments num_correct if answer is correct
    def verify(self):
        correct = True
        self.num_correct += 1
        for i in range(len(self.entered_letters)):
            if self.entered_letters[i] != self.answer_list[self.counter][0][i]:
                correct = False
                self.num_correct -= 1
                break
        return correct

    # advance the game state to the next word
    def advance(self):
        self.counter += 1
        if self.counter < self.total_answers:
            self.current_answer = self.answer_list[self.counter][0]
            self.current_colour_data = self.answer_list[self.counter][1]
            self.entered_letters = []
            self.num_entered = 0
        else:
            self.completed = True

