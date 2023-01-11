import pygame
import numpy as np
from pygame.locals import *

# Konstanten
WINDOW_HEIGHT = 1024
WINDOW_WIDTH = 768


class Application:
    def __init__(self, height, width):
        self.window_size = (height, width)
        self.main_window = pygame.display.set_mode(size=self.window_size)

        self.clock = pygame.time.Clock()

        self.isRunning = True


class Ball(pygame.sprite.Sprite):
    x_default_speed, y_default_speed = (5, 1)

    def __init__(self, hintergrundfarbe=(0, 0, 0)):
        super().pygame.sprite.Sprite.__init__()

        self.image = pygame.Surface([18, 18])
        self.rect = self.image.get_rect()

        self.ball_color = hintergrundfarbe
        print(self.rect.centerx)
        ball_radius = 7
        ball_center_coords = (self.rect.centerx, self.rect.centery)

        self.drawn_ball = pygame.draw.circle(
            self.image, self.ball_color, ball_center_coords, ball_radius
        )

        self.speed = np.array([Ball.x_default_speed, Ball.y_default_speed])

    def first_serve(self):
        self.speed = np.array([Ball.x_default_speed, Ball.y_default_speed])

        direction = np.array([np.random.choice([-1, 1]), np.random.normal(scale=4.5)])

        self.speed[0] *= direction[0]
        self.speed[1] = direction[1]

    def move(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]


class Matchfield:
    def __init__(self, main_window, ball_count=1, hintergrundfarbe=(255, 255, 0)):
        self.hauptfenster = main_window
        self.hintergrundfarbe = hintergrundfarbe

        # List comprehension
        self.balls = [
            Ball()
            for _ in range(
                0,
            )
        ]

    def _redraw_main_window(self):
        self.hauptfenster.fill(self.hintergrundfarbe)

    def run_match(self):
        self._redraw_main_window()

        pygame.display.flip()


def main():
    pygame.init()

    app = Application(WINDOW_HEIGHT, WINDOW_WIDTH)
    spielfeld = Matchfield(app.main_window)

    while app.isRunning:
        app.clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app.isRunning = False

        spielfeld.run_match()


if __name__ == "__main__":
    main()
