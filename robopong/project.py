#!/usr/bin/env python3

import pygame


class Pong:
    def __init__(self):
        pygame.init()
        self.upload_images()
        self.new_game()

        self.m = 0
        self.n = 5

        self.x = 640 - self.robot.get_width()
        self.y = 5

        self.a = 320 - self.ball.get_width() / 2
        self.b = 240 - self.ball.get_height() / 2

        self.velocity1 = 5
        self.velocity2 = 5

        self.counter1 = 0
        self.counter2 = 0

        self.font = pygame.font.SysFont("Arial", 24)

        self.textpos1x = 130
        self.textpos2x = 640 - 210

        pygame.mixer.init()

        self.wallsound = pygame.mixer.Sound("sounds/beep-walls.mp3")
        self.robotsound = pygame.mixer.Sound("sounds/beep-robots.mp3")
        self.bordersound = pygame.mixer.Sound("sounds/beep-warning.mp3")

        self.loop()


    def upload_images(self):
        self.robot = pygame.image.load("images/robot.png")
        self.ball = pygame.image.load("images/ball.png")


    def new_game(self):
        self.window = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.title = pygame.display.set_caption("RoboPong")


    def repositioning(self):
        self.a = 320 - self.ball.get_width() / 2
        self.b = 240 - self.ball.get_height() / 2


    def rects_listener(self):
        self.robot_rect1 = self.robot.get_rect(topleft=(self.m, self.n))
        self.robot_rect2 = self.robot.get_rect(topleft=(self.x, self.y))
        self.ball_rect = self.ball.get_rect(topleft=(self.a, self.b))


    def moving_player1(self, up: bool, down: bool):
        if up and not self.n - 48 <= 0:
            self.n -= 48
        if up and self.n <= 0:
            pass
        if down and not self.n + self.robot.get_height() + 48 >= 480:
            self.n += 48
        if down and self.n + self.robot.get_height() >= 480:
            pass


    def moving_player2(self, up: bool, down: bool):
        if up and not self.y - 48 <= 0:
            self.y -= 48
        if up and self.y <= 0:
            pass
        if down and not self.y + self.robot.get_height() + 48 >= 480:
            self.y += 48
        if down and self.y + self.robot.get_height() >= 480:
            pass


    def moving_ball(self):
        if self.velocity1 > 0 and self.a + self.ball.get_width() >= 640:
            self.velocity1 = -self.velocity1
            self.counter1 += 1
            self.bordersound.play()
            self.repositioning()
        if self.velocity1 < 0 and self.a <= 0:
            self.velocity1 = -self.velocity1
            self.counter2 += 1
            self.bordersound.play()
            self.repositioning()

        if self.velocity2 > 0 and self.b + self.ball.get_height() >= 480:
            self.wallsound.play()
            self.velocity2 = -self.velocity2
        if self.velocity2 < 0 and self.b <= 0:
            self.wallsound.play()
            self.velocity2 = -self.velocity2

        if pygame.Rect.colliderect(self.robot_rect1, self.ball_rect):
            self.robotsound.play()
            self.velocity1 = -self.velocity1
        if pygame.Rect.colliderect(self.robot_rect2, self.ball_rect):
            self.robotsound.play()
            self.velocity1 = -self.velocity1


    def draw_elements(self):
        self.window.fill((0, 0, 0))

        self.window.blit(self.robot, (self.x, self.y))
        self.window.blit(self.robot, (self.m, self.n))
        self.window.blit(self.ball, (self.a, self.b))

        self.text1 = self.font.render(
            "Score: " + str(self.counter1), True, (255, 255, 0)
        )
        self.text2 = self.font.render(
            "Score: " + str(self.counter2), True, (255, 255, 0)
        )

        self.window.blit(self.text1, (self.textpos1x, 15))
        self.window.blit(self.text2, (self.textpos2x, 15))

        pygame.display.flip()


    def event_listener(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.moving_player1(True, False)
                if event.key == pygame.K_s:
                    self.moving_player1(False, True)
                if event.key == pygame.K_UP:
                    self.moving_player2(True, False)
                if event.key == pygame.K_DOWN:
                    self.moving_player2(False, True)
                if event.key == pygame.K_ESCAPE:
                    exit()

            if event.type == pygame.QUIT:
                exit()


    def loop(self):
        while True:
            self.event_listener()
            self.draw_elements()
            self.rects_listener()
            self.moving_ball()
            self.a += self.velocity1
            self.b += self.velocity2
            self.clock.tick(60)


if __name__ == "__main__":
    Pong()
