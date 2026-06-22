import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from .theme import get_color
from controllers.paciente_controller import salvar as salvar_paciente, listar as listar_pacientes, editar as editar_paciente, deletar as deletar_paciente, lista_planos
from datetime import datetime


class PatientsView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.configure(fg_color=get_color("bg"))

        self.pacientes = []
        self.filtro_nome = ""

        self.render()

    def formatar_cpf(self, texto):
        nums = "".join(filter(str.isdigit, texto))[:11]
        if len(nums) <= 3:
            return nums
        elif len(nums) <= 6:
            return f"{nums[:3]}.{nums[3:]}"
        elif len(nums) <= 9:
            return f"{nums[:3]}.{nums[3:6]}.{nums[6:]}"
        else:
            return f"{nums[:3]}.{nums[3:6]}.{nums[6:9]}-{nums[9:]}"

    def render(self):
        for w in self.winfo_children():
            w.destroy()

        header = ctk.CTkFrame(self, fg_color=get_color("panel"), corner_radius=20)
        header.pack(fill="x", padx=25, pady=(20, 10))

        ctk.CTkLabel(
            header,
            text="👨‍⚕️ Pacientes",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=get_color("text"),
        ).pack(side="left", padx=20, pady=15)

        ctk.CTkButton(
            header,
            text="+ Novo paciente",
            fg_color=get_color("accent"),
            hover_color=get_color("accent_hover"),
            corner_radius=12,
            height=40,
            command=self.popup,
        ).pack(side="right", padx=20)

        busca_frame = ctk.CTkFrame(self, fg_color=get_color("panel"), corner_radius=20)
        busca_frame.pack(fill="x", padx=25, pady=(0, 15))

        self.input_busca = ctk.CTkEntry(
            busca_frame,
            placeholder_text="Buscar paciente pelo nome",
            height=42,
            corner_radius=12,
            fg_color=get_color("surface"),
            border_color=get_color("border"),
            border_width=2,
            text_color=get_color("text"),
        )
        self.input_busca.pack(side="left", fill="x", expand=True, padx=15, pady=15)

        ctk.CTkButton(
            busca_frame,
            text="Buscar",
            fg_color=get_color("accent"),
            hover_color=get_color("accent_hover"),
            corner_radius=12,
            command=self.buscar,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            busca_frame,
            text="Limpar",
            fg_color=get_color("text_secondary"),
            hover_color=get_color("border"),
            corner_radius=12,
            command=self.limpar_busca,
        ).pack(side="left", padx=(5, 15))

        self.lista = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.lista.pack(fill="both", expand=True, padx=25, pady=(0, 15))

        self.render_lista()

    def buscar(self):
        self.filtro_nome = self.input_busca.get().lower()
        self.render_lista()

    def limpar_busca(self):
        self.filtro_nome = ""
        self.input_busca.delete(0, "end")
        self.render_lista()

    def mascarar_cpf(self, cpf):
        cpf = ''.join(filter(str.isdigit, cpf))  # remove formatação anterior
        return f"{cpf[:3]}.***.***.{cpf[-2:]}"

    def render_lista(self):
        for w in self.lista.winfo_children():
            w.destroy()

        pacientes = listar_pacientes()
        print(pacientes)
        if self.filtro_nome:
            pacientes = [p for p in pacientes if self.filtro_nome in p["nome"].lower()]
        
        if not pacientes:
            ctk.CTkLabel(
                self.lista,
                text="Nenhum paciente cadastrado",
                text_color=get_color("text"),
                font=ctk.CTkFont(size=16),
            ).pack(pady=40)
            return

        for p in pacientes:
            self.card(p)

    def card(self, p):
        card = ctk.CTkFrame(
            self.lista,
            fg_color=get_color("surface"),
            corner_radius=20,
            border_width=2,
            border_color=get_color("border"),
        )
        card.pack(fill="x", pady=8)

        container = ctk.CTkFrame(card, fg_color="transparent")
        container.pack(fill="x", padx=15, pady=15)

        info = ctk.CTkFrame(container, fg_color="transparent")
        info.pack(side="left", expand=True, fill="x")
       
        #self.id_paciente = p.get("id_paciente")
       
        ctk.CTkLabel(
            info,
            text=p["nome"],
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=get_color("text"),
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=f"CPF: {self.mascarar_cpf(p['cpf'])} | Tel: {p['telefone']}",
            text_color=get_color("text_secondary"),
        ).pack(anchor="w")

        self.tipo = p.get("tipo")
        self.plano = p.get("plano")
        if  self.plano:
            self.tipo = "Convênio"
            self.plano = self.plano
        elif self.plano is None:
            self.tipo = "Particular"
            self.plano = "-"
        ctk.CTkLabel(
           info,
            text=f"Tipo: {self.tipo} | Plano: {self.plano}",
            text_color=get_color("text_secondary"),
        ).pack(anchor="w")

        self.carteirinha = p.get("carteirinha")
        if not self.carteirinha:
            self.carteirinha = "-"

        ctk.CTkLabel(
            info,
            text=f"Cart.: {self.carteirinha} | Nasc: {p.get('nascimento','-')}",
            text_color=get_color("text_secondary"),
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=f"Endereço: {p.get('endereco','-')}",
            text_color=get_color("text_secondary"),
            wraplength=450,
        ).pack(anchor="w")

        ctk.CTkButton(
            container,
            text="Excluir",
            width=90,
            height=38,
            corner_radius=12,
            fg_color="#e53935",
            hover_color="#b71c1c",
            command=lambda p=p: self.excluir(p),
        ).pack(side="right", padx=(0, 8))

        ctk.CTkButton(
            container,
            text="Editar",
            width=90,
            height=38,
            corner_radius=12,
            fg_color=get_color("accent"),
            hover_color=get_color("accent_hover"),
            command=lambda p=p: self.popup(p),
        ).pack(side="right")

    def popup(self, paciente=None):
        popup = ctk.CTkToplevel(self)
        popup.geometry("450x650")
        popup.grab_set()

        frame = ctk.CTkFrame(
            popup,
            fg_color=get_color("surface"),
            corner_radius=20,
        )
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            frame,
            text="👨‍⚕️ Paciente",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=get_color("text"),
        ).pack(pady=15)

        self.nome = ctk.CTkEntry(
            frame,
            placeholder_text="Nome",
            height=40,
            corner_radius=12,
            border_width=2,
            border_color=get_color("border"),
        )
        self.nome.pack(fill="x", pady=6)

        self.cpf = ctk.CTkEntry(
            frame,
            placeholder_text="CPF",
            height=40,
            corner_radius=12,
            border_width=2,
            border_color=get_color("border"),
        )
        self.cpf.pack(fill="x", pady=6)

        def mascara(event):
            valor = self.formatar_cpf(self.cpf.get())
            self.cpf.delete(0, "end")
            self.cpf.insert(0, valor)

        self.cpf.bind("<KeyRelease>", mascara)

        self.telefone = ctk.CTkEntry(
            frame,
            placeholder_text="Telefone",
            height=40,
            corner_radius=12,
            border_width=2,
            border_color=get_color("border"),
        )
        self.telefone.pack(fill="x", pady=6)

        self.nascimento = ctk.CTkEntry(
            frame,
            placeholder_text="Data nascimento",
            height=40,
            corner_radius=12,
            border_width=2,
            border_color=get_color("border"),
        )
        self.nascimento.pack(fill="x", pady=6)

       # self.tipo = ctk.CTkOptionMenu(
        #    frame,
         #   values=["Particular", "Convênio"],
          #  fg_color=get_color("accent"),
           # button_color=get_color("sidebar"),
        #)
        #self.tipo.pack(fill="x", pady=6)

        self.plano = ctk.CTkEntry(
            frame,
            placeholder_text="Plano",
            height=40,
            corner_radius=12,
            border_width=2,
            border_color=get_color("border"),
        )
        self.plano.pack(fill="x", pady=6)

        self.carteirinha = ctk.CTkEntry(
            frame,
            placeholder_text="Carteirinha",
            height=40,
            corner_radius=12,
            border_width=2,
            border_color=get_color("border"),
        )
        self.carteirinha.pack(fill="x", pady=6)

        self.endereco = ctk.CTkEntry(
            frame,
            placeholder_text="Endereço",
            height=40,
            corner_radius=12,
            border_width=2,
            border_color=get_color("border"),
        )
        self.endereco.pack(fill="x", pady=6)

        if paciente:
            self.nome.insert(0, paciente["nome"])
            self.cpf.insert(0, paciente["cpf"])
            self.telefone.insert(0, paciente["telefone"])
            self.nascimento.insert(0, paciente.get("nascimento", ""))
           # self.tipo.set(self.tipo)
            self.plano.insert(0, paciente.get("plano") or "")
            self.carteirinha.insert(0, paciente.get("carteirinha", ""))
            self.endereco.insert(0, paciente.get("endereco", ""))

        erro = ctk.CTkLabel(frame, text="", text_color=get_color("danger"))
        erro.pack(pady=5)
        def mostrar_erro(mensagem):
            erro.configure(text=mensagem)

            erro.after(
                4000,
                lambda: erro.configure(text="")
            )

        def salvar():
            if not self.nome.get() or not self.cpf.get():
                mostrar_erro("Nome e CPF obrigatórios")
                return

            try:
                data = self.nascimento.get()
                data_formatada = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
            except Exception as e:
                mostrar_erro("Data de nascimento inválida.")
                return
           
            planos = lista_planos()
            id_plano = None
           
            nome = self.nome.get()
            cpf = self.cpf.get()
            telefone = self.telefone.get()
            nome_plano = self.plano.get().strip()
            carteirinha = self.carteirinha.get()
            endereco = self.endereco.get()
            
            if nome_plano:
                for plano in planos:
                    if plano['nome'].lower() == nome_plano.lower():
                        id_plano = plano['id_plano']
                        break
                if id_plano is None:
                    mostrar_erro("Plano não encontrado")
                    return
           
            _dados = (nome, data_formatada, endereco, cpf, telefone, carteirinha, id_plano)
            if paciente:
                id_paciente = paciente.get("id_paciente")
                confirmar = editar_paciente(id_paciente, _dados)
                if confirmar == "CPF já cadastrado":
                    mostrar_erro(confirmar)
                    return 
                else:
                    CTkMessagebox(title="Sucesso", message=confirmar, icon="check").get()
                          
            else:
                   
                confirmacao = salvar_paciente(_dados)
                if confirmacao == "CPF já cadastrado":
                    mostrar_erro(confirmacao)
                    return 
                else:
                    CTkMessagebox(title="Sucesso", message=confirmacao, icon="check").get()

                    
            
            self.render_lista()
            popup.destroy()

        ctk.CTkButton(
            frame,
            text="Salvar",
            height=42,
            corner_radius=12,
            fg_color=get_color("accent"),
            hover_color=get_color("accent_hover"),
            command=salvar,
        ).pack(pady=20)
    
    def excluir(self, paciente):
        
        msg = CTkMessagebox(
            title="Confirmar exclusão",
            message=f"Deseja excluir o paciente {paciente['nome']}?",
            icon="warning",
            option_1="Cancelar",
            option_2="Excluir",
        )
        if msg.get() == "Excluir":
            id_paciente = paciente.get("id_paciente")
            deletar_paciente(id_paciente)
            self.render_lista()