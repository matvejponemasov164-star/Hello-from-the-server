import socket
import tkinter as tk
from tkinter import messagebox

def send_data_to_server():
    name = entry_name.get()
    age = entry_age.get()

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12345))
        
        client_socket.send(f"{name},{age}".encode('utf-8'))
        
        response = client_socket.recv(1024).decode('utf-8')
        
        if response.startswith("Ошибка"):
            messagebox.showerror("Ошибка", response)
        else:
            messagebox.showinfo("Результат", response)
    
    except ConnectionRefusedError:
        messagebox.showerror("Ошибка", "Не удалось подключиться к серверу. Убедитесь, что сервер запущен.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла непредвиденная ошибка: {e}")
    finally:
        try:
            client_socket.close()
        except:
            pass

root = tk.Tk()
root.title("Приветственное приложение")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Имя:").grid(row=0, column=0, sticky="w")
entry_name = tk.Entry(frame, width=30)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Возраст:").grid(row=1, column=0, sticky="w")
entry_age = tk.Entry(frame, width=30)
entry_age.grid(row=1, column=1, padx=5, pady=5)

button_send = tk.Button(frame, text="Поприветствовать", command=send_data_to_server)
button_send.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
