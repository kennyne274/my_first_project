import pygame
import os

class Ship(pygame.sprite.Sprite):
    """우주선을 관리하는 클래스"""
    def __init__(self, ai_game):
        super().__init__()
        """우주선을 초기화하고 시작 위치를 설정합니다"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        base_path = os.path.dirname(__file__)
        ship_path = os.path.join(base_path, "image", "ship001.png")
        self.image = pygame.image.load(ship_path)
    
        self.rect = self.image.get_rect()
        # 우주선의 초기 위치는 화면 하단 중앙입니다.
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """움직임 플래그를 바탕으로 우주선 위치를 업데이트합니다"""
        # 좌우 이동
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed

        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # 상하 이동
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed

        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        self.rect.x = self.x
        self.rect.y = self.y


    def draw(self):
        """우주선을 현재 위치에 그립니다"""
        self.screen.blit(self.image, self.rect)
