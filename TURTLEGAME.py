import turtle
import tkinter as tk
from tkinter import ttk, messagebox
import random
import math

class TurtleGame:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Aventura da Tartaruga - Lince Games")
        self.janela.configure(bg="#E6F7FF")
        self.janela.geometry("1200x700")
        
        self.cores = {
            "fundo": "#E6F7FF",
            "destaque": "#FF6B35",
            "texto": "#2A5C7A",
            "botao": "#4CAF50",
            "borda": "#B0E0E6"
        }
        
        self.fontes = {
            "titulo": ("Verdana", 20, "bold"),
            "subtitulo": ("Verdana", 14, "bold"),
            "texto": ("Verdana", 12),
            "botao": ("Verdana", 12, "bold")
        }
        
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
        self.t.color("#4CAF50")
        self.t.speed(5)
        self.t.pensize(3)

    def criar_interface(self):
        controles_frame = tk.Frame(self.janela, bg=self.cores["fundo"], bd=2, relief=tk.RIDGE)
        controles_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.criar_titulo(controles_frame)
        self.criar_secao_movimento(controles_frame)
        self.criar_secao_aparencia(controles_frame)
        self.criar_secao_caneta(controles_frame)
        self.criar_secao_acoes(controles_frame)
        self.criar_secao_dicas(controles_frame)
        
        self.janela.grid_columnconfigure(0, weight=0)
        self.janela.grid_columnconfigure(1, weight=1)
        self.janela.grid_rowconfigure(0, weight=1)

    def criar_titulo(self, parent):
        titulo_frame = tk.Frame(parent, bg=self.cores["fundo"])
        titulo_frame.pack(pady=10, fill=tk.X)
        
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
            padx=10,
            pady=10
        )
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Controles de ângulo e distância
        tk.Label(frame, text="Ângulo (0-360°):", bg=self.cores["fundo"], font=self.fontes["texto"]).grid(row=0, column=0, sticky="w", pady=5)
        self.angulo_spin = ttk.Spinbox(frame, from_=0, to=360, width=5, font=self.fontes["texto"])
        self.angulo_spin.grid(row=0, column=1, pady=5)
        self.angulo_spin.set(0)
        
        tk.Label(frame, text="Distância:", bg=self.cores["fundo"], font=self.fontes["texto"]).grid(row=1, column=0, sticky="w", pady=5)
        self.distancia_spin = ttk.Spinbox(frame, from_=1, to=100, width=5, font=self.fontes["texto"])
        self.distancia_spin.grid(row=1, column=1, pady=5)
        self.distancia_spin.set(20)
        
        ttk.Button(frame, text="MOVER", command=self.aplicar_movimento).grid(row=2, columnspan=2, pady=10)

    def criar_secao_aparencia(self, parent):
        frame = tk.LabelFrame(
            parent,
            text=" Aparência da Tartaruga ",
            bg=self.cores["fundo"],
            fg=self.cores["texto"],
            font=self.fontes["subtitulo"],
            padx=10,
            pady=10
        )
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Cores da tartaruga
        tk.Label(frame, text="Cor:", bg=self.cores["fundo"], font=self.fontes["texto"]).grid(row=0, column=0, sticky="w")
        cores_frame = tk.Frame(frame, bg=self.cores["fundo"])
        cores_frame.grid(row=0, column=1, columnspan=2)
        
        cores = ["#FF5733", "#4CAF50", "#3498DB", "#9B59B6", "#F1C40F"]
        for cor in cores:
            btn = tk.Button(cores_frame, bg=cor, width=3, command=lambda c=cor: self.t.color(c))
            btn.pack(side=tk.LEFT, padx=2)
        
        # Velocidade
        tk.Label(frame, text="Velocidade:", bg=self.cores["fundo"], font=self.fontes["texto"]).grid(row=1, column=0, sticky="w", pady=5)
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
            padx=10,
            pady=10
        )
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Espessura
        tk.Label(frame, text="Espessura:", bg=self.cores["fundo"], font=self.fontes["texto"]).grid(row=0, column=0, sticky="w")
        self.espessura_spin = ttk.Spinbox(frame, from_=1, to=10, width=3, font=self.fontes["texto"])
        self.espessura_spin.grid(row=0, column=1, padx=5)
        self.espessura_spin.set(3)
        
        # Cores da linha
        tk.Label(frame, text="Cor da Linha:", bg=self.cores["fundo"], font=self.fontes["texto"]).grid(row=1, column=0, sticky="w", pady=5)
        cores_frame = tk.Frame(frame, bg=self.cores["fundo"])
        cores_frame.grid(row=1, column=1, columnspan=2)
        
        cores = ["#000000", "#FF0000", "#00FF00", "#0000FF", "#FF00FF"]
        for cor in cores:
            btn = tk.Button(cores_frame, bg=cor, width=3, command=lambda c=cor: self.t.pencolor(c))
            btn.pack(side=tk.LEFT, padx=2)

    def criar_secao_acoes(self, parent):
        frame = tk.LabelFrame(
            parent,
            text=" Ações ",
            bg=self.cores["fundo"],
            fg=self.cores["texto"],
            font=self.fontes["subtitulo"],
            padx=10,
            pady=10
        )
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(frame, text="Limpar Tela", command=self.limpar_tela).pack(pady=5)
        ttk.Button(frame, text="Desenhar Forma", command=self.desenhar_forma_automatica).pack(pady=5)
        ttk.Button(frame, text="Ajuda", command=self.mostrar_ajuda).pack(pady=5)

    def criar_secao_dicas(self, parent):
        frame = tk.LabelFrame(
            parent,
            text=" Dicas ",
            bg=self.cores["fundo"],
            fg=self.cores["texto"],
            font=self.fontes["subtitulo"],
            padx=10,
            pady=10
        )
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.label_dica = tk.Label(
            frame,
            text="Use as setas ou teclas W/A/S/D para mover!",
            bg=self.cores["fundo"],
            fg=self.cores["texto"],
            font=self.fontes["texto"],
            wraplength=250
        )
        self.label_dica.pack()

    def configurar_teclado(self):
        self.screen.listen()
        self.screen.onkey(lambda: self.t.forward(20), "w")
        self.screen.onkey(lambda: self.t.backward(20), "s")
        self.screen.onkey(lambda: self.t.left(15), "a")
        self.screen.onkey(lambda: self.t.right(15), "d")
        self.screen.onkey(self.limpar_tela, "c")
        self.screen.onkey(self.desenhar_forma_automatica, "f")

    def aplicar_movimento(self):
        try:
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

    def desenhar_forma_automatica(self):
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