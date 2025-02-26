import tkinter as tk
import socket
import threading

# SERVER PORT
SERVER_IP = '211.204.59.171' 
SERVER_PORT = 5555

# 클라이언트 소켓 생성 및 서버 연결
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, SERVER_PORT))

# 메시지 보내기
def send_message():
    message = entry.get()  # Entry 위젯에서 텍스트 가져오기
    if message:
        client.send(message.encode())  # 서버로 메시지 전송
        chat_log.config(state=tk.NORMAL)
        chat_log.insert(tk.END, f"사용자 : {message}\n")  # 채팅 로그에 추가
        chat_log.config(state=tk.DISABLED)
        entry.delete(0, tk.END)  # 입력 필드 초기화

# 메시지 받기 (별도의 스레드에서 실행)
def receive_message():
    while True:
        try:
            message = client.recv(1024).decode()  # 서버에서 메시지 수신
            if message:
                chat_log.config(state=tk.NORMAL)
                chat_log.insert(tk.END, message + "\n")
                chat_log.config(state=tk.DISABLED)
                chat_log.yview(tk.END)
        except:
            print("[연결 종료] 서버와의 연결이 끊어졌습니다.")
            break

# GUI 설정
window = tk.Tk()
window.title("네트워크 채팅")

# 채팅 로그 창
chat_log = tk.Text(window, state=tk.DISABLED, width=50, height=20, wrap="word")
chat_log.pack(padx=10, pady=10)

# 사용자 입력 필드
entry = tk.Entry(window, width=40)
entry.pack(side=tk.LEFT, padx=10, pady=10)

# 전송 버튼
send_button = tk.Button(window, text='보내기', command=send_message)
send_button.pack(side=tk.RIGHT, padx=10, pady=10)

# 엔터 키로 메시지 전송 가능
window.bind("<Return>", lambda event: send_message())

# 서버 메시지 수신을 위한 스레드 실행
receive_thread = threading.Thread(target=receive_message, daemon=True)
receive_thread.start()

# Tkinter 실행 루프
window.mainloop()
