import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from .theme import get_color
from .loading_overlay import LoadingOverlay
from controllers.paciente_controller import salvar as salvar_paciente, listar as listar_pacientes, editar as editar_paciente, deletar as deletar_paciente, lista_planos
from datetime import datetime


class PatientsView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.configure(fg_color=get_color("bg"))

        self.pacientes = []
        self.filtro_nome = ""

        # Overlay de loading reutilizável (mesmo componente usado na
        # AgendaView e LoginView). Criado uma vez aqui; o render() é
        # chamado várias vezes e não deve recriar o overlay.
        self.loading = LoadingOverlay(self)

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

        # Overlay precisa ser recriado a cada render(), porque render()
        # destrói TODOS os filhos de `self` (`for w in self.winfo_children():
        # w.destroy()`) — isso inclui o frame do overlay, se ele estiver
        # visível no momento. Na prática o overlay só fica visível durante
        # chamadas de rede (que não chamam render() no meio do caminho),
        # então isso raramente importa, mas recriar a instância aqui
        # garante que `self.loading` nunca aponte para um frame morto.
        self.loading = LoadingOverlay(self)

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

        # ------------------------------------------------------------------
        # ANTES: "pacientes = listar_pacientes()" rodava direto aqui,
        # travando a tela até o MySQL na nuvem responder.
        #
        # AGORA: a mesma chamada `listar_pacientes()` roda em thread
        # separada via run_async. O filtro por nome continua sendo
        # aplicado depois, exatamente como antes — só que dentro de
        # `_ao_concluir`, que recebe a lista vinda do banco.
        # ------------------------------------------------------------------
        def _ao_concluir(pacientes):
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

        def _ao_erro(erro):
            CTkMessagebox(
                title="Erro de conexão",
                message=f"Não foi possível carregar os pacientes.\nDetalhe: {erro}",
                icon="cancel",
            )

        self.loading.run_async(
            tarefa=listar_pacientes,
            ao_concluir=_ao_concluir,
            ao_erro=_ao_erro,
            mensagem="Carregando pacientes...",
        )

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

        # ------------------------------------------------------------------
        # NOTA (não relacionada ao loading, mas vale o registro): aqui no
        # original esses valores eram guardados em `self.tipo` / `self.plano`
        # / `self.carteirinha` — atributos da VIEW, não variáveis locais do
        # card. Como `card()` roda em loop para cada paciente, cada
        # iteração sobrescrevia esses atributos; se algo em outro lugar da
        # classe ler `self.plano` depois, ele pega o valor do ÚLTIMO card
        # renderizado, não de um paciente específico. Troquei para
        # variáveis locais (tipo/plano/carteirinha) para evitar esse efeito
        # colateral — o comportamento visual do card permanece idêntico.
        # ------------------------------------------------------------------
        plano = p.get("plano")
        if plano:
            tipo = "Convênio"
        else:
            tipo = "Particular"
            plano = "-"

        ctk.CTkLabel(
           info,
            text=f"Tipo: {tipo} | Plano: {plano}",
            text_color=get_color("text_secondary"),
        ).pack(anchor="w")

        carteirinha = p.get("carteirinha") or "-"

        ctk.CTkLabel(
            info,
            text=f"Cart.: {carteirinha} | Nasc: {p.get('nascimento','-')}",
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

        btn_salvar = None  # referenciado dentro de salvar() para desabilitar durante o loading

        def salvar():
            if not self.nome.get() or not self.cpf.get():
                mostrar_erro("Nome e CPF obrigatórios")
                return

            try:
                data = self.nascimento.get()
                data_formatada = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
            except Exception:
                mostrar_erro("Data de nascimento inválida.")
                return

            nome = self.nome.get()
            cpf = self.cpf.get()
            telefone = self.telefone.get()
            nome_plano = self.plano.get().strip()
            carteirinha = self.carteirinha.get()
            endereco = self.endereco.get()

            # ----------------------------------------------------------
            # ANTES: "lista_planos()" e depois "salvar_paciente(...)" /
            # "editar_paciente(...)" rodavam em sequência, direto na
            # thread principal — duas idas à nuvem, cada uma travando a
            # tela por vez.
            #
            # AGORA: as duas chamadas vão JUNTAS dentro de uma única
            # `tarefa`, que roda inteira em uma única thread em segundo
            # plano. O overlay fica visível do início ao fim das duas
            # chamadas, em vez de aparecer/desaparecer entre elas.
            #
            # A lógica de resolver `id_plano` a partir do nome digitado
            # é exatamente a mesma de antes, só movida para dentro da
            # função que roda na thread.
            # ----------------------------------------------------------
            def _tarefa():
                planos = lista_planos()
                id_plano = None

                if nome_plano:
                    for plano in planos:
                        if plano['nome'].lower() == nome_plano.lower():
                            id_plano = plano['id_plano']
                            break
                    if id_plano is None:
                        return {"erro": "Plano não encontrado"}

                _dados = (nome, data_formatada, endereco, cpf, telefone, carteirinha, id_plano)

                if paciente:
                    id_paciente = paciente.get("id_paciente")
                    resultado = editar_paciente(id_paciente, _dados)
                else:
                    resultado = salvar_paciente(_dados)

                return {"resultado": resultado}

            def _ao_concluir(saida):
                if "erro" in saida:
                    mostrar_erro(saida["erro"])
                    return

                resultado = saida["resultado"]
                if resultado == "CPF já cadastrado":
                    mostrar_erro(resultado)
                    return

                CTkMessagebox(title="Sucesso", message=resultado, icon="check").get()
                self.render_lista()
                popup.destroy()

            def _ao_erro(erro):
                mostrar_erro(f"Erro ao salvar: {erro}")

            self.loading.run_async(
                tarefa=_tarefa,
                ao_concluir=_ao_concluir,
                ao_erro=_ao_erro,
                mensagem="Salvando paciente...",
            )

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

            # ----------------------------------------------------------
            # ANTES: "deletar_paciente(id_paciente)" rodava direto aqui,
            # travando a tela até a exclusão ser confirmada no banco.
            #
            # AGORA: mesma chamada, envolvida em run_async.
            # ----------------------------------------------------------
            def _ao_concluir(resultado):
                self.render_lista()

            def _ao_erro(erro):
                CTkMessagebox(
                    title="Erro ao excluir",
                    message=f"Não foi possível excluir o paciente.\nDetalhe: {erro}",
                    icon="cancel",
                )

            self.loading.run_async(
                tarefa=lambda: deletar_paciente(id_paciente),
                ao_concluir=_ao_concluir,
                ao_erro=_ao_erro,
                mensagem="Excluindo paciente...",
            )