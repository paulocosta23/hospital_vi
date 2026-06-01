import customtkinter as ctk 
from views.login_view import LoginView
from views.dashboard_view import DashboardView


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("light")

        self.geometry("1000x600")
        self.title("Clínica Médica")
        self.resizable (True , True)
        self.minsize(1530, 850)
        
        self.after(0, lambda: self.state('zoomed')) #minimizar após a janela esta pronta
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
    app = App()
    app.mainloop()