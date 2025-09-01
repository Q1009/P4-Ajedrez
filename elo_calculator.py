def calculate_elo(elo_player, elo_opponent, k_player, w):
    """
    Calcule le nouvel ELO d'un joueur après une partie.

    elo_player : ELO du joueur
    elo_opponent : ELO de l'adversaire
    k_player : coefficient K du joueur
    w : résultat de la partie (1 = victoire, 0.5 = nul, 0 = défaite)
    """
    expected_score = 1 / (1 + 10 ** (-(elo_player - elo_opponent) / 400))
    print(expected_score)# DEBUG
    elo_updated = elo_player + k_player * (w - expected_score)

    return round(elo_updated)

def main():
    # Exemple d'utilisation
    new_elo = calculate_elo(elo_player=2005, elo_opponent=0, k_player=20, w=1)
    print(f"Nouveau ELO : {new_elo}")

if __name__ == "__main__":
    main()


"""
on détermine un coefficient 
K qui vaudra : 

K = 40 jusqu’à la 30e partie du joueur, sinon,
K = 20 pour un classement Elo en dessous de 2 400 Elo, sinon,
K = 10 pour un classement Elo au-dessus de 2 400.

"""