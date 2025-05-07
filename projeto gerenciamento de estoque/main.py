import tkinter as tk
import ui
from database import inicializar_banco

if __name__ == "__main__":
    inicializar_banco()
    root = tk.Tk()
    app = ui.AplicacaoEstoque(root)
    root.mainloop()