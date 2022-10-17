#!/usr/bin/python

import pygame
from pygame.locals import *
from dataclasses import dataclass, field


@dataclass
class Version:
    major: int = field(default=0)
    minor: int = field(default=0)
    micro: int = field(default=1)
    dev_phase: str = field(default="alpha")

    def __repr__(self) -> str:
        return f"{self.major}.{self.minor}.{self.micro}{self.dev_phase}"

    def __str__(self) -> str:
        return self.__repr__()


# Google: constant variable
VERSION = Version(0, 0, 1, "a")
WINDOW_WIDTH = 1024  # width of the game window
WINDOW_HEIGHT = 768  # height of the game window

# Google: Objektorientierte Klassen
class Application:
    # Google: Programming Constructor
    # Google: Python dunder methods
    #    oder statt 'dunder' auch magic methods
    # dunder ist ein aus zwei Begriffen (double und under) zusammengesetzer Fantasiename.
    # Python deklariert interne Methoden (bereits in Python selbst integriert)
    # häufig mit zwei Unterschtrichen, um dem Programmierer keine
    # 'Namen zu klauen'
    def __init__(self, window_width, window_height, caption="Codecentric: Pong"):
        window_size = (window_width, window_height)
        self.main_window = pygame.display.set_mode(window_size)

        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()

        # Zeigt an, ob das Programm in der 'Game-Loop' ausgeführt wird
        self.isRunning = False


class Matchfield:
    def __init__(self, main_window, ball_count=3):
        self.main_window = main_window

        # Google: Python Variable encapsulation
        self._redraw_field()

        self.game_object_sprites = pygame.sprite.Group()

    def _redraw_field(self):
        # Google: Hex Color Picker
        # Farbzusammenstellung: Rot, Grün, Blau (Werte zwischen 0 und 255)
        background_color_rgb = (26, 62, 102)
        self.main_window.fill(background_color_rgb)

    def run_match(self):
        self._redraw_field()  # Sollte zu Anfang der 'Game-Loop' stehen

        self.game_object_sprites.draw(self.main_window)

        # Erneuert das gesamte Fenster mit den bewegten Sprites, Fonts etc.
        pygame.display.flip()  # Sollte zum Ende der 'Game-Loop' stehen


def main():
    pygame.init()

    app = Application(WINDOW_WIDTH, WINDOW_HEIGHT)
    matchfield = Matchfield(app.main_window)

    app.isRunning = True
    while app.isRunning:
        app.clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app.isRunning = False

        matchfield.run_match()


if __name__ == "__main__":
    main()
