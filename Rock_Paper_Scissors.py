import random
import time


choices = ["가위", "바위", "보"]

print("="*30)
print("가위 바위 보 게임을 시작합니다")
print()
print("가위(0), 바위(1), 보(2)")
print("게임을 중단하고 싶으면 'q'를 입력하세요.")
print("="*30)

while True:

    try:
        user = input("가위(0), 바위(1), 보(2) 중 선택한 숫자를 입력 : ").lower()
        if user == 'q':
            print("게임 종료") 
            break
        else:
            user = int(user)

        if user not in [0, 1, 2]:
            raise ValueError # 범위 밖의 정수를 입력하면 에러를 발생시킴

    except ValueError:
        print("정수 0, 1, 2, q 중 하나만 입력하세요.")
        continue
    

    else:
        computer = random.randint(0, 2)

        time.sleep(1)
        print(f"당신의 선택 {choices[user]}")
        time.sleep(1)
        print(f"컴퓨터의 선택 {choices[computer]}")
        time.sleep(1)
        if user == computer:
            print("비겼습니다 🤔 한판 더?")
        elif(user == 0 and computer == 2) or \
            (user == 1 and computer == 0) or\
            (user == 2 and computer == 1):
            print("당신이 이겼습니다 😓")
        else:
            print("컴퓨터의 승리 😂 약 오르지?")
        
        print("="*30)
    
