#!/usr/bin/python

import random
import pygame
from pygame.locals import *
from dataclasses import dataclass, field
import numpy as np


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


VERSION = Version(0, 1, 1, "a")

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


class Ball(pygame.sprite.Sprite):
    def __init__(self, background_color=(255, 255, 255, 255)):
        pygame.sprite.Sprite.__init__(self)

        # pygame Konfiguration: Jedes Objekt, was von 'pygame.sprite.Sprite'
        # erbt, benötigt ein self.image und self.rect Objekt
        self.image = pygame.Surface([18, 18])
        self.rect = self.image.get_rect()
        self.ball_color = self._generate_ball_color()

        self.image.fill(background_color)

        self.ball_radius = 7

        ball_center_coords = (self.rect.centerx, self.rect.centery)
        self.drawn_ball = pygame.draw.circle(
            self.image,
            self.ball_color,
            ball_center_coords,
            self.ball_radius,
        )

        """
        Der Ball bewegt sich 2-Dimensional. Das bedeutet, anders
        als bei den "Schlägern" (der 'Player'-Klasse), kann der
        Ball wie in einem karthesischen Koordinatensystem nach
        links, rechts, oben und unten springen.

        Das numpy array vereinfacht die spätere Berechnung des
        Einfalls-, sowie Ausfallswinkels (Reflexionsgesetz).
        """
        #                      x  y Achsen
        #                      |  |
        #                      v  v
        self.speed = np.array([5, 1])
        self.first_serve()

    def _generate_ball_color(self):
        # Google: Python List comprehension
        return [random.randint(0, 255) for _ in range(3)]

    # Macht den ersten Aufschlag in eine zufällige Richtung
    def first_serve(self):
        self.speed = np.array([5, 1])

        # Erstellt ein numpy array mit zwei Einträgen und wählt zufällig
        # aus den beiden Werten aus. Die Variable 'y_angle' gibt den Winkel des
        # ersten Aufschlages wieder. Je höher der Wert, desto 'steiler' der Aufschlag.
        #   Richtung: links, rechts (x-Achse) ---+              +--- Richtung: oben, unten (y-Achse)
        #                                        |              |
        #                                        v              v
        #                     _________________________   _______________________
        #                    |                         | |                       |
        direction = np.array([np.random.choice([-1, 1]), np.random.normal(scale=4.5)])
        #                                                np.random.normal vvv
        # https://numpy.org/doc/stable/reference/random/generated/numpy.random.normal.html

        """
        Multipliziert beide numpy arrays miteinander (Google: numpy broadcasting)
        Dabei gilt folgende Logik:

       y
       ▲
 x:neg │ x:pos        Wenn also die Instanz-Variable (deshalb auch das >self.<) 'self.speed'
 y:neg │ y:neg        einen positiven x-Wert (der erste Wert self.speed[0]) und einen negativen 
       │              y-Wert hat, fliegt der Ball nach oben rechts. Links in der Darstellung sind
◄──────┼───────►x     alle vier möglichen Richtungen aufgezeigt.
       │
 x:neg │ x:pos        Bsp: self.speed hat die Werte 
 y:pos │ y:pos                              self.speed[0] = -5
       │                                    self.speed[1] =  1
       ▼                   dann fliegt der Ball nach unten links. 
                           Es werden mit der Multiplikation somit nur die Vorzeichen verändert.
        """
        self.speed[0] *= direction[0]
        self.speed[1] = direction[1]

    def move(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]


class Matchfield:
    def __init__(self, main_window, ball_count=1):
        self.main_window = main_window

        self.balls = [Ball() for _ in range(0, ball_count)]

        # Google: Python Variable encapsulation
        self._redraw_field()

        self.game_object_sprites = pygame.sprite.Group()
        self.game_object_sprites.add(self.balls)

    def _redraw_field(self):
        # Google: Hex Color Picker
        # Farbzusammenstellung: Rot, Grün, Blau (Werte zwischen 0 und 255)
        background_color_rgb = (26, 62, 102)
        self.main_window.fill(background_color_rgb)

    def move_ball(self, ball):
        """
        |                     |   Der Ausdruck auf der rechten Seite gibt einen booleschen
        |  <------ ° ------>  |   Wert zurück (True/False). Dieser Zeigt an, ob der Ball
        |                     |   die rechte oder linke Wand berührt hat.
        """
        right_wall_collision = self.main_window.get_rect().right < ball.rect.right
        left_wall_collision = self.main_window.get_rect().left > ball.rect.left

        """
        _________.______________   Hier gilt wie oben beschrieben, die gleiche Logik.
        .      .  . ^              Diesmal wird jedoch geschaut, ob der Ball über
         .    .     °              Bande gespielt wurde.
          .  .      v              Dadurch wird der y-Wert in der 'Ball.speed' Variable
        ____.___________________   mit -1 multiplizert (Vorzeichen wird umgekehrt).
        """
        top_wall_collision = self.main_window.get_rect().top > ball.rect.top
        bottom_wall_collision = self.main_window.get_rect().bottom < ball.rect.bottom

        # Hier werden die Teilergebnise aus den beiden oberen Ausdrücken
        # zu einem Ergebnis durch ein OR zusammengefasst
        # Google: Logikgatter
        top_bot_wall_collision = top_wall_collision or bottom_wall_collision

        if right_wall_collision:
            self._reset_game()

        elif left_wall_collision:
            self._reset_game()

        elif top_bot_wall_collision:
            ball.speed *= np.array([1, -1])

        ball.move()

    def _reset_game(self):
        self._position_ball()

    def _position_ball(self):
        for ball in self.balls:
            ball.rect.centerx = self.main_window.get_rect().centerx
            ball.rect.centery = self.main_window.get_rect().centery
            ball.first_serve()

    def _redraw_field(self):
        # Google: Hex Color Picker
        # Farbzusammenstellung: Rot, Grün, Blau (Werte zwischen 0 und 255)
        background_color_rgb = (26, 62, 102)
        self.main_window.fill(background_color_rgb)

    def run_match(self):
        self._redraw_field()  # Sollte zu Anfang der 'Game-Loop' stehen

        for ball in self.balls:
            self.move_ball(ball)

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
