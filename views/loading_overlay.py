"""
loading_overlay.py
────────────────────────────────────────────────────────────────────────
Componente reutilizável de "carregando" para o Clínica VIP.

Por que isso existe:
Como o MySQL é hospedado na nuvem, toda operação (salvar, excluir, listar)
tem uma latência de rede que não existia num banco local. Sem feedback
visual, o usuário não sabe se o clique funcionou e tende a clicar de novo
— o que pode duplicar registros (ex: salvar a mesma consulta duas vezes).

Este componente cobre a tela inteira com um fundo semi-transparente +
spinner girando + texto, e trava interações com a tela de baixo até ser
fechado. Funciona em CIMA de qualquer CTkFrame (AgendaView, PatientsView,
ConfiguracoesView, etc) sem precisar adaptar nada na tela em si.

────────────────────────────────────────────────────────────────────────
COMO USAR (em qualquer tela):

    from .loading_overlay import LoadingOverlay

    class AgendaView(ctk.CTkFrame):
        def __init__(self, master):
            ...
            self.loading = LoadingOverlay(self)   # cria uma vez, escondido

        def salvar_consulta(self, dados):
            self.loading.show("Salvando consulta...")
            try:
                # BACKEND: chamada real ao banco aqui
                # self.consulta_service.criar(dados)
                pass
            finally:
                self.loading.hide()

────────────────────────────────────────────────────────────────────────
COMO USAR COM OPERAÇÃO ASSÍNCRONA (recomendado para chamadas de rede):

Se a chamada ao banco for bloqueante (a maioria das libs MySQL em Python
é síncrona), rodá-la direto na thread principal do Tkinter congela a
interface inteira — o spinner nem chega a girar. Use `run_async` para
disparar a operação numa thread separada e manter a UI responsiva:

    self.loading.run_async(
        tarefa=lambda: self.consulta_service.criar(dados),
        ao_concluir=lambda resultado: self.render(),
        ao_erro=lambda erro: messagebox.showerror("Erro", str(erro)),
        mensagem="Salvando consulta...",
    )
────────────────────────────────────────────────────────────────────────
"""

import customtkinter as ctk
import threading
from .theme import get_color


class LoadingOverlay:
    """Overlay de carregamento reutilizável, para empilhar sobre qualquer
    CTkFrame (a 'tela' onde ele deve aparecer)."""

    def __init__(self, parent):
        # `parent` é a tela (ex: self dentro da AgendaView) sobre a qual
        # o overlay vai aparecer. Ele não é exibido na criação — só
        # quando .show() é chamado.
        self.parent = parent
        self._frame = None
        self._spinner_label = None
        self._mensagem_label = None
        self._angulo = 0
        self._girando = False

        # Caracteres usados para simular o giro do spinner (substitui um
        # ícone girando de verdade, que exigiria imagem/canvas). Simples,
        # leve, e funciona em qualquer plataforma sem dependência extra.
        self._frames_spinner = ["◐", "◓", "◑", "◒"]
        self._frame_atual = 0

    def show(self, mensagem="Carregando..."):
        """Exibe o overlay cobrindo toda a tela `parent`, com a mensagem
        informada. Bloqueia cliques no conteúdo de baixo."""
        if self._frame is not None:
            # Já está visível — só atualiza a mensagem, evita criar
            # overlays duplicados se show() for chamado mais de uma vez.
            self._mensagem_label.configure(text=mensagem)
            return

        # Resolve a cor de fundo do overlay antes de criar o frame.
        # Se a chave "overlay" não existir no seu theme.py, cai para um
        # cinza-escuro fixo — ajuste esse fallback se quiser outro tom.
        try:
            cor_fundo = get_color("overlay")
        except Exception:
            cor_fundo = "#0F172A"

        self._frame = ctk.CTkFrame(
            self.parent,
            fg_color=cor_fundo,
            corner_radius=0,
        )
        # Cobre 100% da área do parent, por cima de tudo que já existe
        self._frame.place(x=0, y=0, relwidth=1, relheight=1)

        container = ctk.CTkFrame(self._frame, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center")

        self._spinner_label = ctk.CTkLabel(
            container,
            text=self._frames_spinner[0],
            font=ctk.CTkFont(size=42),
            text_color=get_color("accent"),
        )
        self._spinner_label.pack(pady=(0, 10))

        self._mensagem_label = ctk.CTkLabel(
            container,
            text=mensagem,
            font=ctk.CTkFont(size=13),
            text_color=get_color("text_secondary"),
        )
        self._mensagem_label.pack()

        # Bloqueia cliques na tela de baixo: como o overlay cobre tudo
        # com relwidth/relheight=1 e fica por cima na ordem de criação,
        # qualquer clique cai nele (que não tem comando nenhum) em vez
        # de vazar para os widgets da tela.
        self._frame.lift()

        self._girando = True
        self._animar()

    def hide(self):
        """Remove o overlay e libera a tela para interação normal."""
        self._girando = False
        if self._frame is not None:
            self._frame.destroy()
            self._frame = None
            self._spinner_label = None
            self._mensagem_label = None

    def _animar(self):
        """Avança o quadro do spinner a cada 120ms enquanto o overlay
        estiver visível. Usa `.after()` do Tkinter — não trava a UI
        porque é só uma troca de texto, não uma operação pesada."""
        if not self._girando or self._spinner_label is None:
            return
        self._frame_atual = (self._frame_atual + 1) % len(self._frames_spinner)
        self._spinner_label.configure(text=self._frames_spinner[self._frame_atual])
        self.parent.after(120, self._animar)

    def run_async(self, tarefa, ao_concluir=None, ao_erro=None, mensagem="Carregando..."):
        """Executa `tarefa` (uma função sem argumentos) numa thread separada,
        mostrando o overlay durante a execução, e volta para a thread
        principal do Tkinter para aplicar o resultado.

        Isso existe porque bibliotecas de MySQL em Python (mysql-connector,
        PyMySQL, etc) são bloqueantes: se você chamar `cursor.execute(...)`
        direto num botão, a janela inteira congela até a rede responder.
        Rodar numa thread mantém o spinner girando e a janela arrastável
        enquanto espera o banco na nuvem responder.

        BACKEND: é AQUI que entram suas chamadas reais de banco. Exemplo:

            self.loading.run_async(
                tarefa=lambda: self.consulta_service.listar_por_data(data),
                ao_concluir=lambda lista: self._aplicar_lista(lista),
                ao_erro=lambda e: messagebox.showerror("Erro de conexão", str(e)),
                mensagem="Carregando consultas...",
            )
        """
        self.show(mensagem)

        def _worker():
            try:
                resultado = tarefa()
                erro = None
            except Exception as e:
                resultado = None
                erro = e

            # Tkinter não é thread-safe: widgets só podem ser tocados na
            # thread principal. Por isso o resultado volta via `.after()`,
            # que agenda a execução de volta no loop principal do Tk.
            def _finalizar():
                self.hide()
                if erro is not None:
                    if ao_erro:
                        ao_erro(erro)
                else:
                    if ao_concluir:
                        ao_concluir(resultado)

            self.parent.after(0, _finalizar)

        threading.Thread(target=_worker, daemon=True).start()