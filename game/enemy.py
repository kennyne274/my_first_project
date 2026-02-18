
import pygame
import os

class Enemy(pygame.sprite.Sprite):
    """적군 함대 클래스"""

    def __init__(self, ai_game):
        """적군을 초기화 하고 시작 위치를 설정합니다"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        base_path = os.path.dirname(__file__)
        alien_path = os.path.join(base_path, "image", "enemy.png")

        self.image = pygame.image.load(alien_path).convert_alpha()
        self.rect = self.image.get_rect()

    
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

       
        self.x = float(self.rect.x)

    def update(self):
        """현재 방향으로 이동"""
        self.x += self.settings.enemy_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """화면 끝에 닿았는지 확인"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
