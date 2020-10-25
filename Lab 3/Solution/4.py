import sys
import os
import random

def gra(rounds):
    gameRounds = komputerPoint = playerPoint = komputerPointLose = playerPointLose = remis = 0
    while(gameRounds < rounds):
        print("\nRound : ", gameRounds + 1)
        valPlayer = input("Wprowadz (1 - papier, 2 - kamień, 3 - nożyce): ")
        valPlayer = int(valPlayer)
        valKomp = random.randint(1,3)
        print("Twój wybór - ", printWord(valPlayer))
        print("Wybór komputera - ", printWord(valKomp))
        
        if(valPlayer == 1 and valKomp == 2 or valPlayer == 2 and valKomp == 3 or valPlayer == 3 and valKomp == 1):
            playerPoint += 1
            komputerPointLose += 1
        elif(valKomp == 1 and valPlayer == 2 or valKomp == 2 and valPlayer == 3 or valKomp == 3 and valPlayer == 1):
            komputerPoint += 1
            playerPointLose += 1
        else:
            print("powtórka")
            gameRounds -= 1
            remis += 1
        gameRounds += 1
    printResult(komputerPoint, komputerPointLose, playerPoint, playerPointLose, remis)

def printWord(k):
     return {
        1: 'papier',
        2: 'kamień',
        3: 'nożyce',
    }[k]

def printResult(kPoint, kLose, pPoint, pLose, pR):
    print("\nGra zakonczona")
    if(kPoint < pPoint):
        print("Player wygrywa | player win - ", pPoint, " | player lose - ", pLose, " | player remis - ", pR)
    elif(kPoint == pPoint):
        print("Remis | player score - ", pPoint, " | kompuer score - ", kPoint)
    else:
        print("Komputer wygrywa | komputer win - ", kPoint, " | komputer lose - ", kLose, " | komputer remis - ", pR)

if __name__ == "__main__":
    acts = input("Wprowadz liczbę rund: ")
    acts = int(acts)
    gra(acts)