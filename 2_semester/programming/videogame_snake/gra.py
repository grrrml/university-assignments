import pygame
import sys
import os
import pickle
import numpy as np
from pygame.locals import *

# Konfiguracja
FPS = 15
FramePerSec = pygame.time.Clock()

pygame.init()

# EKRAN
SCREENWIDTH, SCREENHEIGHT = 600, 600
pygame.display.set_caption('Snake')
DISPLAYSURF = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), 0, 32)

# FONTY
font = pygame.font.Font(os.path.join(os.path.dirname(__file__), '.\\resources\\AnonymousPro-Regular.ttf'), 30)
font2 = pygame.font.Font(os.path.join(os.path.dirname(__file__), '.\\resources\\AnonymousPro-Regular.ttf'), 50)

# KOLORY
DARKGREEN = pygame.Color(156, 166, 86)
LIGHTGREEN = pygame.Color(160, 191, 48)
DARKGRAY = pygame.Color(38, 38, 38)
LIGHTGRAY = pygame.Color(89, 89, 89)
WHITE = pygame.Color(255, 255, 255)

# DŹWIĘKI
click_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), ".\\resources\\click.wav"))
eat_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), ".\\resources\\eat.wav"))
gameover_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), ".\\resources\\gameover.wav"))
pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), ".\\resources\\music.wav"))

# Funkcje pomocnicze
def draw_text(text, font, color, surface, x, y):
    """ Rysuje tekst """
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect(topleft=(x, y))
    surface.blit(textobj, textrect)

def centered_text(text, font, color, surface, x, y):
    """ Rysuje wyśrodkowany tekst """
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

def save_highscore(new_score):
    """ Dopisuje najlepszy wynik do pliku """
    highscores = read_highscores()
    highscores.append(new_score)
    highscores.sort(reverse=True)
    with open(os.path.join(os.path.dirname(__file__), ".\\resources\\highscores.txt"), "wb") as f:
        pickle.dump(highscores, f)

def read_highscores():
    """ Odczytuje najlepsze wyniki z pliku """
    with open(os.path.join(os.path.dirname(__file__), ".\\resources\\highscores.txt"), "rb") as f:
        return pickle.load(f)

# Funkcje główne
def main_menu():
    """ Menu główne """
    running = True
    click = False

    play_btn = pygame.Rect(200, 150, 200, 50)
    scores_btn = pygame.Rect(200, 250, 200, 50)
    quit_btn = pygame.Rect(200, 350, 200, 50)

    while running:

        DISPLAYSURF.fill(DARKGRAY)
        centered_text('Snake', font2, LIGHTGREEN, DISPLAYSURF, SCREENWIDTH // 2, 75)

        mx, my = pygame.mouse.get_pos()

        if play_btn.collidepoint((mx, my)):
            if click:
                pygame.mixer.Sound.play(click_sound)
                game()

        if scores_btn.collidepoint((mx, my)):
            if click:
                pygame.mixer.Sound.play(click_sound)
                highscores()

        if quit_btn.collidepoint((mx, my)):
            if click:
                pygame.mixer.Sound.play(click_sound)
                pygame.quit()
                sys.exit()

        pygame.draw.rect(DISPLAYSURF, LIGHTGRAY, play_btn)
        pygame.draw.rect(DISPLAYSURF, LIGHTGRAY, scores_btn)
        pygame.draw.rect(DISPLAYSURF, LIGHTGRAY, quit_btn)

        centered_text('Play', font, WHITE, DISPLAYSURF, SCREENWIDTH // 2, 175)
        centered_text('Scores', font, WHITE, DISPLAYSURF, SCREENWIDTH // 2, 275)
        centered_text('Quit', font, WHITE, DISPLAYSURF, SCREENWIDTH // 2, 375)

        click = False

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        FramePerSec.tick(FPS)

def game():
    """ Główna funkcja gry """
    running = True
    speed = FPS
    score = 0
    direction = 'RIGHT'
    gameboard = pygame.Rect(50, 150, 500, 400)
    pygame.mixer.music.play(-1)

    snake = [300, 300]

    snake_segments = [[300, 300], [290, 300], [280, 300], [270, 300]]

    apple_position = [np.random.choice(np.arange(50, 440, 10)), np.random.choice(np.arange(150, 440, 10))]

    apple = 1

    highscore = read_highscores()[0]

    while running:
        DISPLAYSURF.fill(DARKGRAY)
        pygame.draw.rect(DISPLAYSURF, LIGHTGRAY, gameboard)

        scorecolor = WHITE if score <= highscore else DARKGREEN

        centered_text('Snake', font2, LIGHTGREEN, DISPLAYSURF, SCREENWIDTH // 2, 75)
        draw_text(f'Your score: {score}', font, scorecolor, DISPLAYSURF, 50, 110)
        draw_text(f'Highscore: {highscore}', font, WHITE, DISPLAYSURF, 350, 110)

        # Obsługa sterowania
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:

                if (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != 'DOWN':
                    direction = 'UP'

                if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != 'UP':
                    direction = 'DOWN'

                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != 'RIGHT':
                    direction = 'LEFT'

                if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != 'LEFT':
                    direction = 'RIGHT'

                if event.key == pygame.K_p:
                    score += 10

                if event.key == K_ESCAPE:
                    pygame.mixer.music.stop()
                    running = False

        # Poruszanie się
        if direction == 'UP':
            snake[1] -= 10
        if direction == 'DOWN':
            snake[1] += 10
        if direction == 'LEFT':
            snake[0] -= 10
        if direction == 'RIGHT':
            snake[0] += 10

        # Rośnięcie węża, obsługa punktacji i przyspieszania
        snake_segments.insert(0, list(snake))
        if snake[0] == apple_position[0] and snake[1] == apple_position[1]:
            pygame.mixer.Sound.play(eat_sound)
            score += 1
            apple = 0

            if score % 5 == 0 and score != 0:
                speed += 5
        else:
            snake_segments.pop()

        # Pojawianie się nowego jabłka
        if not apple:
            apple_position = [np.random.choice(np.arange(50, 440, 10)), np.random.choice(np.arange(150, 440, 10))]
            apple = 1

        # Koniec gry - dotknięcie brzegu
        if snake[0] < 50 or snake[0] > 540 or snake[1] < 150 or snake[1] > 540:
            save_highscore(score)
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(gameover_sound)
            end_game()

        # Koniec gry - dotknięcie węża
        for segment in snake_segments[1:]:
            if snake[0] == segment[0] and snake[1] == segment[1]:
                save_highscore(score)
                pygame.mixer.Sound.play(gameover_sound)
                pygame.mixer.music.stop()
                end_game()

        # Rysowanie węża i owoców
        for i in range(len(snake_segments)):
            color = LIGHTGREEN if (i + 1) % 3 else DARKGREEN
            pygame.draw.rect(DISPLAYSURF, color, pygame.Rect(snake_segments[i][0], snake_segments[i][1], 10, 10))

        pygame.draw.rect(DISPLAYSURF, WHITE, pygame.Rect(apple_position[0], apple_position[1], 10, 10))

        pygame.display.update()
        FramePerSec.tick(speed)

def highscores():
    """ Ekran najlepszych wyników """
    running = True

    scores = read_highscores()

    while running:
        DISPLAYSURF.fill(DARKGRAY)

        centered_text('Highscores', font2, LIGHTGREEN, DISPLAYSURF, SCREENWIDTH // 2, 75)

        y_pos = 150
        for i in range(5):
            centered_text(str(scores[i]), font, WHITE, DISPLAYSURF, SCREENWIDTH // 2, y_pos)
            y_pos += 60

        mx, my = pygame.mouse.get_pos()

        return_btn = pygame.Rect(200, 500, 200, 50)

        if return_btn.collidepoint((mx, my)):
            if click:
                pygame.mixer.Sound.play(click_sound)
                running = False

        click = False

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.draw.rect(DISPLAYSURF, LIGHTGRAY, return_btn)
        centered_text('Return', font, WHITE, DISPLAYSURF, SCREENWIDTH // 2, 525)

        pygame.display.update()
        FramePerSec.tick(60)

def end_game():
    """ Ekran końca gry """
    click = False

    play_btn = pygame.Rect(175, 150, 250, 50)
    menu_btn = pygame.Rect(175, 250, 250, 50)
    quit_btn = pygame.Rect(200, 350, 200, 50)

    running = True

    while running:

        DISPLAYSURF.fill(DARKGRAY)
        centered_text('Game over!', font2, LIGHTGREEN, DISPLAYSURF, SCREENWIDTH // 2, 75)

        mx, my = pygame.mouse.get_pos()

        if play_btn.collidepoint((mx, my)):
            if click:
                pygame.mixer.Sound.play(click_sound)
                game()

        if menu_btn.collidepoint((mx, my)):
            if click:
                pygame.mixer.Sound.play(click_sound)
                main_menu()

        if quit_btn.collidepoint((mx, my)):
            if click:
                pygame.mixer.Sound.play(click_sound)
                pygame.quit()
                sys.exit()

        pygame.draw.rect(DISPLAYSURF, LIGHTGRAY, play_btn)
        pygame.draw.rect(DISPLAYSURF, LIGHTGRAY, menu_btn)
        pygame.draw.rect(DISPLAYSURF, LIGHTGRAY, quit_btn)

        centered_text('Play again', font, WHITE, DISPLAYSURF, SCREENWIDTH // 2, 175)
        centered_text('Main menu', font, WHITE, DISPLAYSURF, SCREENWIDTH // 2, 275)
        centered_text('Quit', font, WHITE, DISPLAYSURF, SCREENWIDTH // 2, 375)

        click = False

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        FramePerSec.tick(FPS)


if __name__ == "__main__":
    main_menu()
