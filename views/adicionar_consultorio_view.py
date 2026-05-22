import tkinter as tk
from tkinter import ttk
from controllers.consultorio_controller import salvar, listar, remover
from tkinter import messagebox

class AdicionarConsultórioView:
    def __init__(self, root):
            frame = ttk.Frame(root)
            frame.pack(fill="both", expand=True)


            self.text_numer = tk.Label(frame, text="Número do consultório")
            self.text_numer.pack()
            self.numero = tk.Entry(frame)
            self.numero.pack()

            self.text_andar = tk.Label(frame, text="Andar do consultório")
            self.text_andar.pack()
            self.andar = tk.Entry(frame)
            self.andar.pack()
            
            self.text_bloco = tk.Label(frame, text="Bloco do consultório")
            self.text_bloco.pack()
            self.bloco = tk.Entry(frame)
            self.bloco.pack()
        
            tk.Button(frame, text="Salvar", command=self.salvar_consultorio).pack()
            
            tk.Button(frame, text="Remover", command=self.remover_consultorio).pack()

            self.tree = ttk.Treeview(frame, columns=("ID","Número do Consultório", "Andar","Bloco"), show="headings")
            for col in ("ID","Número do Consultório", "Andar","Bloco"):
                self.tree.heading(col, text=col)
            self.tree.pack(fill="both", expand=True)
            
            self.listar_consultorios()

    def limpar_campos(self):
         self.numero.delete(0, tk.END),
         self.andar.delete(0, tk.END),
         self.bloco.delete(0, tk.END)

    def salvar_consultorio(self):

        try:
            numero = int(self.numero.get())
            andar = int(self.andar.get())
            bloco = self.bloco.get()

            salvar((numero, andar, bloco))

        except Exception as e:
            messagebox.showerror("ERRO", "Erro ao salvar Consultório, verifique os dados e tente novamente.")
            return
              
        messagebox.showinfo("Sucesso", "Consultório salvo com sucesso!")
        self.listar_consultorios()
        self.limpar_campos()

    def listar_consultorios(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        dados = listar()

        for c in dados:
            self.tree.insert("", "end", values=(c[0], c[1], c[2], c[3]))

    def remover_consultorio(self):
         item_selecionado = self.tree.selection()

         if not item_selecionado:
              messagebox.showwarning("AVISO", "Selecione um consultorio para remover.")
              return

         item = self.tree.item(item_selecionado)
         id_consultorio = item["values"][0]
         confirmar = messagebox.askyesno("Confirmação", "Deseja remover o consultorio?")
         if confirmar:
              remover(id_consultorio)
              self.listar_consultorios()


             