import pygame
from sys import exit
from pong import Pong
from settings import *


class Game:

    def __init__(self):

        self.print_commands()
        mode = self.server_client_setup()

        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGTH))
        pygame.display.set_caption('Pong')
        self.clock = pygame.time.Clock()

        self.pong = Pong(mode)

    def server_client_setup(self):

        mode = None
        while mode is None:
            print("""
Server or client mode ?
1: local
2: server (online mode)
3: client (online mode)""")
            mode = input()
            if mode == '1':
                mode = 'local'

                # TODO: setup socket here

            elif mode =='2':
                mode = 'server'

                # TODO: setup socket here

            elif mode =='3':
                mode = 'client'

                # TODO: setup socket here

            else:
                print("Please enter 1 or 2 or 3.")
                mode = None
        return mode

    def print_commands(self):
        print("""
Commands:
- Use left and right key for player 1
- Use q and d key for player 2 (local mode)""")

    def run(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.screen.fill('black')
            self.pong.run()
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == '__main__':

    game = Game()
    game.run()
