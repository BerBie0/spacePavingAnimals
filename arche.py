import tkinter as tk
from animal import solve, grilles_de_depart


class Arche(tk.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(width=666, height=580, *args, **kwargs)
        self.imgfond = tk.PhotoImage(file="images/arche_vide.PNG").subsample(2)
        self.create_image(0, 580, image=self.imgfond, anchor="sw")
        self.images = {
            "l": tk.PhotoImage(file="images/lion1.PNG").subsample(2),
            "L": tk.PhotoImage(file="images/lion2.PNG").subsample(2),
            "g": tk.PhotoImage(file="images/girafe1.PNG").subsample(2),
            "G": tk.PhotoImage(file="images/girafe2.PNG").subsample(2),
            "z": tk.PhotoImage(file="images/zebre1.PNG").subsample(2),
            "Z": tk.PhotoImage(file="images/zebre2.PNG").subsample(2),
            "h": tk.PhotoImage(file="images/hipo1.PNG").subsample(2),
            "H": tk.PhotoImage(file="images/hipo2.PNG").subsample(2),
            "e": tk.PhotoImage(file="images/elep1.PNG").subsample(2),
            "E": tk.PhotoImage(file="images/elep2.PNG").subsample(2),
        }

    def coordonnees(self, x, y):
        return 2 + x * 75, 598 - y * 98

    def ajouter_animaux(self, installation):
        for animal, (x, y) in installation:
            a, b = self.coordonnees(x, y)
            self.create_image(a, b, image=self.images[animal[0]], anchor="sw", tags="animal")

    def vider(self):
        self.delete("animal")


class Main(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.texte = tk.Label(self, text="Choisissez une position de départ", font=("Courrier", 12))
        self.texte.grid(row=1, column=1, columnspan=11)
        self.btn_gauche = tk.Button(self, text="<", command=self.gauche)
        self.btn_gauche.grid(row=2, column=5)
        self.btn_droite = tk.Button(self, text=">", command=self.droite)
        self.btn_droite.grid(row=2, column=7)
        self.btn_valider = tk.Button(self, text="Valider", command=self.valider)
        self.btn_valider.grid(row=2, column=11)
        self.arche = Arche(self)
        self.arche.grid(row=3, column=1, columnspan=11)
        self.installations = grilles_de_depart
        self.page = 0
        self.texte_page = tk.Label(self, text="")
        self.texte_page.grid(row=2, column=6)
        # mode 1 pour le choix de la grille de départ, mode 2 pour la page des solutions
        self.mode = 1
        self.rafraichir()

    @property
    def pages(self):
        return len(self.installations)

    def gauche(self):
        self.page -= 1
        self.rafraichir()

    def droite(self):
        self.page += 1
        self.rafraichir()

    def rafraichir(self):
        self.arche.vider()
        if self.pages:
            self.page %= self.pages
            self.arche.ajouter_animaux(self.installations[self.page])
        self.texte_page.config(text="%s / %s" % (self.page + 1 if self.pages else 0, self.pages))

    def valider(self):
        if self.mode == 1:
            solutions = solve(self.installations[self.page], 100)
            self.installations = solutions
            self.texte.config(text="Il y a %s solution(s)" % self.pages)
            self.btn_valider.config(text="Revenir")
            self.mode = 2
        else:
            self.texte.config(text="Choisissez une position de départ")
            self.installations = grilles_de_depart
            self.btn_valider.config(text="Valider")
            self.mode = 1
        self.page = 0
        self.rafraichir()


if __name__ == "__main__":
    root = tk.Tk()
    main = Main(root)
    main.pack()
    root.mainloop()
