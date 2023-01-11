#!/usr/bin/python

import pygame
from pygame.locals import *
import numpy as np
from enum import Enum, unique, auto

WINDOW_WIDTH = 1024  # width of the game window
WINDOW_HEIGHT = 768  # height of the game window


@unique
class PlayerSide(Enum):
    LEFT = auto()
    RIGHT = auto()


class Application:
    def __init__(self, window_width, window_height, caption="Codecentric: Pong"):
        window_size = (window_width, window_height)
        self.main_window = pygame.display.set_mode(window_size)

        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()

        self.isRunning = False


class Player(pygame.sprite.Sprite):
    def __init__(self, side_of_field):
        pygame.sprite.Sprite.__init__(self)

        self.score = 0
        self.side = side_of_field

        self.image = pygame.Surface([10, 100])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()

        self.speed = 8

    def position(self, move_px):
        self.rect.y += move_px


class Ball(pygame.sprite.Sprite):
    def __init__(self, hintergrundfarbe=(255, 0, 0)):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([18, 18])
        self.rect = self.image.get_rect()
        self.ball_color = hintergrundfarbe

        self.image.fill((255, 255, 255))

        self.ball_radius = 7

        ball_center_coords = (self.rect.centerx, self.rect.centery)
        self.drawn_ball = pygame.draw.circle(
            self.image,
            self.ball_color,
            ball_center_coords,
            self.ball_radius,
        )

        self.speed = np.array([5, 1])
        self.first_serve()

    # Macht den ersten Aufschlag in eine zufällige Richtung
    def first_serve(self):
        self.speed = np.array([5, 1])

        direction = np.array([np.random.choice([-1, 1]), np.random.normal(scale=4.5)])

        self.speed[0] *= direction[0]
        self.speed[1] = direction[1]

    def move(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]


class Matchfield:
    def __init__(self, main_window, ball_count=1, hintergrundfarbe=(255, 255, 0)):
        self.main_window = main_window
        self.hintergrundfarbe = hintergrundfarbe

        self.balls = [Ball() for _ in range(0, ball_count)]

        self.player_left = Player(PlayerSide.LEFT)
        self.player_right = Player(PlayerSide.RIGHT)

        self._redraw_field()

        self.game_object_sprites = pygame.sprite.Group()
        self.game_object_sprites.add(self.balls, self.player_left, self.player_right)

    def move_ball(self, ball):
        right_wall_collision = self.main_window.get_rect().right < ball.rect.right
        left_wall_collision = self.main_window.get_rect().left > ball.rect.left

        paddle1_collision = self.player_left.rect.colliderect(ball.rect)
        paddle2_collision = self.player_right.rect.colliderect(ball.rect)

        top_wall_collision = self.main_window.get_rect().top > ball.rect.top
        bottom_wall_collision = self.main_window.get_rect().bottom < ball.rect.bottom

        top_bot_wall_collision = top_wall_collision or bottom_wall_collision

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
        self._position_players()
        self._position_ball()

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
        self.main_window.fill(self.hintergrundfarbe)

    def run_match(self):
        self._redraw_field()

        for ball in self.balls:
            self.move_ball(ball)

        self.move_player()

        self.game_object_sprites.draw(self.main_window)

        pygame.display.flip()


def main():
    pygame.init()

    app = Application(WINDOW_WIDTH, WINDOW_HEIGHT)
    matchfield = Matchfield(app.main_window, ball_count=30)

    app.isRunning = True

    while app.isRunning:
        app.clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app.isRunning = False

        matchfield.run_match()


if __name__ == "__main__":
    main()
