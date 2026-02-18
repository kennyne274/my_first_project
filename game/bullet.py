import pygame
import os

class Bullet(pygame.sprite.Sprite):
    """총알을 관리하는 클래스"""

    def __init__(self, ai_game):
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings

        base_path = os.path.dirname(__file__)
        bullet_path = os.path.join(base_path, "image", "bullet.png")

       
        self.image = pygame.image.load(bullet_path)

        self.rect = self.image.get_rect()

        # 총알 시작 위치 = 우주선 중앙 상단
        self.rect.midbottom = ai_game.ship.rect.midtop

        self.y = float(self.rect.y + 50) 

    def update(self):
        """총알을 위로 이동"""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y 

    def draw(self):
        self.screen.blit(self.image, self.rect)
