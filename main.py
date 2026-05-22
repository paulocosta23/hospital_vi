import tkinter as tk
from views.login_view import LoginView

def iniciar():
    root = tk.Tk()
    root.title("Sistema Hospitalar")
    root.geometry("900x600")

    LoginView(root)

    root.mainloop()

if __name__ == "__main__":
    iniciar()   