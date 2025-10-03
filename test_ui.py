"""Simple test to check if CustomTkinter is working"""

import customtkinter as ctk

app = ctk.CTk()
app.title("Test")
app.geometry("400x300")

label = ctk.CTkLabel(app, text="Can you see this text?", font=("Arial", 20))
label.pack(pady=50)

button = ctk.CTkButton(app, text="Test Button", width=200, height=50)
button.pack(pady=20)

app.mainloop()
