from tkinter import Y
import pygame
from random import randint, choice


class Bar(pygame.sprite.Sprite):

    def __init__(self, player, width=100, thickness=10):
        super().__init__()

        self.screen = pygame.display.get_surface()

        # parameters
        y_offset = 30
        color = 'white'
        self.speed = 4
        self.player = player

        # setup keys and position
        if self.player == 1:
            self.keys = {
                'left': pygame.K_LEFT,
                'right': pygame.K_RIGHT}
            y_center = self.screen.get_height() - y_offset
        elif self.player == 2:
            self.keys = {
                'left': pygame.K_q,
                'right': pygame.K_d}
            y_center = y_offset

        self.image = pygame.Surface((width,thickness))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(
            self.screen.get_width() / 2,
            y_center
        ))

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[self.keys['left']] is True:
            self.move('left')
        if keys[self.keys['right']] is True:
            self.move('right')

    def move(self, dir):
        if dir == 'left':
            speed = - self.speed
        if dir == 'right':
            speed = self.speed
        self.rect.x += speed

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.screen.get_width():
            self.rect.right = self.screen.get_width()

    def update(self):
        self.get_input() # get input and move


class Ball(pygame.sprite.Sprite):

    def __init__(self, size=10):
        super().__init__()

        self.screen = pygame.display.get_surface()

        # parameters
        y_offset = 30
        color = 'white'
        self.speed = 4

        self.vector = pygame.math.Vector2()

        self.image = pygame.Surface((size,size))
        self.image.fill(color)
        self.rect = self.image.get_rect()

        self.reset()
    
    def reset(self):
        self.rect.center = (
            self.screen.get_width() / 2,
            self.screen.get_height() / 2
        )

        self.vector.x = randint(-10, 10)
        self.vector.y = randint(-10, 10)

        # fix: can bug if self.vector == (0,0), and avoid horizontal movement too slow
        if self.vector.x == 0:
            self.vector.x = choice([-2, 2])
        if self.vector.y in [-1, 0, 1]:
            self.vector.y = choice([-2, 2])
        self.vector = self.vector.normalize()

    def move(self, angle):
        if angle == 'horizontal':
            self.rect.x += self.vector.x * self.speed
        elif angle == 'vertical':
            self.rect.y += self.vector.y * self.speed

    def collision(self, angle, bars):
        if angle == 'horizontal':
            # on left
            if self.rect.left < 0:
                self.vector.x = - self.vector.x
                self.rect.left = - self.rect.left
            # on right
            if self.rect.right > self.screen.get_width():
                self.vector.x = - self.vector.x
                self.rect.right = self.rect.right - (self.rect.right - self.screen.get_width()) * 2
            # with bars
            if pygame.sprite.spritecollideany(self, bars) != None:
                #TODO: do better collision with bars
                self.vector.x = - self.vector.x
        elif angle == 'vertical':
            # on top
            if self.rect.top < 0:
                self.vector.y = - self.vector.y
                # TODO: score and reset ball
            # on bottom
            if self.rect.bottom > self.screen.get_height():
                self.vector.y = - self.vector.y
                # TODO: score and reset ball
            collided_bar = pygame.sprite.spritecollide(self, bars, False)
            if collided_bar != []:
                if self.vector.y > 0:
                    y_offset = self.rect.bottom - collided_bar[0].rect.top
                    self.rect.y = self.rect.y - 2 * y_offset
                elif self.vector.y < 0:
                    y_offset = collided_bar[0].rect.bottom - self.rect.top
                    self.rect.y = self.rect.y + 2 * y_offset
                self.vector.y = - self.vector.y

    def update(self, bars):
        self.move('horizontal')
        self.collision('horizontal', bars)
        self.move('vertical')
        self.collision('vertical', bars)


class Pong:

    def __init__(self, mode, bar_size=20):

        self.mode = mode
        self.screen = pygame.display.get_surface()

        # sprites groups
        self.bars = pygame.sprite.Group()
        self.ball = pygame.sprite.Group()

        self.bars.add(Bar(player=1))
        self.bars.add(Bar(player=2))
        self.ball.add(Ball())

    def run(self):
        self.bars.update()
        self.bars.draw(self.screen)
        self.ball.update(self.bars)
        self.ball.draw(self.screen)
