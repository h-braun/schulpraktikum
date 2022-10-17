#!/usr/bin/python

from enum import Enum, unique, auto
import random
import os
import pathlib
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


VERSION = Version(0, 2, 0, "a")

WINDOW_WIDTH = 1024  # width of the game window
WINDOW_HEIGHT = 768  # height of the game window

_DEBUG_MODE = True

# Google: Enumeration
@unique
class PlayerSide(Enum):
    LEFT = auto()
    RIGHT = auto()


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


# Google: Objektorientierte Vererbung
# Google: Python class inheritance
class Player(pygame.sprite.Sprite):
    def __init__(self, side_of_field):
        pygame.sprite.Sprite.__init__(self)

        self.score = 0
        self.side = side_of_field

        # pygame Konfiguration: Jedes Objekt, was von 'pygame.sprite.Sprite'
        # erbt, benötigt ein self.image und self.rect Objekt
        # Einstellungen, um das 'Sprite' Objekt darzustellen
        self.image = pygame.Surface([10, 100])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()

        self.speed = 8

    def position(self, move_px):
        self.rect.y += move_px


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

        self.player_left = Player(PlayerSide.LEFT)
        self.player_right = Player(PlayerSide.RIGHT)

        # Google: Python Variable encapsulation
        self._redraw_field()

        self.game_object_sprites = pygame.sprite.Group()
        self.game_object_sprites.add(self.balls, self.player_left, self.player_right)

        self.debugger = None

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

        # Falls der Ball einen Schläger trifft, soll sich die "Flugrichtung" des Balles
        # umkehren. Das beudetet, wir multiplizieren diesmal den x-Wert der Variable
        # 'Ball.speed'.
        paddle1_collision = self.player_left.rect.colliderect(ball.rect)
        paddle2_collision = self.player_right.rect.colliderect(ball.rect)

        # Hier werden die Teilergebnise aus den beiden oberen Ausdrücken
        # zu einem Ergebnis durch ein OR zusammengefasst
        # Google: Logikgatter
        top_bot_wall_collision = top_wall_collision or bottom_wall_collision

        # Wie oben, Zusammenfassung der Teilergebnisse, da das Vorgehen unabhängig davon ist,
        # welchen Schläger der Ball berührt.
        paddle_collision = paddle1_collision or paddle2_collision

        if right_wall_collision:
            self.player_left.score += 1
            self._reset_game()

        elif left_wall_collision:
            self.player_right.score += 1
            self._reset_game()

        elif top_bot_wall_collision:
            ball.speed *= np.array([1, -1])

        elif paddle_collision:
            # Google: Ternary Operator
            y_angle_sign = np.sign(ball.speed[1]) if np.sign(ball.speed[1]) else 1

            strike_angle = np.random.normal(scale=6.5)

            ball.speed[0] += 1 * np.sign(ball.speed[0])
            ball.speed[0] *= -1
            ball.speed[1] = strike_angle * y_angle_sign

        ball.move()

    def move_player(self):
        if pygame.key.get_pressed()[pygame.K_w]:
            move_player_px = self.player_left.speed * -1
            self.player_left.position(move_player_px)

        if pygame.key.get_pressed()[pygame.K_s]:
            move_player_px = self.player_left.speed
            self.player_left.position(move_player_px)

        if pygame.key.get_pressed()[pygame.K_UP]:
            move_player_px = self.player_right.speed * -1
            self.player_right.position(move_player_px)

        if pygame.key.get_pressed()[pygame.K_DOWN]:
            move_player_px = self.player_right.speed
            self.player_right.position(move_player_px)

    def _reset_game(self):
        self._position_ball()
        self._position_players()

    def _position_ball(self):
        for ball in self.balls:
            ball.rect.centerx = self.main_window.get_rect().centerx
            ball.rect.centery = self.main_window.get_rect().centery
            ball.first_serve()

    def _position_players(self):
        move_px_from_wall = 50

        self.player_left.rect.centerx = (
            self.main_window.get_rect().left + move_px_from_wall
        )

        self.player_right.rect.centerx = (
            self.main_window.get_rect().right - move_px_from_wall
        )

        self.player_left.rect.centery = self.main_window.get_rect().centery

        self.player_right.rect.centery = self.main_window.get_rect().centery

    def _redraw_field(self):
        # Google: Hex Color Picker
        # Farbzusammenstellung: Rot, Grün, Blau (Werte zwischen 0 und 255)
        background_color_rgb = (26, 62, 102)
        self.main_window.fill(background_color_rgb)

    def run_match(self):
        self._redraw_field()  # Sollte zu Anfang der 'Game-Loop' stehen

        for ball in self.balls:
            self.move_ball(ball)

        self.move_player()

        if not self.debugger is None:
            if self.debugger.showOnScreen:
                self.debugger.show_fps()
                self.debugger.show_coords()
                self.debugger.show_paddle_coord()
                self.debugger.show_version()

        self.game_object_sprites.draw(self.main_window)

        # Erneuert das gesamte Fenster mit den bewegten Sprites, Fonts etc.
        pygame.display.flip()  # Sollte zum Ende der 'Game-Loop' stehen


class Debugger:
    def __init__(self, app, match):
        self.app = app
        self.match = match
        self.showOnScreen = False
        self.font = pygame.font.SysFont("Consolas", 12)
        self.font_color = (41, 255, 144)
        self.font_bg = (0, 0, 0, 1)

        self.refresh_tick = 0
        self.debug_coords = (0, 0)

    def show_fps(self):
        show_at_coordinates = (0, 0)
        fps_text = str(int(self.app.clock.get_fps()))

        fps_counter = self.font.render(fps_text, True, self.font_color, self.font_bg)
        self.app.main_window.blit(fps_counter, show_at_coordinates)

    def show_coords(self):
        self.refresh_tick += 1
        show_at_coordinates = (0, 12)
        if self.refresh_tick > 3:
            coords_as_str = f"Ball 0 at (x: {self.match.balls[0].rect.centerx} | y: {self.match.balls[0].rect.centery}) Speed: {self.match.balls[0].speed[0]} | Angle: {self.match.balls[0].speed[1]}"
            self.debug_coords = (
                self.match.balls[0].rect.centerx,
                self.match.balls[0].rect.centery,
            )
            self.refresh_tick = 0
        else:
            coords_as_str = f"Ball 0 at (x: {self.debug_coords[0]} | y: {self.debug_coords[1]}) Speed: {self.match.balls[0].speed[0]} | Angle: {self.match.balls[0].speed[1]}"

        coords = self.font.render(
            str(coords_as_str), True, (41, 255, 144), (0, 0, 0, 1)
        )

        self.app.main_window.blit(coords, show_at_coordinates)

    def show_paddle_coord(self):
        show_at_coordinates_left = (0, 24)

        coords_as_str_left = f"Left player: (x: {self.match.player_left.rect.centerx} | y: {self.match.player_left.rect.centery})"
        coords_left = self.font.render(
            str(coords_as_str_left), True, (41, 255, 144), (0, 0, 0, 1)
        )
        show_at_coordinates_right = (0, 36)

        coords_as_str_right = f"Right player: (x: {self.match.player_right.rect.centerx} | y: {self.match.player_right.rect.centery})"
        coords_right = self.font.render(
            str(coords_as_str_right), True, (41, 255, 144), (0, 0, 0, 1)
        )
        self.app.main_window.blit(coords_left, show_at_coordinates_left)
        self.app.main_window.blit(coords_right, show_at_coordinates_right)

    def show_version(self):
        show_at_coordinates_left = (0, 72)

        version_txt = f"Version: {VERSION}"
        version_rect = self.font.render(
            str(version_txt), True, (41, 255, 144), (0, 0, 0, 1)
        )
        self.app.main_window.blit(version_rect, show_at_coordinates_left)


def main():
    pygame.init()

    app = Application(WINDOW_WIDTH, WINDOW_HEIGHT)
    matchfield = Matchfield(app.main_window)

    # Google: Header-Guard
    # Wird häufig in der Programmierpsrache C/C++ verwendet
    if _DEBUG_MODE:
        matchfield.debugger = Debugger(app, matchfield)

    app.isRunning = True
    while app.isRunning:
        app.clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app.isRunning = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    matchfield.debugger.showOnScreen = (
                        not matchfield.debugger.showOnScreen
                    )

        matchfield.run_match()


if __name__ == "__main__":
    main()
