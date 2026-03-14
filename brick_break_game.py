import pygame

# 벽돌을 그리는 함수
def draw_brick(bricks, color):
    for i in  bricks:
        pygame.draw.rect(screen, color, i)

# 게임 초기화
pygame.init()
# 화면 크기
size = (600, 700)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Brick Breaker Game")

clock = pygame.time.Clock()
FPS = 120

# 패들
paddle = pygame.Rect(100, 650, 200, 30)
# 공
ball = pygame.Rect(50, 350, 20, 20)
# 점수
score = 0
# 공의 이동방향
move = [3, 3]

game = True

# 색상 정의
YELLOW = (255, 255, 0)
BLUE = (50, 150, 255)
GREEN = (28, 252, 106)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (252, 3, 152)
ORANGE = (252, 170, 28)
RED = (255, 0, 0)

# 벽돌 생성(6 x 4 = 24개)
b1 = [pygame.Rect(1 + i * 100, 60, 97, 38) for i in range(6)]
b2 = [pygame.Rect(1 + i * 100, 100, 97, 38) for i in range(6)]
b3 = [pygame.Rect(1 + i * 100, 140, 97, 38) for i in range(6)]
b4 = [pygame.Rect(1 + i * 100, 180, 97, 38) for i in range(6)]


# 게임 진행 구간
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
    # 게임 화면은 검정색으로 설정
    screen.fill(BLACK)
    pygame.draw.rect(screen, PINK, paddle)
    font = pygame.font.Font(None, 34)
    text = font.render("CURRENT SCORE: " + str(score), 1, WHITE)
    screen.blit(text, (180, 10))

    # 키보드의 ⬅️➡️ 키를 눌러 패들을 이동함
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            if paddle.x < 480:
                paddle.x = paddle.x + 7 # 패들의 이동 속도(오른쪽)
                
        if event.key == pygame.K_LEFT:
            if paddle.x > 0:
                paddle.x = paddle.x - 7 # 패들의 이동 속도(왼쪽)

    # 벽돌 그리기
    draw_brick(b1, RED)
    draw_brick(b2, YELLOW)
    draw_brick(b3, GREEN)
    draw_brick(b4, BLUE)

    ball.x = ball.x + move[0]
    ball.y = ball.y + move[1]

    # 볼이 천장이나 벽에 닿으면 튕겨내기
    if ball.x > 580 or ball.x < 0:
        move[0] = -move[0]
    if ball.y <= 3:
        move[1] = -move[1]
    # 공이 패들에 닿으면 튕겨내기
    if paddle.collidepoint(ball.x, ball.y):
        move[1] = -move[1]

    # 볼이 바닥에 닿았을 때 종료 처리 및 점수 표시
    if ball.y >= 690:
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over!", 1, RED)
        screen.blit(text, (150, 300))
        font = pygame.font.Font(None, 50)
        text = font.render("YOUR FINAL SCORE: " + str(score), 1, GREEN)
        screen.blit(text, (100, 350))
        pygame.display.flip()
        # 3초 대기
        pygame.time.wait(3000)
        break
    
    # 공 그리기
    pygame.draw.circle(screen, WHITE, ball.center, 10)

    brick_layers = [b1, b2, b3, b4]
    # 공이 벽돌에 닿으면 제거
    for bricks in brick_layers:
        for i in bricks:
            if i.collidepoint(ball.x, ball.y):
                bricks.remove(i)
                move[0] = -move[0]
                move[1] = -move[1]
                score = score + 1
        

    # 벽돌을 모두 제거하면 승리(24개)
    if score == 24:
        font = pygame.font.Font(None, 74)
        text = font.render("YOU WON THE GAME!", 1, GREEN)
        screen.blit(text, (150, 350))
        pygame.display.flip()
        # 3초 대기
        pygame.time.wait(3000)
        break

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()




