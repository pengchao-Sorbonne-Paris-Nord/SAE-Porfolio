#!/usr/bin/python3
#Fayssal Benkhaldoun le 25/09/2022

import numpy as np  ; import matplotlib.pyplot as plt ; import math ; import time

T=0.25              #on a défini une valeur t=0.25
Omega=2*math.pi/T   #on a défini la valeur de omega pour le code

nend=10 #on déclare une variable

# spatial domain
xleft = -2*T ; xright = 2*T   # on a défini les valeurs de x positive et négative

# num of grid points  ; # x grid of n points # Time step 
m = 101  ; x, dx = np.linspace(xleft,xright,m,retstep=True)  ; #on a défini une valeur m= 101 , pui on a fait l'opération des points


fig, axs = plt.subplots(2, 2) # On a défini les axes de 2 à 2 
def plotsol(NN,YC,Uo):
    axs[0, 0].plot(x, Uo, color='red',marker=".")   #on défini l'axe de 0,0 pour x, Uo pour une couleur rouge avec la marque .
    axs[0, 0].set_title("Fig. 1") #on donne le nom comme la figure 1
    axs[1, 0].plot(NN, YC, color='white', marker="o",markeredgecolor='green') #on défini l'axe de 1,0 pour NN,YC avec la couleur blanc et vert pour la marque
    axs[1, 0].set_title("Fig. 2") #on donne le nom comme la figure 2
    axs[0, 1].plot(x, Uo, color='black',marker="+") #on défini l'axe de 0,1 pour x,Uo avec la couleur noir avec la marque +
    axs[0, 1].set_title("Fig. 3") #on donne le nom comme la figure 3
    axs[1, 1].plot(x, Uo, color='cyan',marker="x")  #on défini l'axe de 1,1 pour x,Uo avec la couleur cyan avec la marque x
    axs[1, 1].set_title("Fig. 4") #on donne le nom comme la figure 4

    

YC= [(4/math.pi)] #on défini la valeur YC d'ou math est une valeur de float
NN= [1] #on défini la valeur de NN en 1

Uo = (4/math.pi)*np.sin(Omega*x) #On défini la valeur ded Uo
plotsol(NN,YC,Uo) #on défini une séquence de valeur
plt.show() #on veut imprimer le résultat
time.sleep(0.1) #on lui donne un temps


n=2 #on défini la valeur de n
while n <= nend: #on dit que si n est plus petit ou égal à nend(10)
    fig, axs = plt.subplots(2, 2) #on construit une figgure de 2,2
    Uo=Uo+(4/math.pi)*(1/n)*np.sin(n*Omega*x) #on défini la nouvelle valeur de Uo
    modharm=(4/math.pi)*(1/n) #on déclare une variable
    YC.append(modharm) #on ajoute l'élément modharm pour YC
    NN.append(n); #on ajoute l'élément n pour NN
    plotsol(NN,YC,Uo)#on défini une séquence de valeur pour NN,YX,Uo
    plt.show()#on imprime le résultat
    time.sleep(0.1)#on donne une intervalle de temps
    n=n+1#on donne la valeur n avec n=n+1
    

print(quit) #on imprime les résultats
quit()


    




