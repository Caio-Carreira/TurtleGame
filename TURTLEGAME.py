import turtle
import tkinter as tk
from tkinter import ttk, messagebox
import random
import math

class TurtleGame:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Aventura da Tartaruga - Lince Games")
        self.janela.configure(bg="#F0F8FF")
        self.janela.geometry("1200x700")
        
        self.cores = {
            "fundo": "#F0F8FF",
            "destaque": "#4682B4",
            "texto": "#2A4D69",
            "botao": "#5F9EA0",
            "borda": "#B0C4DE"
        }
        
        self.fontes = {
            "titulo": ("Segoe UI", 20, "bold"),
            "subtitulo": ("Segoe UI", 14, "bold"),
            "texto": ("Segoe UI", 12),
            "botao": ("Segoe UI", 12, "bold")
        }
        
        self.history = []
        self.setup_turtle()
        self.criar_interface()
        self.configurar_teclado()
        
        self.janela.mainloop()

    def setup_turtle(self):
        self.canvas = turtle.ScrolledCanvas(self.janela, width=800, height=600)
        self.canvas.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.screen = turtle.TurtleScreen(self.canvas)
        self.screen.bgcolor("#FFFFFF")
        
        self.t = turtle.RawTurtle(self.screen)
        self.t.shape("turtle")
        self.t.shapesize(2, 2)
        self.t.color("#5F9EA0")
        self.t.speed(5)
        self.t.pensize(3)

    def criar_interface(self):
        controles_frame = tk.Frame(self.janela, bg=self.cores["fundo"], bd=2, relief=tk.GROOVE)
        controles_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.criar_titulo(controles_frame)
        self.criar_secao_movimento(controles_frame)
        self.criar_secao_aparencia(controles_frame)
        self.criar_secao_caneta(controles_frame)
        self.criar_secao_acoes(controles_frame)
        
        self.janela.grid_columnconfigure(0, weight=0)
        self.janela.grid_columnconfigure(1, weight=1)
        self.janela.grid_rowconfigure(0, weight=1)

    def criar_titulo(self, parent):
        titulo_frame = tk.Frame(parent, bg=self.cores["fundo"])
        titulo_frame.pack(pady=15, fill=tk.X)
        
        tk.Label(
            titulo_frame,
            text="🐢 AVENTURA DA TARTARUGA 🐢",
            bg=self.cores["fundo"],
            fg=self.cores["destaque"],
            font=self.fontes["titulo"]
        ).pack()

    def criar_secao_movimento(self, parent):
        frame = tk.LabelFrame(
            parent,
            text=" Controles de Movimento ",
            bg=self.cores["fundo"],
            fg=self.cores["texto"],
            font=self.fontes["subtitulo"],
            padx=15,
            pady=15
        )
        frame.pack(fill=tk.X, padx=5, pady=5, ipady=5)
        
        # Controles de ângulo e distância
        ttk.Label(frame, text="Ângulo (0-360°):", background=self.cores["fundo"], font=self.fontes["texto"]).grid(row=0, column=0, sticky="w", pady=5)
        self.angulo_spin = ttk.Spinbox(frame, from_=0, to=360, width=8, font=self.fontes["texto"])
        self.angulo_spin.grid(row=0, column=1, pady=5, padx=5)
        self.angulo_spin.set(0)
        
        ttk.Label(frame, text="Distância:", background=self.cores["fundo"], font=self.fontes["texto"]).grid(row=1, column=0, sticky="w", pady=5)
        self.distancia_spin = ttk.Spinbox(frame, from_=1, to=100, width=8, font=self.fontes["texto"])
        self.distancia_spin.grid(row=1, column=1, pady=5, padx=5)
        self.distancia_spin.set(20)
        
        ttk.Button(frame, text="MOVER", command=self.aplicar_movimento, style="TButton").grid(row=2, columnspan=2, pady=10)

    def criar_secao_aparencia(self, parent):
        frame = tk.LabelFrame(
            parent,
            text=" Aparência da Tartaruga ",
            bg=self.cores["fundo"],
            fg=self.cores["texto"],
            font=self.fontes["subtitulo"],
            padx=15,
            pady=15
        )
        frame.pack(fill=tk.X, padx=5, pady=5, ipady=5)
        
        # Cores da tartaruga
        ttk.Label(frame, text="Cor:", background=self.cores["fundo"], font=self.fontes["texto"]).grid(row=0, column=0, sticky="w")
        cores_frame = tk.Frame(frame, bg=self.cores["fundo"])
        cores_frame.grid(row=0, column=1, columnspan=2)
        
        cores = ["#FF5733", "#4CAF50", "#3498DB", "#9B59B6", "#F1C40F"]
        for cor in cores:
            btn = tk.Button(cores_frame, bg=cor, width=3, command=lambda c=cor: self.t.color(c))
            btn.pack(side=tk.LEFT, padx=2)
        
        # Velocidade
        ttk.Label(frame, text="Velocidade:", background=self.cores["fundo"], font=self.fontes["texto"]).grid(row=1, column=0, sticky="w", pady=5)
        self.velocidade = ttk.Scale(frame, from_=1, to=10, command=lambda v: self.t.speed(int(v)))
        self.velocidade.grid(row=1, column=1, sticky="ew")
        self.velocidade.set(5)

    def criar_secao_caneta(self, parent):
        frame = tk.LabelFrame(
            parent,
            text=" Configurações da Caneta ",
            bg=self.cores["fundo"],
            fg=self.cores["texto"],
            font=self.fontes["subtitulo"],
            padx=15,
            pady=15
        )
        frame.pack(fill=tk.X, padx=5, pady=5, ipady=5)
        
        # Espessura
        ttk.Label(frame, text="Espessura:", background=self.cores["fundo"], font=self.fontes["texto"]).grid(row=0, column=0, sticky="w")
        self.espessura_spin = ttk.Spinbox(frame, from_=1, to=10, width=8, font=self.fontes["texto"])
        self.espessura_spin.grid(row=0, column=1, padx=5)
        self.espessura_spin.set(3)
        
        # Cores da linha
        ttk.Label(frame, text="Cor da Linha:", background=self.cores["fundo"], font=self.fontes["texto"]).grid(row=1, column=0, sticky="w", pady=5)
        cores_frame = tk.Frame(frame, bg=self.cores["fundo"])
        cores_frame.grid(row=1, column=1, columnspan=2)
        
        cores = ["#000000", "#FF0000", "#00FF00", "#0000FF", "#FF00FF", "#FFFFFF"]
        for cor in cores:
            if cor == "#FFFFFF":
                btn = tk.Button(cores_frame, bg=cor, width=3, command=self.t.penup)
                btn.config(text="✖", fg="red")
            else:
                btn = tk.Button(cores_frame, bg=cor, width=3, command=lambda c=cor: [self.t.pendown(), self.t.pencolor(c)])
            btn.pack(side=tk.LEFT, padx=2)

    def criar_secao_acoes(self, parent):
        frame = tk.LabelFrame(
            parent,
            text=" Ações ",
            bg=self.cores["fundo"],
            fg=self.cores["texto"],
            font=self.fontes["subtitulo"],
            padx=15,
            pady=15
        )
        frame.pack(fill=tk.X, padx=5, pady=5, ipady=5)
        
        ttk.Button(frame, text="Limpar Tela", command=self.limpar_tela).pack(pady=5, fill=tk.X)
        ttk.Button(frame, text="Desenhar Forma", command=self.desenhar_forma_automatica).pack(pady=5, fill=tk.X)
        ttk.Button(frame, text="Desfazer", command=self.desfazer_ultimo_movimento).pack(pady=5, fill=tk.X)
        ttk.Button(frame, text="Ajuda", command=self.mostrar_ajuda).pack(pady=5, fill=tk.X)

    def configurar_teclado(self):
        self.screen.listen()
        self.screen.onkey(self.mover_frente, "w")
        self.screen.onkey(self.mover_tras, "s")
        self.screen.onkey(self.girar_esquerda, "a")
        self.screen.onkey(self.girar_direita, "d")
        self.screen.onkey(self.limpar_tela, "c")
        self.screen.onkey(self.desenhar_forma_automatica, "f")

    def salvar_estado(self):
        estado = {
            'pos': self.t.position(),
            'heading': self.t.heading(),
            'pencolor': self.t.pencolor(),
            'pensize': self.t.pensize(),
            'pendown': self.t.isdown(),
            'color': self.t.color()
        }
        self.history.append(estado)

    def desfazer_ultimo_movimento(self):
        if len(self.history) > 0:
            estado_anterior = self.history.pop()
            self.t.penup()
            self.t.setposition(estado_anterior['pos'])
            self.t.setheading(estado_anterior['heading'])
            self.t.pencolor(estado_anterior['pencolor'])
            self.t.pensize(estado_anterior['pensize'])
            if estado_anterior['pendown']:
                self.t.pendown()
            else:
                self.t.penup()
            self.t.color(estado_anterior['color'][0], estado_anterior['color'][1])
        else:
            messagebox.showinfo("Aviso", "Não há movimentos para desfazer.")

    def mover_frente(self):
        self.salvar_estado()
        self.t.forward(20)

    def mover_tras(self):
        self.salvar_estado()
        self.t.backward(20)

    def girar_esquerda(self):
        self.salvar_estado()
        self.t.left(15)

    def girar_direita(self):
        self.salvar_estado()
        self.t.right(15)

    def aplicar_movimento(self):
        try:
            self.salvar_estado()
            angulo = (90 - float(self.angulo_spin.get())) % 360
            distancia = float(self.distancia_spin.get())
            self.t.setheading(angulo)
            self.t.forward(distancia)
            self.t.pensize(int(self.espessura_spin.get()))
        except ValueError:
            messagebox.showerror("Erro", "Valores inválidos!")

    def limpar_tela(self):
        self.t.clear()
        self.t.penup()
        self.t.home()
        self.t.pendown()
        self.history.clear()

    def desenhar_forma_automatica(self):
        self.salvar_estado()
        formas = ["quadrado", "triangulo", "circulo", "estrela"]
        forma = random.choice(formas)
        
        self.t.penup()
        self.t.goto(random.randint(-300, 300), random.randint(-200, 200))
        self.t.pendown()
        
        if forma == "quadrado":
            for _ in range(4): self.t.forward(50); self.t.right(90)
        elif forma == "triangulo":
            for _ in range(3): self.t.forward(60); self.t.left(120)
        elif forma == "circulo":
            self.t.circle(30)
        elif forma == "estrela":
            for _ in range(5): self.t.forward(50); self.t.right(144)
        
        messagebox.showinfo("Forma Desenhada", f"Desenhei um {forma}!")

    def mostrar_ajuda(self):
        ajuda = """
        CONTROLES:
        W - Mover para frente
        S - Mover para trás
        A - Girar esquerda
        D - Girar direita
        C - Limpar tela
        F - Desenhar forma aleatória
        """
        messagebox.showinfo("Ajuda", ajuda)

if __name__ == "__main__":
    TurtleGame()