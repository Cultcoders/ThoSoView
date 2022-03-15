import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

root = tk.Tk()

root.title("Titel da")
root.geometry("400x300")
#root.minsize(width=200, height=150)
#root.maxsize(width=400, height=300)

image = Image.open("1_keyboard.jpg").resize((300, 100))
photo = ImageTk.PhotoImage(image)

label1 = ttk.Label(root, image=photo, compound="bottom")
label1.pack(padx=10, pady=10)

# label1["image"] = photo1
label1["text"] = "Hello World!"

root.mainloop()