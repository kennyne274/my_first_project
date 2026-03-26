import pygame
import random
import os
 
# 캐릭터 이동 함수
def character_move(keys, speed):
    # 이동할 좌표
    to_x = 0
    to_y = 0

    if keys[pygame.K_LEFT]:
        to_x -= speed
    if keys[pygame.K_RIGHT]:
        to_x += speed
    if keys[pygame.K_UP]:
        to_y -= speed
    if keys[pygame.K_DOWN]:
        to_y += speed
        
    return to_x, to_y

########################################################
pygame.init() # 초기화 (반드시 필요)
pygame.mixer.init()  # 사운드 초기화

# 화면 크기 설정
screen_width = 820 # 가로 크기
screen_height = 700 # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Shooting Game") # 게임 이름

# FPS
clock = pygame.time.Clock()

###########################################################

# 사용자 게임 초기화(배경 화면, 게임 이미지, 좌표, 폰트 등)

current_path = os.path.dirname(__file__) # 현재 파일의 위치 반환
image_path = os.path.join(current_path, "image")
sound_path = os.path.join(current_path, "sound")

# 배경 만들기
background = pygame.image.load(os.path.join(image_path, "space.png"))
bg_y = 0

# 배경 음악
bgm = pygame.mixer.Sound(os.path.join(sound_path, "main.mp3"))
bgm.set_volume(0.4)  

# 효과음
shoot_sound = pygame.mixer.Sound(os.path.join(sound_path, "shoot.wav"))
hit_enemy_sound = pygame.mixer.Sound(os.path.join(sound_path, "enemy_hit.wav"))
crash_sound = pygame.mixer.Sound(os.path.join(sound_path, "crash.wav"))
gameover_sound = pygame.mixer.Sound(os.path.join(sound_path, "gameover.wav"))

# 캐릭터 
character = pygame.image.load(os.path.join(image_path, "ship.png"))
character_size = character.get_rect().size # 이미지 크기를 구해옴
character_width = character_size[0] # 캐릭터의 가로 크기
character_height = character_size[1] # 캐릭터의 세로 크기
character_x_pos = (screen_width / 2) - (character_width / 2) # 화면 가로 중앙에 위치
character_y_pos = screen_height - character_height # 화면 하단에 위치

# 적
enemy= pygame.image.load(os.path.join(image_path, "enemy.png"))# 캐릭터의 가로 크기
enemy_size = enemy.get_rect().size # 이미지 크기를 구해옴
enemy_width = enemy_size[0] # 캐릭터의 가로 크기
enemy_height = enemy_size[1] # 캐릭터의 세로 크기
enemy_x_pos = random.randint(0, screen_width - enemy_width)
enemy_y_pos = 0 + enemy_height # 화면 상단에 위치

# 폭발
explosion = pygame.image.load(os.path.join(image_path, "explosion.png"))

exploding = False
explosion_timer = 0
explosion_x = 0
explosion_y = 0

# 이동 속도
character_speed = 0.5
enemy_speed = 0.4

# 점수
score = 0

# 수명
lives = 3

# 총알 만들기
bullet = pygame.image.load(os.path.join(image_path, "bullet.png"))
bullet_size = bullet.get_rect().size # 이미지 크기를 구해옴
bullet_width = bullet_size[0] 

# 총알은 한 번에 여러 발 발사 가능
bullets = []

# 총알 속도
bullet_speed = 1
bullet_to_remove = -1

# 배경음악 시작 (-1 = 무한 반복)
bgm.play(-1)

# 이벤트 루프
running = True # 게임이 진행중인가?
while running:
    dt = clock.tick(60) # 게임 화면당 초당 프레임수 설정

    # 현재 화면의 실제 크기 가져오기 (일반/풀스크린 모두 대응)
    current_width, current_height = screen.get_size()
    # 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get(): # 어떤 이벤트가 발생하였는가?
        if event.type == pygame.QUIT: # 창이 닫히는 이벤트가 발생하였는가?
            running = False # 게임이 진행 중이 아님

        if event.type == pygame.KEYDOWN:  # 키가 눌러졌는지 확인
            if event.key == pygame.K_F1: # F1키를 누르면 풀스크린 모드로 전환
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
                # 풀스크린으로 바뀐 후 캐릭터를 중앙으로 재배치
                current_width, current_height = screen.get_size()
                character_x_pos = (current_width / 2) - (character_width / 2)
            if event.key == pygame.K_ESCAPE: # ESC키를 누르면 화면을 원래대로 전환
                screen = pygame.display.set_mode((screen_width, screen_height))

            # 스페이스키 누르면 총알 발사
            if event.key == pygame.K_SPACE: 
                bullet_x_pos = character_x_pos + (character_width / 2) - (bullet_width / 2)
                bullet_y_pos = character_y_pos - character_height
                bullets.append([bullet_x_pos, bullet_y_pos])
                shoot_sound.play()

    # 키 입력 → 이동 방향 계산
    keys = pygame.key.get_pressed()
    to_x, to_y = character_move(keys, character_speed)
         
            
    character_x_pos += to_x * dt
    character_y_pos += to_y * dt

    # 가로 경계값 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos  > current_width - character_width:
        character_x_pos = current_width - character_width

    # 세로 경계값 처리
    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos > current_height - character_height:
        character_y_pos = current_height - character_height

    enemy_y_pos += enemy_speed * dt

    if enemy_y_pos > screen_height:
        enemy_y_pos = 0
        enemy_x_pos = random.randint(0, screen_width - enemy_width)

    # 총알 위치 조정
    bullets = [[b[0], b[1] - bullet_speed * dt] for b in bullets] # 총알 위치를 위로

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
        crash_sound.play()

        enemy_y_pos = 0
        enemy_x_pos = random.randint(0, screen_width - enemy_width)

        if lives <= 0:
            bgm.stop()
            gameover_sound.play()

            # GAME OVER 텍스트
            game_over_font = pygame.font.Font(None, 180)       
            game_over_text = game_over_font.render("GAME OVER", True, (255, 50, 50))
            
            # 화면 중앙에 배치
            text_rect = game_over_text.get_rect(
                center=(current_width // 2, current_height // 2 - 60)
            )
            screen.blit(game_over_text, text_rect)

            # 최종 점수
            score_font = pygame.font.Font(None, 100)
            score_text = score_font.render(f"FINAL SCORE : {score}", True, (0, 255, 200))
            score_rect = score_text.get_rect(
                center=(current_width // 2, current_height // 2 + 40)
            )
            screen.blit(score_text, score_rect)

            # 화면 갱신
            pygame.display.flip() 
            # 3초 대기
            pygame.time.delay(3000)
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
            score += 1
            hit_enemy_sound.play()

            # 폭발 시작
            exploding = True
            explosion_timer = pygame.time.get_ticks()
            explosion_x = enemy_x_pos
            explosion_y = enemy_y_pos

            # 적 숨기기 (즉시 리스폰 안 함)
            enemy_y_pos = -100


    # 총알 제거
    if bullet_to_remove > -1:
        del bullets[bullet_to_remove]
        bullet_to_remove = -1

 
    # 화면에 그리기
    
    # 배경 화면 스크롤
    bg_y = (bg_y + 8) % screen_height
    screen.blit(background, [0, bg_y - 700])
    screen.blit(background, [0, bg_y])

    # 캐릭터와 적을 그리기
    screen.blit(character, (character_x_pos, character_y_pos))
    screen.blit(enemy, (enemy_x_pos, enemy_y_pos))
    for bullet_x_pos, bullet_y_pos in bullets:
        screen.blit(bullet, (bullet_x_pos, bullet_y_pos))

    # 폭발 중이면
    if exploding:
        screen.blit(explosion, (explosion_x, explosion_y))

        # 200ms 후 종료
        if pygame.time.get_ticks() - explosion_timer > 200:
            exploding = False

            # 적 리스폰
            enemy_y_pos = 0
            enemy_x_pos = random.randint(0, screen_width - enemy_width)
    
    # 폰트 정의
    game_font = pygame.font.Font(None, 40) # 폰트 객체 생성(폰트, 크기)
    score_text = game_font.render(f"SCORE : {score}  LIFE : {lives}", True, (255,255,0))
    screen.blit(score_text, (10, 10))


    pygame.display.update() # 게임 화면 업데이트

# 게임 종료
pygame.quit()


