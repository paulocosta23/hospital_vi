import sys
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk 
from config import db
from views.login_view import LoginView
from views.dashboard_view import DashboardView
from views.theme import DEFAULT_MODE, set_theme_mode


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        set_theme_mode(DEFAULT_MODE)

        self.geometry("1000x600")
        self.title("Clínica Médica")
        self.resizable (True , True)
        self.minsize(1100, 650)
        
        self.after(0, lambda: self.state('zoomed'))
        self.current_view = None
        self.dashboard = None
        self.usuario_logado = None

        self.show_login()



    # ---------- controle de telas ----------
    def clear_view(self):
        if self.current_view is not None:
            self.current_view.destroy()
            self.current_view = None

    # ---------- login ----------
    def show_login(self):
        self.clear_view()
        self.dashboard = None
        self.usuario_logado = None

        self.current_view = LoginView(
            self,
            on_login=self.fake_login
        )

    # ---------- login simulado (temporário) ----------
    def fake_login(self):
        # 🔹 Ajusta depois com banco
        self.usuario_logado = {
            "nome": "Administrador",
            "tipo": "admin"
        }

        self.show_dashboard()

    # ---------- dashboard ----------
    def show_dashboard(self):
        self.clear_view()

        self.dashboard = DashboardView(
            self,
            usuario=self.usuario_logado
        )

        self.current_view = self.dashboard


if __name__ == "__main__":
    conexao = db.conectar()
    if conexao is None:
        sys.exit(1)
    conexao.close()

    app = App()
    app.mainloop()