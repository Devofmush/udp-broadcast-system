import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
import pystray
from PIL import Image, ImageDraw
from PyQt5 import QtWidgets, QtCore, QtGui, QtMultimedia
import sys
import os
from datetime import datetime
import getpass

def create_image():
    width = 16
    height = 16
    color1 = "black"
    color2 = "white"

    image = Image.new("RGB", (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle([(width // 2, 0), (width, height // 2)], fill=color2)
    dc.rectangle([(0, height // 2), (width // 2, height)], fill=color2)
    return image

def log_message(message):
    user = getpass.getuser()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {user}: {message}\n"

    with open("message_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)

def udp_server(host='localhost', port=12345):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
            server_socket.bind((host, port))
            print(f"Server listening on {host}:{port}")

            while True:
                message, address = server_socket.recvfrom(1024)
                decoded_message = message.decode()
                print(f"Received message from {address}: {decoded_message}")
                log_message(decoded_message)
                root.after(0, show_popup, decoded_message)
    except Exception as e:
        print(f"Error in UDP server: {e}")

def start_udp_server():
    server_thread = threading.Thread(target=udp_server, args=('localhost', 12345))
    server_thread.daemon = True
    server_thread.start()

def show_popup(message):
    def run_qt_app():
        app = QtWidgets.QApplication(sys.argv)

        window = QtWidgets.QMainWindow()
        window.showFullScreen()

        #load font
        font_path = os.path.abspath('font.ttf')
        font_id = QtGui.QFontDatabase.addApplicationFont(font_path)
        font_family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QtGui.QFont(font_family, 48)  #font size

        central_widget = QtWidgets.QWidget()
        window.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)

        label = QtWidgets.QLabel(message)
        label.setFont(font)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setWordWrap(True)
        layout.addWidget(label)

        #notification sound
        sound_path = os.path.abspath('notification.mp3')
        url = QtCore.QUrl.fromLocalFile(sound_path)
        content = QtMultimedia.QMediaContent(url)
        player = QtMultimedia.QMediaPlayer()
        player.setMedia(content)
        player.setVolume(100)
        player.play()

        #close the popup after 5 seconds
        QtCore.QTimer.singleShot(5000, window.close)
        QtCore.QTimer.singleShot(5000, app.quit)

        app.exec_()

    qt_thread = threading.Thread(target=run_qt_app)
    qt_thread.start()

def show_window():
    root.deiconify()

def hide_window(icon, item):
    root.withdraw()

def quit_app(icon, item):
    icon.stop()
    root.quit()

root = tk.Tk()
root.title("UDP Server")
root.geometry("400x300")

output_label = tk.Label(root, text="Received Messages:")
output_label.pack(padx=10, pady=5)

output_text = scrolledtext.ScrolledText(root, width=50, height=20, wrap=tk.WORD)
output_text.pack(padx=10, pady=5)

root.withdraw()

start_udp_server()

icon_image = create_image()
menu = pystray.Menu(
    pystray.MenuItem('Show', show_window),
    pystray.MenuItem('Quit', quit_app)
)
icon = pystray.Icon("UDP Server", icon_image, "UDP Server", menu)
icon.run_detached()

root.mainloop()
