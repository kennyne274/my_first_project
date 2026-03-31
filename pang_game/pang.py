import pygame
import os

###########################################################

current_path = os.path.dirname(__file__) # 현재 파일의 위치 반환
image_path = os.path.join(current_path, "image")
sound_path = os.path.join(current_path, "sound")

####### 이미지 업로드########

# 배경 
background = pygame.image.load(os.path.join(image_path, "pang.png"))

# 스테이지
stage = 180

# 기회
lives = 3

# 레벨
level = 1

# 화면 크기 설정
screen_width = 1100 # 가로 크기
screen_height = 720 # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 캐릭터 
character = pygame.image.load(os.path.join(image_path, "main.png"))
character_size = character.get_rect().size # 이미지 크기를 구해옴
character_width = character_size[0] # 캐릭터의 가로 크기
character_height = character_size[1] # 캐릭터의 세로 크기
character_x_pos = (screen_width / 2) - (character_width / 2) # 화면 가로 중앙에 위치
character_y_pos = screen_height - stage # 화면 하단 스테이지 높이 
character_speed = 0.4

# 무기
bullet = pygame.image.load(os.path.join(image_path, "bullet.png"))
bullet_size = bullet.get_rect().size # 이미지 크기를 구해옴
bullet_width = bullet_size[0] 

# 공
ball_images = [
        pygame.image.load(os.path.join(image_path, "ball.png")),
        pygame.image.load(os.path.join(image_path, "ball2.png")),
        pygame.image.load(os.path.join(image_path, "ball3.png")),
        pygame.image.load(os.path.join(image_path, "ball4.png"))]
                                             

# 공 크기에 따른 최초 스피드
ball_speed_y = [-18, -16, -14, -12]

balls =[]

balls.append({
    "pos_x" : 50, # 공의 x좌표
    "pos_y" : 50, # 공의 y좌표
    "img_idx" : 0,# 공의 이미지 인덱스
    "to_x" : 3, # x축 이동 방향
    "to_y": -6,  # y축 이동 방향 # y 최초 속도
    "init_spd_y" : ball_speed_y[0]})

# 이동할 좌표
character_x = 0

def main():
    global character_x_pos, character_y_pos, character_x, lives, level
    # 게임 초기화
    pygame.init() # Initialising pygame


    # 화면 타이틀 설정
    pygame.display.set_caption("Pang") # 게임 이름

    # FPS
    clock = pygame.time.Clock()

    ###########################################################

    # 사용자 게임 초기화(배경 화면, 게임 이미지, 좌표, 폰트 등)


    # 배경 음악
    bgm = pygame.mixer.Sound(os.path.join(sound_path, "main.mp3"))
     # 효과음
    shoot_sound = pygame.mixer.Sound(os.path.join(sound_path, "shoot.wav"))
    gameover_sound = pygame.mixer.Sound(os.path.join(sound_path, "gameover.wav"))
    crash_sound = pygame.mixer.Sound(os.path.join(sound_path, "crash.wav"))
    bgm.set_volume(0.4)  

    # 배경음악 시작 
    bgm.play(-1)

    # 폰트 정의(게임 오버)
    game_over_font = pygame.font.Font(None, 180) 

    # 총알 여러발 생성
    bullets = []
    # 총알 스피드
    bullet_speed = 0.5

    # 이벤트 루프
    running = True 
    while running:
        dt = clock.tick(60) # 게임 화면당 초당 프레임수 설정
      
        # 이벤트 처리 (키보드, 마우스 등)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False 

            # 키 입력 → 이동 방향 계산              
            if event.type == pygame.KEYDOWN:  # 키가 눌러졌는지 확인
                if event.key == pygame.K_SPACE: 
                        bullet_x_pos = character_x_pos + (character_width / 2) - (bullet_width / 2)
                        bullet_y_pos = character_y_pos - character_height
                        bullets.append([bullet_x_pos, bullet_y_pos]) 
                        shoot_sound.play()  

                if event.key == pygame.K_LEFT: # 캐릭터를 왼쪽으로
                    character_x -= character_speed
                elif event.key == pygame.K_RIGHT: # 캐릭터를 오른쪽으로
                    character_x += character_speed      
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    character_x = 0
            
        character_x_pos += character_x * dt

        if character_x_pos < 0:
            character_x_pos = 0
        elif character_x_pos > screen_width - character_width:
            character_x_pos = screen_width - character_width        

      
        # 총알 위치 조정
        bullets = [[b[0], b[1] - bullet_speed * dt] for b in bullets] # 총알 위치를 위로
        # 천장에 닿은 총알 제거하기
        bullets = [[b[0], b[1]] for b in bullets if b[1] > 0]

        # 사라질 무기, 공 정보 저장 변수
        bullet_to_remove = -1
        ball_to_remove = -1

        # 공 위치 정의
        for ball_idx, ball_val in enumerate(balls):
            ball_pos_x = ball_val["pos_x"]
            ball_pos_y = ball_val["pos_y"]
            ball_img_idx = ball_val["img_idx"]

            ball_size = ball_images[ball_img_idx].get_rect().size
            ball_width = ball_size[0]
            ball_height = ball_size[1]

            # 공이 벽에 닿았을 때
            if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
                ball_val["to_x"] = ball_val["to_x"] * -1 # 가로벽에 닿았을 때 공을 반대 방향으로 튕김
            
            # 공이 바닥에 닿았을 때
            if ball_pos_y >= screen_height - ball_height - 100:
                ball_val["to_y"] = ball_val["init_spd_y"]
            else: # 그 외의 모든 경우에는 속도를 증가
                ball_val["to_y"] += 0.5
            
            ball_val["pos_x"] += ball_val["to_x"] 
            ball_val["pos_y"] += ball_val["to_y"]

        # ====충돌 처리====

        # 캐릭터 rect 정보 업데이트
        character_rect = character.get_rect()
        character_rect.left = character_x_pos
        character_rect.top = character_y_pos

        for ball_idx, ball_val in enumerate(balls):
            ball_pos_x = ball_val["pos_x"]
            ball_pos_y = ball_val["pos_y"]
            ball_img_idx = ball_val["img_idx"]

            # 공 rect 정보 업데이트
            ball_rect = ball_images[ball_img_idx].get_rect()
            ball_rect.left = ball_pos_x
            ball_rect.top = ball_pos_y

            # 공과 캐릭터 충돌 처리

            
            if character_rect.colliderect(ball_rect) and level ==1:
                crash_sound.play()
                lives -= 1

                pygame.time.delay(2000)

                bullets.clear()
                balls.clear()

                balls.append({
                    "pos_x": 50,
                    "pos_y": 50,
                    "img_idx": 0,
                    "to_x": 3,
                    "to_y": -6,
                    "init_spd_y": ball_speed_y[0]
                })


            if lives == 0:
                # 게임 사운드
                bgm.stop()
                gameover_sound.play()
        
                # GAME OVER 텍스트
                    
                game_over_text = game_over_font.render("GAME OVER", True, (255, 50, 50))
                
                # 화면 중앙에 배치
                text_rect = game_over_text.get_rect(
                    center=(screen_width // 2, screen_height // 2)
                )
                screen.blit(game_over_text, text_rect)
                pygame.display.update()

                pygame.time.delay(2000)
                running = False
                break

            # 공과 무기들 충돌 처리
            for bulllet_idx, bullet_val in enumerate(bullets):
                bullet_x_pos = bullet_val[0]
                bullet_y_pos = bullet_val[1]

                bullet_rect = bullet.get_rect()
                bullet_rect.left = bullet_x_pos
                bullet_rect.top = bullet_y_pos

                # 충돌 체크
                if bullet_rect.colliderect(ball_rect):
                    bullet_to_remove = bulllet_idx 
                    ball_to_remove = ball_idx

                    # 가장 작은 크기의 공이 아니라면 쪼개기
                    if ball_img_idx < 3:
                        # 현재 공 크기 정보를 가져옴
                        ball_width = ball_rect.size[0]
                        ball_height = ball_rect.size[1]

                        # 나눠진 공 정보
                        small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                        small_ball_width = small_ball_rect.size[0]
                        small_ball_height = small_ball_rect.size[1]

                        # 왼쪽 작은 공
                        balls.append({
                            "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2), # 공의 x좌표
                            "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2), # 공의 y좌표
                            "img_idx" : ball_img_idx + 1, # 공의 이미지 인덱스
                            "to_x" : -3, # x축 이동 방향
                            "to_y": -6,  # y축 이동 방향 # y 최초 속도
                            "init_spd_y" : ball_speed_y[ball_img_idx + 1]})
                        # 오른쪽 작은 공
                        balls.append({
                            "pos_x" : ball_pos_x + ball_width / 2 - small_ball_width / 2, # 공의 x좌표
                            "pos_y" : ball_pos_y + ball_height / 2 - small_ball_height / 2, # 공의 y좌표
                            "img_idx" : ball_img_idx + 1, # 공의 이미지 인덱스
                            "to_x" : 3, # x축 이동 방향
                            "to_y": -6,  # y축 이동 방향 # y 최초 속도
                            "init_spd_y" : ball_speed_y[ball_img_idx + 1]})

                    break
            else: # 계속 게임을 진행
                continue
            break # 바깥쪽 for문 탈출

        # 충돌한 공 or 무기 없애기
        if ball_to_remove > -1:
            del balls[ball_to_remove]
            ball_to_remove = -1

        if bullet_to_remove > -1:
            del bullets[bullet_to_remove]
            bullet_to_remove = -1
        
        screen.blit(background, (0, 0))
        screen.blit(character, (character_x_pos, character_y_pos ))
        for bullet_x_pos, bullet_y_pos in bullets:
            screen.blit(bullet, (bullet_x_pos, bullet_y_pos))
       
        for idx, val in enumerate(balls):
            ball_pos_x = val["pos_x"]
            ball_pos_y = val["pos_y"]
            ball_img_idx = val["img_idx"]
            screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))
       
    
        # 폰트 정의
        game_font = pygame.font.Font(None, 40) # 폰트 객체 생성(폰트, 크기)
        score_text = game_font.render(f"LIFE : {lives}", True, (255,255,0))
        screen.blit(score_text, (10, 10))
        pygame.display.flip()

        
        if len(balls) == 0:
            
            font = pygame.font.Font(None, 100)
            clear_text = font.render("STAGE CLEAR!", True, (0, 255, 0))

            screen.blit(clear_text, (300, 300))
            pygame.display.update()

            pygame.time.delay(2000)

            bullets.clear()
            balls.clear()
            level = 2
            lives = 3


            balls.append({
                "pos_x": 50,
                "pos_y": 50,
                "img_idx": 0,
                "to_x": 3,
                "to_y": -6,
                "init_spd_y": ball_speed_y[0]
            })
            
            balls.append({
                "pos_x": 500,
                "pos_y": 50,
                "img_idx": 0,
                "to_x": 3,
                "to_y": -6,
                "init_spd_y": ball_speed_y[0]
            })

    
        # 공과 캐릭터 충돌 처리
        if character_rect.colliderect(ball_rect) and level ==2:
            crash_sound.play()
            lives -= 1

            pygame.time.delay(2000)

            bullets.clear()
            balls.clear()

            balls.append({
                "pos_x": 50,
                "pos_y": 50,
                "img_idx": 0,
                "to_x": 3,
                "to_y": -6,
                "init_spd_y": ball_speed_y[0]
            })
            
            balls.append({
            "pos_x": 500,
            "pos_y": 50,
            "img_idx": 0,
            "to_x": 3,
            "to_y": -6,
            "init_spd_y": ball_speed_y[0]
        })
            
    
main()
# 게임 종료
pygame.quit()import pygame
import os

###########################################################

current_path = os.path.dirname(__file__) # 현재 파일의 위치 반환
image_path = os.path.join(current_path, "image")
sound_path = os.path.join(current_path, "sound")

####### 이미지 업로드########

# 배경 
background = pygame.image.load(os.path.join(image_path, "pang.png"))

# 스테이지
stage = 180

# 기회
lives = 3

# 레벨
level = 1

# 화면 크기 설정
screen_width = 1100 # 가로 크기
screen_height = 720 # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 캐릭터 
character = pygame.image.load(os.path.join(image_path, "main.png"))
character_size = character.get_rect().size # 이미지 크기를 구해옴
character_width = character_size[0] # 캐릭터의 가로 크기
character_height = character_size[1] # 캐릭터의 세로 크기
character_x_pos = (screen_width / 2) - (character_width / 2) # 화면 가로 중앙에 위치
character_y_pos = screen_height - stage # 화면 하단 스테이지 높이 
character_speed = 0.4

# 무기
bullet = pygame.image.load(os.path.join(image_path, "bullet.png"))
bullet_size = bullet.get_rect().size # 이미지 크기를 구해옴
bullet_width = bullet_size[0] 

# 공
ball_images = [
        pygame.image.load(os.path.join(image_path, "ball.png")),
        pygame.image.load(os.path.join(image_path, "ball2.png")),
        pygame.image.load(os.path.join(image_path, "ball3.png")),
        pygame.image.load(os.path.join(image_path, "ball4.png"))]
                                             

# 공 크기에 따른 최초 스피드
ball_speed_y = [-18, -16, -14, -12]

balls =[]

balls.append({
    "pos_x" : 50, # 공의 x좌표
    "pos_y" : 50, # 공의 y좌표
    "img_idx" : 0,# 공의 이미지 인덱스
    "to_x" : 3, # x축 이동 방향
    "to_y": -6,  # y축 이동 방향 # y 최초 속도
    "init_spd_y" : ball_speed_y[0]})

# 이동할 좌표
character_x = 0

def main():
    global character_x_pos, character_y_pos, character_x, lives, level
    # 게임 초기화
    pygame.init() # Initialising pygame


    # 화면 타이틀 설정
    pygame.display.set_caption("Pang") # 게임 이름

    # FPS
    clock = pygame.time.Clock()

    ###########################################################

    # 사용자 게임 초기화(배경 화면, 게임 이미지, 좌표, 폰트 등)


    # 배경 음악
    bgm = pygame.mixer.Sound(os.path.join(sound_path, "main.mp3"))
     # 효과음
    shoot_sound = pygame.mixer.Sound(os.path.join(sound_path, "shoot.wav"))
    gameover_sound = pygame.mixer.Sound(os.path.join(sound_path, "gameover.wav"))
    crash_sound = pygame.mixer.Sound(os.path.join(sound_path, "crash.wav"))
    bgm.set_volume(0.4)  

    # 배경음악 시작 
    bgm.play(-1)

    # 폰트 정의(게임 오버)
    game_over_font = pygame.font.Font(None, 180) 

    # 총알 여러발 생성
    bullets = []
    # 총알 스피드
    bullet_speed = 0.5

    # 이벤트 루프
    running = True 
    while running:
        dt = clock.tick(60) # 게임 화면당 초당 프레임수 설정
      
        # 이벤트 처리 (키보드, 마우스 등)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False 

            # 키 입력 → 이동 방향 계산              
            if event.type == pygame.KEYDOWN:  # 키가 눌러졌는지 확인
                if event.key == pygame.K_SPACE: 
                        bullet_x_pos = character_x_pos + (character_width / 2) - (bullet_width / 2)
                        bullet_y_pos = character_y_pos - character_height
                        bullets.append([bullet_x_pos, bullet_y_pos]) 
                        shoot_sound.play()  

                if event.key == pygame.K_LEFT: # 캐릭터를 왼쪽으로
                    character_x -= character_speed
                elif event.key == pygame.K_RIGHT: # 캐릭터를 오른쪽으로
                    character_x += character_speed      
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    character_x = 0
            
        character_x_pos += character_x * dt

        if character_x_pos < 0:
            character_x_pos = 0
        elif character_x_pos > screen_width - character_width:
            character_x_pos = screen_width - character_width        

      
        # 총알 위치 조정
        bullets = [[b[0], b[1] - bullet_speed * dt] for b in bullets] # 총알 위치를 위로
        # 천장에 닿은 총알 제거하기
        bullets = [[b[0], b[1]] for b in bullets if b[1] > 0]

        # 사라질 무기, 공 정보 저장 변수
        bullet_to_remove = -1
        ball_to_remove = -1

        # 공 위치 정의
        for ball_idx, ball_val in enumerate(balls):
            ball_pos_x = ball_val["pos_x"]
            ball_pos_y = ball_val["pos_y"]
            ball_img_idx = ball_val["img_idx"]

            ball_size = ball_images[ball_img_idx].get_rect().size
            ball_width = ball_size[0]
            ball_height = ball_size[1]

            # 공이 벽에 닿았을 때
            if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
                ball_val["to_x"] = ball_val["to_x"] * -1 # 가로벽에 닿았을 때 공을 반대 방향으로 튕김
            
            # 공이 바닥에 닿았을 때
            if ball_pos_y >= screen_height - ball_height - 100:
                ball_val["to_y"] = ball_val["init_spd_y"]
            else: # 그 외의 모든 경우에는 속도를 증가
                ball_val["to_y"] += 0.5
            
            ball_val["pos_x"] += ball_val["to_x"] 
            ball_val["pos_y"] += ball_val["to_y"]

        # ====충돌 처리====

        # 캐릭터 rect 정보 업데이트
        character_rect = character.get_rect()
        character_rect.left = character_x_pos
        character_rect.top = character_y_pos

        for ball_idx, ball_val in enumerate(balls):
            ball_pos_x = ball_val["pos_x"]
            ball_pos_y = ball_val["pos_y"]
            ball_img_idx = ball_val["img_idx"]

            # 공 rect 정보 업데이트
            ball_rect = ball_images[ball_img_idx].get_rect()
            ball_rect.left = ball_pos_x
            ball_rect.top = ball_pos_y

            # 공과 캐릭터 충돌 처리

            
            if character_rect.colliderect(ball_rect) and level ==1:
                crash_sound.play()
                lives -= 1

                pygame.time.delay(2000)

                bullets.clear()
                balls.clear()

                balls.append({
                    "pos_x": 50,
                    "pos_y": 50,
                    "img_idx": 0,
                    "to_x": 3,
                    "to_y": -6,
                    "init_spd_y": ball_speed_y[0]
                })


            if lives == 0:
                # 게임 사운드
                bgm.stop()
                gameover_sound.play()
        
                # GAME OVER 텍스트
                    
                game_over_text = game_over_font.render("GAME OVER", True, (255, 50, 50))
                
                # 화면 중앙에 배치
                text_rect = game_over_text.get_rect(
                    center=(screen_width // 2, screen_height // 2)
                )
                screen.blit(game_over_text, text_rect)
                pygame.display.update()

                pygame.time.delay(2000)
                running = False
                break

            # 공과 무기들 충돌 처리
            for bulllet_idx, bullet_val in enumerate(bullets):
                bullet_x_pos = bullet_val[0]
                bullet_y_pos = bullet_val[1]

                bullet_rect = bullet.get_rect()
                bullet_rect.left = bullet_x_pos
                bullet_rect.top = bullet_y_pos

                # 충돌 체크
                if bullet_rect.colliderect(ball_rect):
                    bullet_to_remove = bulllet_idx 
                    ball_to_remove = ball_idx

                    # 가장 작은 크기의 공이 아니라면 쪼개기
                    if ball_img_idx < 3:
                        # 현재 공 크기 정보를 가져옴
                        ball_width = ball_rect.size[0]
                        ball_height = ball_rect.size[1]

                        # 나눠진 공 정보
                        small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                        small_ball_width = small_ball_rect.size[0]
                        small_ball_height = small_ball_rect.size[1]

                        # 왼쪽 작은 공
                        balls.append({
                            "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2), # 공의 x좌표
                            "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2), # 공의 y좌표
                            "img_idx" : ball_img_idx + 1, # 공의 이미지 인덱스
                            "to_x" : -3, # x축 이동 방향
                            "to_y": -6,  # y축 이동 방향 # y 최초 속도
                            "init_spd_y" : ball_speed_y[ball_img_idx + 1]})
                        # 오른쪽 작은 공
                        balls.append({
                            "pos_x" : ball_pos_x + ball_width / 2 - small_ball_width / 2, # 공의 x좌표
                            "pos_y" : ball_pos_y + ball_height / 2 - small_ball_height / 2, # 공의 y좌표
                            "img_idx" : ball_img_idx + 1, # 공의 이미지 인덱스
                            "to_x" : 3, # x축 이동 방향
                            "to_y": -6,  # y축 이동 방향 # y 최초 속도
                            "init_spd_y" : ball_speed_y[ball_img_idx + 1]})

                    break
            else: # 계속 게임을 진행
                continue
            break # 바깥쪽 for문 탈출

        # 충돌한 공 or 무기 없애기
        if ball_to_remove > -1:
            del balls[ball_to_remove]
            ball_to_remove = -1

        if bullet_to_remove > -1:
            del bullets[bullet_to_remove]
            bullet_to_remove = -1
        
        screen.blit(background, (0, 0))
        screen.blit(character, (character_x_pos, character_y_pos ))
        for bullet_x_pos, bullet_y_pos in bullets:
            screen.blit(bullet, (bullet_x_pos, bullet_y_pos))
       
        for idx, val in enumerate(balls):
            ball_pos_x = val["pos_x"]
            ball_pos_y = val["pos_y"]
            ball_img_idx = val["img_idx"]
            screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))
       
    
        # 폰트 정의
        game_font = pygame.font.Font(None, 40) # 폰트 객체 생성(폰트, 크기)
        score_text = game_font.render(f"LIFE : {lives}", True, (255,255,0))
        screen.blit(score_text, (10, 10))
        pygame.display.flip()

        
        if len(balls) == 0:
            
            font = pygame.font.Font(None, 100)
            clear_text = font.render("STAGE CLEAR!", True, (0, 255, 0))

            screen.blit(clear_text, (300, 300))
            pygame.display.update()

            pygame.time.delay(2000)

            bullets.clear()
            balls.clear()
            level = 2
            lives = 3


            balls.append({
                "pos_x": 50,
                "pos_y": 50,
                "img_idx": 0,
                "to_x": 3,
                "to_y": -6,
                "init_spd_y": ball_speed_y[0]
            })
            
            balls.append({
                "pos_x": 500,
                "pos_y": 50,
                "img_idx": 0,
                "to_x": 3,
                "to_y": -6,
                "init_spd_y": ball_speed_y[0]
            })

    
        # 공과 캐릭터 충돌 처리
        if character_rect.colliderect(ball_rect) and level ==2:
            crash_sound.play()
            lives -= 1

            pygame.time.delay(2000)

            bullets.clear()
            balls.clear()

            balls.append({
                "pos_x": 50,
                "pos_y": 50,
                "img_idx": 0,
                "to_x": 3,
                "to_y": -6,
                "init_spd_y": ball_speed_y[0]
            })
            
            balls.append({
            "pos_x": 500,
            "pos_y": 50,
            "img_idx": 0,
            "to_x": 3,
            "to_y": -6,
            "init_spd_y": ball_speed_y[0]
        })
            
    
main()
# 게임 종료
pygame.quit()
