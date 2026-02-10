# 간단한 네트워크 스캐너, 주의사항, 대규모 네트워크 스캔은 불법입니다. 자신의 컴퓨터를 대상으로 연습하세요.
import socket
import threading
from time import time

# 포트 스캔 함수
def scan_port(target, port):
    """
    target IP의 특정 port가 열려 있는지 확인한다.
    TCP connect 방식으로 포트 상태를 판단한다.
    """
    try:
        # IPv4(AF_INET) + TCP(SOCK_STREAM) 소켓 생성
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        s.settimeout(1) # 응답 없으면 1초 기다림

        result = s.connect_ex((target, port)) # 대상 ip의 특정 포트 연결 시도, 성공하면 0반환
        if result == 0:
            print(f"[OPEN] Port {port}")

        s.close()
    # 예외 처리
    except KeyboardInterrupt:
        print ("You pressed Ctrl+C")
        return
    except socket.gaierror:
        print ('Hostname could not be resolved.')
        return
    except socket.error:
        print ("Couldn't connect to server")
        return 
    

def thread_scan(target, start_port, end_port, thread_count=100):
    """ 여러 개의 포트를 동시 스캔하는 함수, 
    스레드 개수를 제한해서 과부하 방지"""
    threads = [] 
   
    for port in range(start_port, end_port + 1):
        
        t = threading.Thread(target=scan_port, args=(target, port))
        threads.append(t)
        t.start()

        # 동시에 실행 중인 스레드가 thread_count에 도달하면
        # 전부 종료될 때까지 대기 (join)
        if len(threads) >= thread_count:
            for t in threads:
                t.join()
            threads = [] # 스레드 리스트 초기화

    # 마지막 남은 스레드 처리
    for t in threads:
        t.join()

    # 모든 스레드 종료 대기
   
def main():

    target = "45.33.32.156" # nmap의 테스트용 서버 ip
    start_port = 1
    end_port = 1024

    print(f"\n{target} 스캔 시작...\n")
    t1 = time() # 스캔 시작 시간

    thread_scan(target, start_port, end_port)

    t2 = time() # 스캔 종료 시간
    total = t2 - t1 # 스캔 소요 시간 계산
    print("\n스캔 완료")
    print(f"소요시간 : {round(total, 2)}")

if __name__ == "__main__":
    main()
