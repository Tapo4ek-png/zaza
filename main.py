import pygame
import random

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Виселица')
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
hangman_pics = [pygame.image.load(f'rsc/{i}.png') for i in range(7)]

def get_word(qwe):
    with open('rsc/words.txt', 'r', encoding='utf-8') as file:
        words = [word.strip() for word in file if len(word.strip()) in qwe]
    return random.choice(words).upper()

def display_message(message):
    pygame.time.delay(500)
    screen.fill(WHITE)
    font = pygame.font.SysFont(None, 36)
    text = font.render(message, True, BLACK)
    screen.blit(text, (10, 300))
    pygame.display.update()
    pygame.time.delay(2000)

def display_wrong_guesses(wrong_guesses):
    font = pygame.font.SysFont(None, 36)
    text = font.render('Неверные буквы: ' + ' '.join(wrong_guesses), True, BLACK)
    screen.blit(text, (10, 550))

def game(qwe):
    running = True
    word = get_word(qwe)
    guessed = ['_' for _ in word]
    wrong_guesses = []
    hangman_status = 0
    game_started = True

    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    letter = event.unicode.upper()
                    if letter in word:
                        for i, ltr in enumerate(word):
                            if ltr == letter:
                                guessed[i] = letter
                    else:
                        if letter not in wrong_guesses:
                            wrong_guesses.append(letter)
                        hangman_status += 1
                    if hangman_status == 6 or '_' not in guessed:
                        running = False

        font = pygame.font.SysFont(None, 48)
        display_word = ' '.join(guessed)
        text = font.render(display_word, True, BLACK)
        screen.blit(text, (400, 200))

        screen.blit(hangman_pics[hangman_status], (150, 100))

        display_wrong_guesses(wrong_guesses)

        if hangman_status == 6:
            display_message('Вы проиграли! Загаданое слово было: ' + word)
            running = False
        if '_' not in guessed:
            display_message('Вы выиграли! Загаданое слово было: ' + word)
            running = False

        pygame.display.update()

def menu():
    menu_font = pygame.font.SysFont(None, 48)
    running = True
    qwe_ranges = {
        '1': range(3, 5),
        '2': range(5, 7),
        '3': range(7, 11)
    }
    qwe = qwe_ranges['1']

    while running:
        screen.fill(WHITE)
        choice = menu_font.render('Выберите уровень сложности:', True, BLACK)
        text_easy = menu_font.render('1 - Легко (3-4 буквы)', True, BLACK)
        text_medium = menu_font.render('2 - Средне (5-6 букв)', True, BLACK)
        text_hard = menu_font.render('3 - Сложно (7-10 букв)', True, BLACK)
        screen.blit(choice, (170, 20))
        screen.blit(text_easy, (225, 150))
        screen.blit(text_medium, (225, 250))
        screen.blit(text_hard, (225, 350))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.unicode in ['1', '2', '3']:
                    game(qwe_ranges[event.unicode])

menu()
pygame.quit()