import socket
import threading

# 서버 설정(모든 네트워크 인터페이스 + 포트는 5555)
HOST = '0.0.0.0'
PORT = 5555

# 클라이언트 리스트
clients = []

# 서버 실행 여부 변수
server_running = True 

# 특정 클라이언트에게 받아서 모든 클라이언트에게 전송
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:  # sender_socket(메시지를 보낸 클라이언트) 제외
            try:
                client.send(message)
            except:
                clients.remove(client)  # 연결이 끊어진 클라이언트 제거

# 클라이언트 처리 (개별 실행)            
def handle_client(client_socket, addr):
    print(f"[+] {addr} 연결됨")
    clients.append(client_socket)  # 클라이언트 추가

    while True:
        try:
            print(f"[{addr}] 메시지 대기 중...")  # 메시지를 기다리는 상태 표시
            message = client_socket.recv(1024)  # 메시지 수신
            print(f"[{addr}] 받은 메시지 원본: {message}")  # 메시지 원본 출력

            if not message:
                print(f"[{addr}] 빈 메시지 수신. 연결 종료 처리")
                break

            decoded_message = message.decode()
            print(f"[{addr}] 디코딩된 메시지: {decoded_message}")
            broadcast(message, client_socket)  # 다른 클라이언트에게 전달
        except:
            break  # 오류 발생 시 루프 종료

    clients.remove(client_socket)
    client_socket.close()
    print(f"[-] {addr} 연결 해제됨")

# 서버 실행
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print(f"[*] 서버가 {PORT}에서 실행 중...")

# 종료 함수
def shutdown_server():
    global server_running
    input("서버를 종료하려면 Enter 키를 누르세요...\n")
    server_running = False
    server.close()
    print("[*] 서버가 종료되었습니다.")

shutdown_thread = threading.Thread(target=shutdown_server)
shutdown_thread.start()

while server_running:
    try:
        client_socket, addr = server.accept()
        print(f"[+] {addr} 새 클라이언트 연결됨")
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()
    except OSError:
        break  # 서버 소켓이 닫혔을 때 예외 발생 처리
