import random

import pygame
from GameState import GameState

alphabet = "abcdefghijklmnopqrstuvwxyz"

input_file = "input.txt"
word_length = 5

display_width = 800
display_height = 500

black = (0, 0, 0)
white = (238, 238, 238)
incorrect_red = (216, 100, 100)
correct_green = (87, 172, 120)

game_display = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption("Wordle Memory")

clock = pygame.time.Clock()

image_dict = {"  ": pygame.image.load('letters/blank.png')}

letter_width = image_dict["  "].get_width()
letter_height = image_dict["  "].get_height()


# draw an empty letter space at x,y
def draw_blank(x, y):
    game_display.blit(image_dict["  "], (x, y))


# draw a letter with the specified type (w, b, y, g) at x,y
def draw_letter(letter, type, x, y):
    game_display.blit(image_dict[letter + type], (x, y))


# draw the progress counter in the upper left
def draw_progress_counter(progress_font, counter, max):
    text_surface = progress_font.render(str(counter) + "/" + str(max), True, black)
    game_display.blit(text_surface, (0, 0))


# draw the correctness indicator in the lower left
def draw_correctness_indicator(correctness_count_font, correctness_percent_font, correct, tried):
    # prevent division by zero
    if tried == 0:
        tried = 1

    percent = round((correct / tried * 100), 2)
    count_surface = correctness_count_font.render("Correct: " + str(correct), True, black)
    percent_surface = correctness_percent_font.render(str(percent) + "%", True, black)

    game_display.blit(count_surface, (0, display_height - count_surface.get_height() - percent_surface.get_height()))
    game_display.blit(percent_surface, (0, display_height - percent_surface.get_height()))


# draw the timer in the upper right
def draw_timer(timer_font, time):
    hours = time // 3600000
    time = time - (3600000 * hours)
    minutes = time // 60000
    time = time - (60000 * minutes)
    seconds = time // 1000
    milliseconds = time % 1000

    clock_string = ""
    if hours >= 10:
        clock_string += str(hours) + ":"
    else:
        clock_string += "0" + str(hours) + ":"

    if minutes >= 10:
        clock_string += str(minutes) + ":"
    else:
        clock_string += "0" + str(minutes) + ":"

    if seconds >= 10:
        clock_string += str(seconds) + "."
    else:
        clock_string += "0" + str(seconds) + "."

    if milliseconds >= 100:
        clock_string += str(milliseconds)
    elif milliseconds >= 10:
        clock_string += "0" + str(milliseconds)
    else:
        clock_string += "00" + str(milliseconds)

    timer_surface = timer_font.render(clock_string, True, black)
    game_display.blit(timer_surface, (display_width - 231, 0))


# draw the text indicating a correct guess
def draw_correct_guess(correct_font):
    correct_surface = correct_font.render("Correct!", True, black)
    game_display.blit(correct_surface, (display_width // 2 - (correct_surface.get_width() // 2), 0))


# draw the text indicating an incorrect guess, as well as what the answer was
def draw_incorrect_guess(incorrect_font, answer_font, correct_answer):
    incorrect_surface = incorrect_font.render("Wrong!", True, black)
    answer_surface = answer_font.render("The correct answer was: " + correct_answer, True, black)

    game_display.blit(incorrect_surface, (display_width // 2 - (incorrect_surface.get_width() // 2), 0))
    game_display.blit(answer_surface, (display_width // 2 - (answer_surface.get_width() // 2),
                                       incorrect_surface.get_height()))


# main game loop, game is a GameState object
def game_loop(game):
    gameExit = False
    background_change_timer = 0
    valid_colour = white

    user_has_typed = False
    start_time = 0
    complete_time = 0

    # 0 for starting stage, 1 if last guess was correct, 2 if it was incorrect
    last_guess = 0

    progress_font = pygame.font.Font('fonts/arial.ttf', 40)
    correctness_count_font = pygame.font.Font('fonts/arial.ttf', 40)
    correctness_percent_font = pygame.font.Font('fonts/arial.ttf', 40)
    timer_font = pygame.font.Font('fonts/arial.ttf', 40)
    correct_font = pygame.font.Font('fonts/arial.ttf', 80)
    incorrect_font = pygame.font.Font('fonts/arial.ttf', 80)
    answer_font = pygame.font.Font('fonts/arial.ttf', 40)


    # main game loop
    while not gameExit:

        completed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            elif event.type == pygame.KEYDOWN:
                if not user_has_typed:
                    user_has_typed = True
                    start_time = pygame.time.get_ticks()
                if event.key == pygame.K_RETURN and game.num_entered == word_length and not game.completed:
                    completed = True
                elif event.key == pygame.K_BACKSPACE:
                    game.delete_letter()
                elif event.unicode.isalpha():
                    game.enter_letter(event.unicode)

        # advance the game if completed, as well as verify if the guess was correct
        if completed:
            if game.verify():
                valid_colour = correct_green
                last_guess = 1
            else:
                valid_colour = incorrect_red
                last_guess = 2
            background_change_timer = 30
            game.advance()

        # change the background colour after a correct or incorrect guess
        if background_change_timer > 0:
            game_display.fill(valid_colour)
            background_change_timer -= 1
        else:
            game_display.fill(white)

        # draw the keyword area
        if word_length % 2 == 1:
            x = (display_width // 2) - (letter_width // 2)
        else:
            x = display_width // 2

        x -= (word_length // 2) * letter_width
        y = (display_height * 0.4) - letter_height

        for i in range(word_length):
            draw_letter(game.keyword[i], game.answer_list[game.counter][1][i], x, y)
            x += letter_width

        # draw the user input area, including the letters they have typed
        if word_length % 2 == 1:
            x = (display_width // 2) - (letter_width // 2)
        else:
            x = display_width // 2

        x -= (word_length // 2) * letter_width
        y = (display_height * 0.8) - letter_height

        for i in range(word_length):
            if i >= game.num_entered:
                draw_blank(x, y)
            else:
                draw_letter(game.entered_letters[i], "w", x, y)
            x += letter_width

        draw_progress_counter(progress_font, game.counter, game.total_answers)
        draw_correctness_indicator(correctness_count_font, correctness_percent_font, game.num_correct,
                                   game.counter)

        if last_guess == 1:
            draw_correct_guess(correct_font)
        elif last_guess == 2:
            draw_incorrect_guess(incorrect_font, answer_font, game.answer_list[game.counter - 1][0])

        # stop timer when game is done
        if game.completed and complete_time == 0:
            complete_time = pygame.time.get_ticks()

        if complete_time > 0:
            play_time = complete_time - start_time
        elif start_time > 0:
            play_time = pygame.time.get_ticks() - start_time
        else:
            play_time = 0
        draw_timer(timer_font, play_time)

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':

    # read data from the input file
    f = open(input_file, "r")

    input_list = f.readlines()

    f.close()

    # store the first line of the input file as the keyword
    keyword = input_list[0].strip()

    # store the rest of the lines of the input file as answer/data tuples
    answer_list = []
    for i in range(1, len(input_list)):
        answer_input = input_list[i].strip().split(",")
        answer_list.append((answer_input[1], answer_input[0]))

    random.shuffle(answer_list)

    game = GameState(keyword, answer_list)
    pygame.init()

    pygame.event.set_blocked(None)
    pygame.event.set_allowed(pygame.KEYUP)
    pygame.event.set_allowed(pygame.KEYDOWN)
    pygame.event.set_allowed(pygame.QUIT)

    for alpha in alphabet:
        image_dict[alpha + "w"] = pygame.image.load("letters/" + alpha + "w.png")
        image_dict[alpha + "b"] = pygame.image.load("letters/" + alpha + "b.png")
        image_dict[alpha + "y"] = pygame.image.load("letters/" + alpha + "y.png")
        image_dict[alpha + "g"] = pygame.image.load("letters/" + alpha + "g.png")

    game_loop(game)
    pygame.quit()
    quit()
