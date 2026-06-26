import customtkinter as ctk
from controllers.consulta_controller import ConsultaContrroler
from datetime import datetime, timedelta
from tkinter import filedialog, messagebox
import time 
import os
import re
from .theme import get_color
from .loading_overlay import LoadingOverlay


# ──────────────────────────────────────────────────────────────────────────
# Mapeamento de cores por status. Centralizado aqui pra facilitar manutenção
# (se mudar a paleta do app, ajusta só essas chaves).
# ──────────────────────────────────────────────────────────────────────────
STATUS_COLORS = {
    "Agendado": "#3B82F6",   # azul
    "Chegou": "#F59E0B",     # amarelo/âmbar
    "Atendido": "#22C55E",   # verde
}

STATUS_OPCOES = ["Agendado", "Chegou"]


class AgendaView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.bg = get_color("bg")
        self.panel = get_color("panel")
        self.card_color = get_color("card")
        self.soft = get_color("surface_dark")
        self.primary = get_color("accent")
        self.accent = get_color("accent")
        self.text_dark = get_color("text")

        self.configure(fg_color=self.bg)

        self.data_atual = datetime.now()
        self.medicos = []
        self.arquivos_pdf = []
        self.consulta_controller = ConsultaContrroler()

        self.consultas = []

        self.dados_medico = []
        self.dados_paciente = []

        self._montar_header()

        self.lista = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.lista.pack(fill="both", expand=True, padx=20, pady=10)

        self.loading = LoadingOverlay(self)

        self.update_data()
        self._carregar_dados_iniciais()

    def _carregar_dados_iniciais(self):
        def _tarefa():
            inicio = time.time()
            dados_medico = self.consulta_controller.lista_medico()
            dados_paciente = self.consulta_controller.lista_paciente()
            consultas = self.consulta_controller.listar()
            print(dados_medico)
            print(f"Tempo de carregamento inicial (médicos + pacientes + consultas): {time.time() - inicio:.2f}s")
            return dados_medico, dados_paciente, consultas

        def _ao_concluir(resultado):
            self.dados_medico, self.dados_paciente, self.consultas = resultado
            for medico in self.dados_medico:
                self.medicos.append(medico['nome'])

            self.update_data()
            self._renderizar_consultas_do_dia()

        def _ao_erro(erro):
            messagebox.showerror(
                "Erro ao carregar agenda",
                f"Não foi possível carregar a agenda.\nDetalhe: {erro}",
            )

        self.loading.run_async(
            tarefa=_tarefa,
            ao_concluir=_ao_concluir,
            ao_erro=_ao_erro,
            mensagem="Carregando agenda...",
        )

    def _montar_header(self):
        header = ctk.CTkFrame(
            self,
            fg_color=self.panel,
            corner_radius=20,
            height=100,
        )
        header.pack(fill="x", padx=20, pady=(20, 10))
        header.pack_propagate(False)

        titulo_frame = ctk.CTkFrame(header, fg_color="transparent")
        titulo_frame.place(x=25, y=18)

        ctk.CTkLabel(
            titulo_frame,
            text="📅 Agenda Clínica",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=get_color("text"),
        ).pack(anchor="w")

        self.label_contador = ctk.CTkLabel(
            titulo_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=get_color("text_secondary"),
        )
        self.label_contador.pack(anchor="w")

        data_frame = ctk.CTkFrame(header, fg_color="transparent")
        data_frame.pack(side="right", padx=15, pady=20)

        ctk.CTkButton(
            data_frame,
            text="◀",
            width=35,
            fg_color=self.soft,
            text_color=self.accent,
            command=self.voltar,
        ).pack(side="left", padx=2)

        self.label_data = ctk.CTkLabel(
            data_frame,
            text="",
            text_color=get_color("text"),
            font=ctk.CTkFont(size=14, weight="bold"),
            width=140,
        )
        self.label_data.pack(side="left", padx=10)

        ctk.CTkButton(
            data_frame,
            text="▶",
            width=35,
            fg_color=self.soft,
            text_color=self.accent,
            command=self.avancar,
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            data_frame,
            text="Hoje",
            width=60,
            fg_color=self.primary,
            hover_color=get_color("accent_hover"),
            command=self.ir_hoje,
        ).pack(side="left", padx=5)

        self.input_data = ctk.CTkEntry(
            data_frame,
            width=110,
            placeholder_text="dd/mm/aaaa",
        )
        self.input_data.pack(side="left", padx=5)
        self.input_data.bind("<Return>", lambda e: self.ir_data())

        ctk.CTkButton(
            data_frame,
            text="Ir",
            width=40,
            fg_color=self.accent,
            command=self.ir_data,
        ).pack(side="left")

        ctk.CTkButton(
            header,
            text="+ Nova consulta",
            fg_color=self.primary,
            hover_color=get_color("accent_hover"),
            corner_radius=18,
            command=lambda: self.popup(),
        ).pack(side="right", padx=15)

    def update_data(self):
        self.label_data.configure(text=self.data_atual.strftime("%d/%m/%Y"))

        data_str = self.data_atual.strftime("%d/%m/%Y")
        total = len([c for c in self.consultas if c["data"] == data_str])
        if total == 0:
            self.label_contador.configure(text="Nenhuma consulta")
        elif total == 1:
            self.label_contador.configure(text="1 consulta")
        else:
            self.label_contador.configure(text=f"{total} consultas")

    def avancar(self):
        self.data_atual += timedelta(days=1)
        self.update_data()
        self.render()

    def voltar(self):
        self.data_atual -= timedelta(days=1)
        self.update_data()
        self.render()

    def ir_hoje(self):
        self.data_atual = datetime.now()
        self.update_data()

        # ------------------------------------------------------------------
        # ANTES: "self.consultas = self.consulta_controller.listar()"
        # rodava direto aqui, travando a tela sem nenhum feedback visual
        # até a nuvem responder.
        #
        # AGORA: mesma chamada, em thread separada via run_async, com o
        # overlay de loading visível durante a espera. Ao concluir,
        # _renderizar_consultas_do_dia() desenha os cards a partir dos
        # dados já atualizados em memória.
        # ------------------------------------------------------------------
        def _ao_concluir(consultas):
            self.consultas = consultas
            self._renderizar_consultas_do_dia()

        def _ao_erro(erro):
            messagebox.showerror(
                "Erro ao carregar consultas",
                f"Não foi possível carregar as consultas de hoje.\nDetalhe: {erro}",
            )

        self.loading.run_async(
            tarefa=self.consulta_controller.listar,
            ao_concluir=_ao_concluir,
            ao_erro=_ao_erro,
            mensagem="Carregando consultas...",
        )

    def ir_data(self):
        texto = self.input_data.get().strip()
        try:
            nova_data = datetime.strptime(texto, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror(
                "Data inválida",
                "Digite a data no formato dd/mm/aaaa.\nEx: 25/12/2026",
            )
            self.input_data.focus_set()
            return

        # ------------------------------------------------------------------
        # ANTES: "self.consultas = self.consulta_controller.listar_por_data(...)"
        # rodava direto aqui, travando a tela sem feedback visual.
        #
        # AGORA: mesma chamada, em thread separada via run_async — mesmo
        # padrão de ir_hoje(). self.data_atual só é atualizada dentro de
        # _ao_concluir, depois que os dados já chegaram, para não mudar
        # a data exibida no header antes de saber se a busca deu certo.
        # ------------------------------------------------------------------
        def _ao_concluir(consultas):
            self.consultas = consultas
            self.data_atual = nova_data
            self.update_data()
            self._renderizar_consultas_do_dia()

        def _ao_erro(erro):
            messagebox.showerror(
                "Erro ao carregar consultas",
                f"Não foi possível carregar as consultas para essa data.\nDetalhe: {erro}",
            )

        self.loading.run_async(
            tarefa=lambda: self.consulta_controller.listar_por_data(nova_data),
            ao_concluir=_ao_concluir,
            ao_erro=_ao_erro,
            mensagem="Carregando consultas...",
        )

    def formatar_cpf(self, texto):
        nums = "".join(filter(str.isdigit, texto))[:11]
        if len(nums) <= 3:
            return nums
        elif len(nums) <= 6:
            return f"{nums[:3]}.{nums[3:]}"
        elif len(nums) <= 9:
            return f"{nums[:3]}.{nums[3:6]}.{nums[6:]}"
        return f"{nums[:3]}.{nums[3:6]}.{nums[6:9]}-{nums[9:]}"

    def formatar_data(self, texto):
        nums = "".join(filter(str.isdigit, texto))[:8]
        if len(nums) <= 2:
            return nums
        elif len(nums) <= 4:
            return f"{nums[:2]}/{nums[2:]}"
        return f"{nums[:2]}/{nums[2:4]}/{nums[4:]}"

    def formatar_hora(self, texto):
        nums = "".join(filter(str.isdigit, texto))[:4]

        if len(nums) >= 2:
            hh = int(nums[:2])
            if hh > 23:
                nums = "23" + nums[2:]

        if len(nums) == 4:
            mm = int(nums[2:4])
            if mm > 59:
                nums = nums[:2] + "59"

        if len(nums) <= 2:
            return nums
        return f"{nums[:2]}:{nums[2:]}"

    def ocultar_cpf(self, cpf):
        nums = "".join(filter(str.isdigit, cpf))
        if len(nums) < 11:
            return cpf
        return f"{nums[:3]}.***.***-{nums[-2:]}"

    def _validar_cpf_completo(self, cpf):
        nums = "".join(filter(str.isdigit, cpf))
        return len(nums) == 11

    def _validar_hora(self, texto):
        return bool(re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", texto.strip()))

    def _validar_data(self, texto):
        try:
            datetime.strptime(texto.strip(), "%d/%m/%Y")
            return True
        except ValueError:
            return False

    def _renderizar_consultas_do_dia(self):
        inicio = time.time()
        for w in self.lista.winfo_children():
            w.destroy()

        data = self.data_atual.strftime("%d/%m/%Y")

        consultas_do_dia = [c for c in self.consultas if c["data"] == data]
        consultas_do_dia.sort(key=lambda c: c.get("hora", ""))

        if not consultas_do_dia:
            ctk.CTkLabel(
                self.lista,
                text="📭 Nenhuma consulta neste dia",
                text_color=self.text_dark,
                font=ctk.CTkFont(size=14),
            ).pack(pady=50)
        else:
            for c in consultas_do_dia:
                self.card(c)

        print("render:", time.time() - inicio)

    def render(self):
        """Filtra e redesenha a partir de self.consultas, que já está em
        memória — SEM ir ao banco. Usado pela navegação de data
        (avancar/voltar), que só precisa re-filtrar o que já foi
        carregado, sem precisar de uma nova ida à nuvem a cada troca de
        dia.

        ir_hoje() e ir_data() têm sua própria busca via run_async (com
        loading), já que ambas podem precisar de dados que não estão em
        self.consultas ainda — por exemplo, ir_data() para uma data fora
        do período já carregado em memória."""
        self._renderizar_consultas_do_dia()

    def _recarregar_e_renderizar(self):
        def _ao_concluir(consultas):
            self.consultas = consultas
            self._renderizar_consultas_do_dia()

        def _ao_erro(erro):
            messagebox.showerror(
                "Erro ao carregar consultas",
                f"Não foi possível carregar as consultas.\nDetalhe: {erro}",
            )

        self.loading.run_async(
            tarefa=self.consulta_controller.listar,
            ao_concluir=_ao_concluir,
            ao_erro=_ao_erro,
            mensagem="Carregando consultas...",
        )

    def card(self, c):
        card = ctk.CTkFrame(self.lista, fg_color=self.card_color, corner_radius=16)
        card.pack(fill="x", pady=6)

        cor_status = STATUS_COLORS.get(c.get("status", "Agendado"), self.primary)

        bar = ctk.CTkFrame(card, width=6, fg_color=cor_status, corner_radius=10)
        bar.pack(side="left", fill="y")

        container = ctk.CTkFrame(card, fg_color="transparent")
        container.pack(fill="x", expand=True, padx=15, pady=15)

        hora = ctk.CTkLabel(
            container,
            text=c["hora"],
            width=70,
            height=32,
            fg_color=self.soft,
            text_color=self.accent,
            corner_radius=10,
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        hora.pack(side="left", padx=(0, 15))

        info = ctk.CTkFrame(container, fg_color="transparent")
        info.pack(side="left", expand=True, fill="x")

        ctk.CTkLabel(
            info,
            text=c["paciente"],
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=get_color("text"),
            anchor="w",
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=f"CPF: {self.ocultar_cpf(c['cpf'])}   •   {c['medico']}",
            text_color=get_color("text_secondary"),
            font=ctk.CTkFont(size=12),
            anchor="w",
        ).pack(anchor="w")

        if c.get("anexos"):
            ctk.CTkLabel(
                info,
                text=f"📎 {len(c['anexos'])} anexo(s)",
                text_color=get_color("text_secondary"),
                font=ctk.CTkFont(size=11),
                anchor="w",
            ).pack(anchor="w", pady=(2, 0))

        lado_direito = ctk.CTkFrame(container, fg_color="transparent")
        lado_direito.pack(side="right")

        ctk.CTkLabel(
            lado_direito,
            text=f"  {c.get('status', 'Agendado')}  ",
            fg_color=cor_status,
            text_color="#FFFFFF",
            corner_radius=10,
            font=ctk.CTkFont(size=11, weight="bold"),
            height=26,
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            lado_direito,
            text="Editar",
            width=80,
            height=32,
            corner_radius=14,
            fg_color=self.primary,
            hover_color=get_color("accent_hover"),
            command=lambda c=c: self.popup(c),
        ).pack(side="left")

    def popup(self, consulta=None):
        popup = ctk.CTkToplevel(self)
        popup.title("Editar consulta" if consulta else "Nova consulta")
        popup.geometry("420x600")
        popup.grab_set()
        popup.configure(fg_color=self.card_color)
        popup.resizable(False, False)

        frame = ctk.CTkScrollableFrame(popup, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            frame,
            text="📋 Editar consulta" if consulta else "📋 Nova consulta",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=get_color("text"),
        ).pack(pady=(0, 15))

        ctk.CTkLabel(frame, text="Paciente *", anchor="w",
                     text_color=get_color("text_secondary"),
                     font=ctk.CTkFont(size=12)).pack(fill="x")
        paciente = ctk.CTkEntry(frame, placeholder_text="Nome completo")
        paciente.pack(fill="x", pady=(2, 12))

        ctk.CTkLabel(frame, text="CPF *", anchor="w",
                     text_color=get_color("text_secondary"),
                     font=ctk.CTkFont(size=12)).pack(fill="x")
        cpf = ctk.CTkEntry(frame, placeholder_text="000.000.000-00")
        cpf.pack(fill="x", pady=(2, 12))

        def _on_cpf_change(event=None):
            texto = cpf.get()
            formatado = self.formatar_cpf(texto)
            if formatado != texto:
                cpf.delete(0, "end")
                cpf.insert(0, formatado)
        cpf.bind("<KeyRelease>", _on_cpf_change)

        ctk.CTkLabel(frame, text="Médico *", anchor="w",
                     text_color=get_color("text_secondary"),
                     font=ctk.CTkFont(size=12)).pack(fill="x")
        medico = ctk.CTkOptionMenu(frame, values=self.medicos)
        medico.pack(fill="x", pady=(2, 12))

        linha_data_hora = ctk.CTkFrame(frame, fg_color="transparent")
        linha_data_hora.pack(fill="x", pady=(0, 12))

        col_data = ctk.CTkFrame(linha_data_hora, fg_color="transparent")
        col_data.pack(side="left", fill="x", expand=True, padx=(0, 6))
        ctk.CTkLabel(col_data, text="Data *", anchor="w",
                     text_color=get_color("text_secondary"),
                     font=ctk.CTkFont(size=12)).pack(fill="x")
        data = ctk.CTkEntry(col_data, placeholder_text="dd/mm/aaaa")
        data.pack(fill="x", pady=(2, 0))

        def _on_data_change(event=None):
            texto = data.get()
            formatado = self.formatar_data(texto)
            if formatado != texto:
                data.delete(0, "end")
                data.insert(0, formatado)
        data.bind("<KeyRelease>", _on_data_change)

        col_hora = ctk.CTkFrame(linha_data_hora, fg_color="transparent")
        col_hora.pack(side="left", fill="x", expand=True, padx=(6, 0))
        ctk.CTkLabel(col_hora, text="Hora *", anchor="w",
                     text_color=get_color("text_secondary"),
                     font=ctk.CTkFont(size=12)).pack(fill="x")
        hora = ctk.CTkEntry(col_hora, placeholder_text="HH:MM")
        hora.pack(fill="x", pady=(2, 0))

        def _on_hora_change(event=None):
            texto = hora.get()
            formatado = self.formatar_hora(texto)
            if formatado != texto:
                hora.delete(0, "end")
                hora.insert(0, formatado)
        hora.bind("<KeyRelease>", _on_hora_change)

        ctk.CTkLabel(frame, text="Status", anchor="w",
                     text_color=get_color("text_secondary"),
                     font=ctk.CTkFont(size=12)).pack(fill="x")
        status = ctk.CTkOptionMenu(frame, values=STATUS_OPCOES)
        status.pack(fill="x", pady=(2, 12))

        if consulta:
            anexos = [
                {
                    "nome_original": a["nome_original"],
                    "caminho": None,
                    "caminho_storage": a["caminho_storage"],
                    "id_documento": a["id_documento"],              
                }
                for a in consulta.get("anexos", [])
            ]
        else:
            anexos = []
        
        if consulta:
            paciente.insert(0, consulta.get("paciente", ""))
            cpf.insert(0, consulta.get("cpf", ""))

            paciente.configure(state="disabled")
            cpf.configure(state="disabled")

            medico.set(consulta.get("medico", self.medicos[0]))
            data.insert(0, consulta.get("data", ""))
            hora.insert(0, consulta.get("hora", ""))
            status.set(consulta.get("status", "Agendado"))
        else:
            data.insert(0, self.data_atual.strftime("%d/%m/%Y"))
            status.set("Agendado")

        ctk.CTkLabel(frame, text="Anexos (PDF)", anchor="w",
                     text_color=get_color("text_secondary"),
                     font=ctk.CTkFont(size=12)).pack(fill="x")

        box = ctk.CTkTextbox(frame, height=70)
        box.pack(fill="x", pady=(2, 5))

        def _redesenhar_anexos():
            box.delete("1.0", "end")
            for a in anexos:
                box.insert("end", os.path.basename(a["nome_original"]) + "\n")
        _redesenhar_anexos()
        box.configure(state="disabled")

        def adicionar_anexo():
            arq = filedialog.askopenfilename(
                title="Selecionar PDF",
                filetypes=[("Arquivos PDF", "*.pdf")],
            )
            if not arq:
                return

            nome_arquivo = os.path.basename(arq)

            ja_existe = any(
                a["nome_original"].lower() == nome_arquivo.lower()
                for a in anexos
            )
            if ja_existe:
                messagebox.showwarning(
                    "Arquivo já anexado",
                    f"O arquivo \"{nome_arquivo}\" já está anexado a esta consulta.",
                )
                return

            anexos.append({
                "nome_original": os.path.basename(arq),
                "caminho": arq,
                "tipo": "pdf"
            })
            box.configure(state="normal")
            _redesenhar_anexos()
            box.configure(state="disabled")

        def abrir_ultimo_anexo():
            if not anexos:
                messagebox.showinfo("Anexos", "Nenhum arquivo anexado ainda.")
                return

            ultimo = anexos[-1]

            if ultimo["caminho"] is not None:
                try:
                    self.abrir_arquivo(ultimo["caminho"])
                except Exception as e:
                    messagebox.showerror("ERRO", str(e))
                return

            def _ao_concluir(caminho):
                try:
                    self.abrir_arquivo(caminho)
                except Exception as e:
                    messagebox.showerror("ERRO", str(e))

            def _ao_erro(erro):
                messagebox.showerror("ERRO", str(erro))

            self.loading.run_async(
                tarefa=lambda: self.consulta_controller.baixar_anexo(ultimo["caminho_storage"]),
                ao_concluir=_ao_concluir,
                ao_erro=_ao_erro,
                mensagem="Baixando anexo...",
            )

        def remover_ultimo_anexo():
            if not anexos:
                messagebox.showinfo("Anexos", "Nenhum arquivo anexado ainda.")
                return
            anexos.pop()
            box.configure(state="normal")
            _redesenhar_anexos()
            box.configure(state="disabled")

        linha_anexos = ctk.CTkFrame(frame, fg_color="transparent")
        linha_anexos.pack(fill="x", pady=(0, 5))

        ctk.CTkButton(
            linha_anexos, text="+ Anexar PDF", height=32,
            command=adicionar_anexo,
        ).pack(fill="x")

        linha_anexos2 = ctk.CTkFrame(frame, fg_color="transparent")
        linha_anexos2.pack(fill="x", pady=(0, 15))

        ctk.CTkButton(
            linha_anexos2, text="📂 Abrir último anexo", height=30,
            fg_color=self.soft, text_color=self.accent,
            command=abrir_ultimo_anexo,
        ).pack(side="left", expand=True, fill="x", padx=(0, 4))

        ctk.CTkButton(
            linha_anexos2, text="🗑", width=44, height=30,
            fg_color="#7C2D2D", hover_color="#9B3A3A",
            command=remover_ultimo_anexo,
        ).pack(side="left", padx=(4, 0))

        def validar_formulario():
            erros = []
            if not paciente.get().strip():
                erros.append("Nome do paciente é obrigatório.")
            if not self._validar_cpf_completo(cpf.get()):
                erros.append("CPF incompleto. Use o formato 000.000.000-00.")
            if not self._validar_data(data.get()):
                erros.append("Data inválida. Use o formato dd/mm/aaaa.")
            if not self._validar_hora(hora.get()):
                erros.append("Hora inválida. Use o formato HH:MM (24h).")
            return erros

        def salvar():
            inicio = time.time()
            erros = validar_formulario()
            if erros:
                messagebox.showerror("Verifique os campos", "\n".join(erros))
                return

            id_paciente = None
            id_medico = None
            tipo_atendimento = None

            nome_paciente = paciente.get().strip()
            cpf_paciente = cpf.get().strip()
            nome_medico = medico.get()
            data_consulta = data.get().strip()
            hora_consulta = hora.get().strip()
            status_consulta = status.get()
            arquivos_pdf = anexos
            
            data_formatada = datetime.strptime(data_consulta, "%d/%m/%Y").strftime("%Y-%m-%d")

            for p in self.dados_paciente:
                if p["nome"].lower() == nome_paciente.lower() and p["cpf"] == cpf_paciente:
                    id_paciente = p["id_paciente"]
                    tipo_atendimento = p["id_plano"]
                    break
            if id_paciente is None:
                messagebox.showwarning("Atenção", "Paciente ou CPF não contrado!")
                return

            if tipo_atendimento is None:
                tipo_atendimento = "particular"
            else:
                tipo_atendimento = "plano"
            
            for m in self.dados_medico:
                if m["nome"].lower() == nome_medico.lower():
                    id_medico = m["id_medico"]
                    break
            if id_medico is None:
                messagebox.showwarning("Atenção", "Medico não contrado!")
                return

            if consulta:
                def _tarefa():
                    return self.consulta_controller.editar(
                        id_consulta=consulta["id_consulta"],
                        data_consulta=data_formatada,
                        hora_consulta=hora_consulta,
                        status_consulta=status_consulta,
                        tipo_atendimento=tipo_atendimento,
                        id_medico=id_medico,
                        arquivos_pdf=anexos,
                        anexos_antigos=consulta["anexos"],
                    )

                def _ao_concluir(resultado_editar):
                    if resultado_editar["sucesso"]:
                        if resultado_editar["erros_upload"]:
                            messagebox.showwarning(
                                "Consulta salva",
                                "A consulta foi salva, porém alguns documentos não puderam ser anexados:\n\n"
                                + "\n".join(resultado_editar["erros_upload"])
                            )
                        else:
                            messagebox.showinfo(
                                "Sucesso",
                                "Consulta editada com sucesso."
                            )

                    self.update_data()
                    self._recarregar_e_renderizar()
                    print("salvar:", time.time() - inicio)
                    popup.destroy()

            else:
                def _tarefa():
                    return self.consulta_controller.salvar(
                        data_consulta=data_formatada,
                        hora_consulta=hora_consulta,
                        status_consulta=status_consulta,
                        tipo_atendimento=tipo_atendimento,
                        id_paciente=id_paciente,
                        id_medico=id_medico,
                        arquivos_pdf=arquivos_pdf,
                    )

                def _ao_concluir(resultado):
                    if resultado["sucesso"]:
                        if resultado["erros_upload"]:
                            messagebox.showwarning(
                                "Consulta salva",
                                "A consulta foi salva, porém alguns documentos não puderam ser anexados:\n\n"
                                + "\n".join(resultado["erros_upload"])
                            )
                        else:
                            messagebox.showinfo(
                                "Sucesso",
                                "Consulta salva com sucesso."
                            )

                    self.update_data()
                    self._recarregar_e_renderizar()
                    print("salvar:", time.time() - inicio)
                    popup.destroy()

            def _ao_erro(erro):
                messagebox.showerror(
                    "Erro ao salvar",
                    f"Não foi possível salvar a consulta.\nDetalhe: {erro}",
                )

            self.loading.run_async(
                tarefa=_tarefa,
                ao_concluir=_ao_concluir,
                ao_erro=_ao_erro,
                mensagem="Salvando consulta...",
            )

        def excluir():
            confirmar = messagebox.askyesno(
                "Excluir consulta",
                f"Tem certeza que deseja excluir a consulta de "
                f"{consulta.get('paciente', '')}?\nEsta ação não pode ser desfeita.",
            )
            if not confirmar:
                return

            self.consultas.remove(consulta)
            self.update_data()
            self.render()
            popup.destroy()

        btns = ctk.CTkFrame(frame, fg_color="transparent")
        btns.pack(fill="x", pady=(5, 0))

        ctk.CTkButton(
            btns,
            text="Cancelar",
            fg_color=self.soft,
            text_color=self.accent,
            command=popup.destroy,
        ).pack(side="left", expand=True, padx=5)

        ctk.CTkButton(
            btns,
            text="Salvar",
            fg_color=self.primary,
            hover_color=get_color("accent_hover"),
            command=salvar,
        ).pack(side="left", expand=True, padx=(5, 0))

    def abrir_arquivo(self, caminho):
        if not os.path.exists(caminho):
            messagebox.showerror("Arquivo não encontrado", f"O arquivo não existe mais:\n{caminho}")
            return
        try:
            os.startfile(caminho)
        except AttributeError:
            messagebox.showerror("Não suportado", "Abrir arquivos automaticamente só funciona no Windows por enquanto.")
        except OSError as e:
            messagebox.showerror("Erro ao abrir arquivo", str(e))