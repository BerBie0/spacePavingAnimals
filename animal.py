import copy
import time

VOISINS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

arche_vide = [
    ["C", "o", "o", "o", "o", "o", "o", "o", "D"],
    ["o", "o", ".", ".", ".", ".", ".", "o", "o"],
    ["o", ".", ".", ".", ".", ".", ".", ".", "o"],
    ["o", ".", ".", ".", ".", ".", ".", ".", "o"],
    ["o", "o", ".", ".", ".", ".", ".", "o", "o"],
    ["A", "o", "o", "o", "o", "o", "o", "o", "B"],
]

lion1 = ("l", 1, [(0, 0), (1, 0)])
lion2 = ("L", 2, [(0, 0), (0, 1), (1, 1)])

girafe1 = ("g", 1, [(0, 0), (1, 0), (1, 1)])
girafe2 = ("G", 2, [(0, 0), (0, 1)])

hipo1 = ("h", 1, [(0, 0), (1, 0)])
hipo2 = ("H", 2, [(0, 0), (1, 0), (2, 0)])

zebre1 = ("z", 1, [(0, 0), (1, 0)])
zebre2 = ("Z", 2, [(0, 0), (0, 1)])

elep1 = ("e", 1, [(0, 0), (1, 0)])
elep2 = ("E", 2, [(0, 0), (1, 0), (0, 1)])

COUPLES = [
    (lion1, lion2),
    (girafe1, girafe2),
    (hipo1, hipo2),
    (zebre1, zebre2),
    (elep1, elep2),
]

liste_animaux = [
    lion1,
    lion2,
    hipo1,
    hipo2,
    zebre1,
    zebre2,
    girafe1,
    girafe2,
    elep1,
    elep2,
]

# installation_1 = [
#     (lion1, (2, 4)),
#     (lion2, (4, 3)),
#     (girafe1, (6, 2)),
#     (girafe2, (6, 3)),
#     (zebre1, (3, 2)),
#     (zebre2, (5, 2)),
#     (elep1, (2, 3)),
#     (elep2, (1, 2)),
#     (hipo1, (2, 1)),
#     (hipo2, (4, 1)),
# ]

grilles_de_depart = [
    [],
    [(hipo2, (2, 1)), (zebre2, (5, 3))],
    [(lion2, (4, 1))],
    [(hipo2, (5, 3))],
    [(hipo1, (2, 3))],
    [(elep1, (3, 1))],
    [(elep1, (4, 3))],
    [(zebre2, (1, 2)), (hipo1, (5, 1))],
    [(lion1, (2, 4)), (girafe2, (4, 1))],
    [(hipo2, (4, 4))],  # 8 solutions
    [(lion1, (2, 1)), (lion2, (5, 3))],  # 0 solutions
]


def affiche_grille(grille):
    """
        affiche l'arche
        :param grille: Une arche
    """
    for ligne in reversed(grille):
        print(*ligne, sep="")
    print()


def copie_grille(grille):
    """
       Renvoie une copie de la grille
       :param grille: Une arche
    """
    return copy.deepcopy(grille)


def position_animal_arche(position, animal):
    """
        Renvoie la liste des positions de l'animal
        :param position: la position du point (0, 0) de l'animal
        :param animal: un animal
    """
    x, y = position
    return [(x + ax, y + ay) for ax, ay in animal[2]]


def place_libre(position, grille, animal):
    """
        Détermine si un emplacement est libre pour un animal
        :param position: la position de l'emplacement
        :param grille: une arche
        :param animal: un animal
        sortie : un booléen
    """
    for x, y in position_animal_arche(position, animal):
        # on peut se passer des tests d'inclusions grâce aux bords de la grille
        if not (0 <= x <= 9) or not (0 <= y <= 6) or grille[y][x] != ".":
            return False
    return True


def installe_animal(position, grille, animal):
    """
        Modifie une arche en y installant un animal
        :param position: l'endroit ou l'on place l'animal
        :param grille: une arche
        :param animal: un animal
    """
    for x, y in position_animal_arche(position, animal):
        grille[y][x] = animal[0]


def enleve_animal(position, grille, animal):
    """
        Modifie une arche en y retirant un animal
        :param position: position de l'animal à retirer
        :param grille: une arche
        :param animal: un animal
    """
    for x, y in position_animal_arche(position, animal):
        grille[y][x] = "."


def installe_installation(grille, installation):
    """
        Modifie une arche en installant plusieurs animaux
        :param grille: une arche
        :param installation: une liste de tuples (animal, position)
        sortie : True si l'installation a réussi, False sinon
    """
    for animal, position in installation:
        if not place_libre(position, grille, animal):
            return False
        installe_animal(position, grille, animal)
    return True


def sont_voisins(a1, p1, a2, p2):
    """
        Détermine si deux animaux sont voisins
        :param a1: le premier animal
        :param p2: la position du premier animal
        :param a2: le deuxième animal
        :param p2: la position du deuxième animal
        sortie : un booléen
    """
    for x1, y1 in position_animal_arche(p1, a1):
        for x2, y2 in position_animal_arche(p2, a2):
            # deux cases voisines suffisent
            if any((x1 + a, y1 + b) == (x2, y2) for a, b in VOISINS):
                return True
    return False


def position_animal_dans_installation(animal, installation):
    """
        Cherche un animal dans une installation et renvoie sa position
        :param animal: un animal
        :param installation: une liste de tuples (animal, position)
        sortie : la position ou False si l'animal n'est pas dans l'installation
    """
    for inst in installation:
        if inst[0][0] == animal[0]:
            return inst[1]
    return False


def verifie_animaux_voisins_dans_installation(installation):
    """
        Vérifie si tous les couples d'une installation sont voisins
        Les couples qui ne sont pas au complet sont ignorés
        :param installation: une liste de tuples (animal, position)
        sortie : booléen
    """
    for a1, a2 in COUPLES:
        p1 = position_animal_dans_installation(a1, installation)
        p2 = position_animal_dans_installation(a2, installation)
        if p1 and p2 and not sont_voisins(a1, p1, a2, p2):
            return False
    return True


def points_libres(grille):
    """
        renvoie les positions libres d'une arche
        :param grille: une arche
    """
    for x in range(9):
        for y in range(6):
            if grille[y][x] == ".":
                yield x, y


def _solve(grille, installation, animaux):
    # cette fonction est un générateur, ainsi on peut
    # facilement choisir de s'arrêter à la nème solution
    if not animaux:
        yield installation
        return
    # on place le premier animal de la liste
    a = animaux[0]
    # inutile de parcourir les bordures
    for x in range(1, 8):
        for y in range(1, 5):
            # ce test permet de gagner un peu de performance
            if grille[y][x] != ".":
                continue
            if place_libre((x, y), grille, a):
                nouvelle_inst = installation + [(a, (x, y))]
                if not verifie_animaux_voisins_dans_installation(nouvelle_inst):
                    continue
                installe_animal((x, y), grille, a)
                yield from _solve(grille, nouvelle_inst, animaux[1:])
                enleve_animal((x, y), grille, a)


def solve(installation, nombre_de_solutions=1):
    """
        renvoie une liste de solutions selon une installation de départ
        :param installation: une liste de tuples (animal, position)
        :param nombre_de_solutions: un entier représentant le nombre
                                    maximal de solutions voulues
        sortie : une liste d'installations
    """
    grille = copie_grille(arche_vide)
    animaux_presents = [inst[0] for inst in installation]
    animaux_absents = [a for a in liste_animaux if a not in animaux_presents]
    installe_installation(grille, installation)
    gen = _solve(grille, installation, animaux_absents)
    res = []
    # on récupère le nombre de solutions choisi
    for _ in range(nombre_de_solutions):
        try:
            solution = next(gen)
            res.append(solution)
        except StopIteration:
            # s'il n'y a pas assez de solutions, on s'arrête
            break
    return res


if __name__ == "__main__":

    for i, inst in enumerate(grilles_de_depart, 1):
        print(i, ":", inst)

    print()

    while True:
        try:
            rep = input("Choisissez une installation de départ : ")
            rep = int(rep)
            if not (1 <= rep <= len(grilles_de_depart)):
                raise ValueError()
            inst = grilles_de_depart[rep - 1]
        except ValueError:
            print("Réponse invalide")
        else:
            break

    t = time.perf_counter()
    solutions = solve(inst, 100)  # on peut changer le nombre si on veut moins de solutions
    t = time.perf_counter() - t

    if not solutions:
        print("Pas de solutions")

    for i, solution in enumerate(solutions, 1):
        print("Solution n°", i)
        temp_grille = copie_grille(arche_vide)
        installe_installation(temp_grille, solution)
        affiche_grille(temp_grille)

    print("Calculé en", t, "secondes")
