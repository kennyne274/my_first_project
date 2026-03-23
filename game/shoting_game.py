import pygame
import random
import os
########################################################
pygame.init() # 초기화 (반드시 필요)

# 화면 크기 설정
screen_width = 820 # 가로 크기
screen_height = 700 # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("벽돌 피하기") # 게임 이름

# FPS
clock = pygame.time.Clock()

###########################################################

# 사용자 게임 초기화(배경 화면, 게임 이미지, 좌표, 폰트 등)

current_path = os.path.dirname(__file__) # 현재 파일의 위치 반환
image_path = os.path.join(current_path, "image")

# 배경 만들기
background = pygame.image.load(os.path.join(image_path, "space.png"))

# 캐릭터 
character = pygame.image.load(os.path.join(image_path, "ship.png"))
character_size = character.get_rect().size # 이미지 크기를 구해옴
character_width = character_size[0] # 캐릭터의 가로 크기
character_height = character_size[1] # 캐릭터의 세로 크기
character_x_pos = (screen_width / 2) - (character_width / 2) # 화면 가로 중앙에 위치
character_y_pos = screen_height - character_height # 화면 하단에 위치

# 적

enemy= pygame.image.load(os.path.join(image_path, "brick.png"))# 캐릭터의 가로 크기
enemy_size = enemy.get_rect().size # 이미지 크기를 구해옴
enemy_width = enemy_size[0] # 캐릭터의 가로 크기
enemy_height = enemy_size[1] # 캐릭터의 세로 크기
enemy_x_pos = random.randint(0, screen_width - enemy_width)
enemy_y_pos = 0 + enemy_height # 화면 상단에 위치

# 이동할 좌표 
to_x = 0
to_y = 0

# 이동 속도
character_speed = 0.6
enemy_speed = 10

# 점수
score = 0

# 수명
lives = 3

# 폰트 정의
game_font = pygame.font.Font(None, 40) # 폰트 객체 생성(폰트, 크기)

# 총알 만들기
bullet = pygame.image.load(os.path.join(image_path, "bullet.png"))
bullet_size = bullet.get_rect().size # 이미지 크기를 구해옴
bullet_width = bullet_size[0] 

# 총알은 한 번에 여러 발 발사 가능
bullets = []

# 총알 속도
bullet_speed = 10
bullet_to_remove = -1

# 이벤트 루프
running = True # 게임이 진행중인가?
while running:
    dt = clock.tick(60) # 게임 화면당 초당 프레임수 설정

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get(): # 어떤 이벤트가 발생하였는가?
        if event.type == pygame.QUIT: # 창이 닫히는 이벤트가 발생하였는가?
            running = False # 게임이 진행 중이 아님

        if event.type == pygame.KEYDOWN:  # 키가 눌러졌는지 확인
            if event.key == pygame.K_F1: # F1키를 누르면 풀스크린 모드로 전환
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
            if event.key == pygame.K_ESCAPE: # ESC키를 누르면 화면을 원래대로 전환
                screen = pygame.display.set_mode((screen_width, screen_height))
            
            if event.key == pygame.K_LEFT: # 캐릭터를 왼쪽으로
                to_x -= character_speed
            elif event.key == pygame.K_RIGHT: # 캐릭터를 오른쪽으로
                to_x += character_speed
            elif event.key == pygame.K_UP: # 캐릭터를 위로
                to_y -= character_speed
            elif event.key == pygame.K_DOWN: # 캐릭터를 아래로
                to_y += character_speed
            elif event.key == pygame.K_SPACE: # 스페이스키 누르면 총알 발사
                bullet_x_pos = character_x_pos + (character_width / 2) - (bullet_width / 2)
                bullet_y_pos = character_y_pos - character_height
                bullets.append([bullet_x_pos, bullet_y_pos])
            
            
        if event.type == pygame.KEYUP: # 키를 뗐을 때
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y = 0
            
    character_x_pos += to_x * dt
    character_y_pos += to_y * dt

    # 가로 경계값 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos  > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 세로 경계값 처리
    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos > screen_height - character_height:
        character_y_pos = screen_height - character_height

    enemy_y_pos += enemy_speed

    if enemy_y_pos > screen_height:
        enemy_y_pos = 0
        enemy_x_pos = random.randint(0, screen_width - enemy_width)

    # 총알 위치 조정
    bullets = [[b[0], b[1] - bullet_speed] for b in bullets] # 총알 위치를 위로

    # 범위를 벗어난 총알 제거하기
    bullets = [[b[0], b[1]] for b in bullets if b[1] > 0]

    # 충돌 처리를 위한 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos 

 
    # 충돌 체크
    if character_rect.colliderect(enemy_rect):
        lives -= 1

        enemy_y_pos = 0
        enemy_x_pos = random.randint(0, screen_width - enemy_width)

        if lives <= 0:
            running = False

    for bullet_idx, bullet_val in enumerate(bullets):
        bullet_x_pos = bullet_val[0]
        bullet_y_pos = bullet_val[1]

        # 총알 rect 정보 업데이트
        bullet_rect = bullet.get_rect()
        bullet_rect.left = bullet_x_pos
        bullet_rect.top = bullet_y_pos

        # 충돌 체크
        if bullet_rect.colliderect(enemy_rect):
            bullet_to_remove = bullet_idx
            enemy_y_pos = 0
            enemy_x_pos = random.randint(0, screen_width - enemy_width)
            score += 1

    # 총알 제거
    if bullet_to_remove > -1:
        del bullets[bullet_to_remove]
        bullet_to_remove = -1

 
    # 화면에 그리기
    screen.blit(background, (0, 0))
    screen.blit(character, (character_x_pos, character_y_pos))
    screen.blit(enemy, (enemy_x_pos, enemy_y_pos))
    for bullet_x_pos, bullet_y_pos in bullets:
        screen.blit(bullet, (bullet_x_pos, bullet_y_pos))

    score_text = game_font.render(f"SCORE : {score}  LIFE : {lives}", True, (255,255,0))
    screen.blit(score_text, (10, 10))


    pygame.display.update() # 게임 화면 업데이트

# 종료 전 1초 동안 대기
pygame.time.delay(2000)
# 게임 종료
pygame.quit()
