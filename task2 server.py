import socket
import threading

def validate_data(name, age):
    errors = []
    if not name or not name.strip():
        errors.append("Имя не может быть пустым.")
    try:
        age_int = int(age)
        if age_int <= 0:
            errors.append("Возраст должен быть положительным числом.")
    except ValueError:
        errors.append("Возраст должен быть целым числом.")
    
    return errors

def handle_client(client_socket):
    try:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            return
        
        name, age = data.split(',')
        print(f"Получены данные: Имя={name}, Возраст={age}")

        errors = validate_data(name, age)
        
        if errors:
            response = "Ошибка: " + "; ".join(errors)
        else:
            response = f"Привет, {name.strip()}! Тебе {age} лет."
      
        client_socket.send(response.encode('utf-8'))
    
    except Exception as e:
        print(f"Ошибка при обработке запроса: {e}")
        client_socket.send("Ошибка сервера при обработке запроса.".encode('utf-8'))
    finally:
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 12345))
    server.listen(5)
    print("Сервер запущен и ожидает подключений...")

    while True:
        client_socket, addr = server.accept()
        print(f"Подключен клиент с адресом: {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
