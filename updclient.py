import socket
import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

TEMPLATE_FILE = 'templates.json'

def load_templates():
    if os.path.exists(TEMPLATE_FILE):
        with open(TEMPLATE_FILE, 'r') as file:
            return json.load(file)
    return []

def save_templates(templates):
    with open(TEMPLATE_FILE, 'w') as file:
        json.dump(templates, file, indent=4)

def udp_client(message, host='localhost', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.sendto(message.encode(), (host, port))
        print(f"Sent message to {host}:{port}: {message}")

def send_message(event=None):
    user_input = message_entry.get().strip()
    
    selected_index = template_list.curselection()
    
    if selected_index:
        template = templates[selected_index[0]]
        
        if "%name%" in template:
            final_message = template.replace("%name%", user_input)
        else:
            final_message = f"{template} {user_input}" if user_input else template
    else:
        final_message = user_input
    
    
    if final_message.strip():
        udp_client(message=final_message)
        messagebox.showinfo("Info", "Message sent successfully")
        message_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Message cannot be empty")

def add_template():
    template_name = simpledialog.askstring("Input", "Enter template content (use %name% as a placeholder):")
    if template_name:
        templates.append(template_name)
        update_template_list()
        save_templates(templates)

def edit_template():
    selected_index = template_list.curselection()
    if selected_index:
        new_value = simpledialog.askstring("Input", "Edit template content:", initialvalue=templates[selected_index[0]])
        if new_value:
            templates[selected_index[0]] = new_value
            update_template_list()
            save_templates(templates)

def delete_template():
    selected_index = template_list.curselection()
    if selected_index:
        templates.pop(selected_index[0])
        update_template_list()
        save_templates(templates)

def update_template_list():
    template_list.delete(0, tk.END)
    for template in templates:
        template_list.insert(tk.END, template)

def load_template(event):
    pass

root = tk.Tk()
root.title("UDP Client")

templates = load_templates()

template_frame = tk.Frame(root)
template_frame.pack(padx=10, pady=5, fill=tk.X)

template_list = tk.Listbox(template_frame, height=5)
template_list.pack(side=tk.LEFT, fill=tk.X, expand=True)

template_list.bind('<<ListboxSelect>>', load_template)

btn_frame = tk.Frame(template_frame)
btn_frame.pack(side=tk.RIGHT, padx=5)

add_button = tk.Button(btn_frame, text="Add", command=add_template)
add_button.pack(side=tk.TOP, fill=tk.X)

edit_button = tk.Button(btn_frame, text="Edit", command=edit_template)
edit_button.pack(side=tk.TOP, fill=tk.X)

delete_button = tk.Button(btn_frame, text="Delete", command=delete_template)
delete_button.pack(side=tk.TOP, fill=tk.X)

message_label = tk.Label(root, text="Message:")
message_label.pack(padx=10, pady=5)

message_entry = tk.Entry(root, width=50)
message_entry.pack(padx=10, pady=5)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(padx=10, pady=20)

root.bind('<Return>', send_message)

update_template_list()

root.mainloop()
