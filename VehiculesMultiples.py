# tkinter_app_27Nov2010.py
from tkinter import *
import time
# mise a jour bout à bout Movetion/vitesse/END/DFA dernier objet to premier
#  1 m = 10 px
WIDTH = 1010            # OF SCREEN IN PIXELS
HEIGHT = 500            # OF SCREEN IN PIXELS
BALLS = 3               # Nombre de véhicules lors de l'animation
WALL = 5                # FROM SIDE IN PIXELS
Colors = ["Blue","Orange","Yellow","Brown","Green"] # On introduit un tableau avec les différentes couleurs des véhicules
DFM = 500               # Distance Feu/Mur
#WALL_FORCE = 400        # ACCELERATION PER MOVE
StartSPEED = 0              # m  / s : vitesse de départ
ACCELERATION = 1.39     # m / s²
#DECELERATION = 0
BALL_RADIUS = 10        # FOR ballS IN PIXELS
SPEED_LIMIT = 40         # km / h
#OFFSET_START = 20       # FROM WALL IN PIXELS
FRAMES_PER_SEC = 50     # SCREEN UPDATE RATE
FRICTION = 0.8          # Coefficient cinétique de friction
MASS = 1500             # Kg Poids du vehicule
flag = 0                # critère d'arret
#DFA = False   Move: distance de freinage atteinte ?
FRouge = False               # Move: feu rouge ?
#DAA = 0
j = 0                   # indice de la balle en mouvement


# Véhicule i = (objet, Position, speed, End: Move: Le véhicule a atteint le mur ?, DFA, DAA, Vitesse de Deceleration)


########################################################
#Fontions pour le code
#######################################################

def moveCircle():
    global flag, j, i, BALLS

    if i[j][3] == False :
        if FRouge == True and i[j][1] < WIDTH-DFM : # si le feu est rouge et que le vehicule ne l'a pas dépassé
            if i[j-1][1] > WIDTH-DFM or j == 0 :
                i[j][5] = (WIDTH-DFM - BALL_RADIUS-i[j][1])/10 # La distance avant arret est celle du véhicule au feu
            else: # si le véhicule n'est pas premier
                i[j][5] = (i[j-1][1] -i[j][1] - BALL_RADIUS*2)/10 #  La distance avant arret est celle du véhicule au véhicule de devant
        elif j != 0: #  si le véhicule n'est pas premier
            i[j][5] = (i[j-1][1] -i[j][1] - BALL_RADIUS*2)/10 #  La distance avant arret est celle du véhicule au véhicule de devant
        else:
            i[j][5] = (WIDTH-BALL_RADIUS-i[j][1])/10 #  La distance avant arret est celle du véhicule au mur

        if i[j][2] != 0:                # si le demarrage ne se fait pas à vitesse nulle SPEED != 0

            print ("Vitesse Vehicule",j+1," ", i[j][2]*3.6)

            #if Distance Avant Arret > distance de freinage + Distance de sécurité:
            if i[j][5] > (((i[j][2])**2)/(2*FRICTION*9.81))+BALL_RADIUS/10 and i[j][4] == False: # DAA > Distance Freinage requise et DFA == False
                accelerate() # Accélérer

            elif i[j][5] <= (((i[j][2])**2)/(2*FRICTION*9.81))+BALL_RADIUS/10: # sinon on freine
                decelerate() # Décélérer

            else: #si le feu repasse au vert
                accelerate()

        else: accelerate()

        if i[j][5]>0 and i[j][2] > 0: # si la voiture n'a pas atteint le mur ou le feu et n'est pas arretée
            i[j][1]+=i[j][2]/5 # Position = SPEED/5 (On bouge le véhicule en fonction de sa vitesse calculée plus haut)
        else:
            i[j][2] = StartSPEED # Reinitialisation de la vitesse
            i[j][4] = False
            if i[j][1] >= WIDTH-BALL_RADIUS- j*(BALL_RADIUS*2 + BALL_RADIUS/10 ) - 10: # si la voiture a atteint le mur
                i[j][3] = True #END = True
                print("############ ENDED Véhicule ",j," ############")
                if j == BALLS - 1: # SI le dernier vehicule a atteint le mur
                    stop_it()      # Mettre en pause

    if flag >0: # Si l'animation n'a pas été mise en pause
        myCan.coords(i[j][0], i[j][1]-BALL_RADIUS, HEIGHT/2-BALL_RADIUS, i[j][1]+BALL_RADIUS, HEIGHT/2+BALL_RADIUS)
        changeCircle() # permet de passer au véhicule suivant
        root.after(int(1000/(FRAMES_PER_SEC*BALLS)),moveCircle) # répetition de la boule si le critere d'arret est bon

def accelerate():
    global i
    i[j][4] = False # on réentame un accélération donc on va rénitialiser la decel pour la prochaine
    if i[j][2] + ACCELERATION*1/FRAMES_PER_SEC <= SPEED_LIMIT/3.6 : # si le véhicule ne va pas dépasser la limite de vitesse (km/h vers m/s: /3.6)
        i[j][2] += ACCELERATION*1/FRAMES_PER_SEC # la boucle s'actualise toute les 1000/FRAMES_PER_SEC ms d'ou le * 1/FRAMES_PER_SEC
    elif i[j][2] > SPEED_LIMIT/3.6:                     # si le véhicule a dépassé la vitesse limite il freine
        i[j][2] -= ACCELERATION*1/FRAMES_PER_SEC
                                                              # sinon il maintient sa vitesse

def decelerate():
    global i
    if i[j][4] == False: #Pour n'affecter a Decceleration une valeur une seule fois
        i[j][6] = (i[j][2]*i[j][2])/(2*(i[j][5]))        # Vitesse de déceleration = v²/2x
        print ("Decel ", i[j][6])
        i[j][4] = True
        i[j][2] -= i[j][6]*1/FRAMES_PER_SEC
    else:
        i[j][2] -= i[j][6]*1/FRAMES_PER_SEC

def changeCircle():
    global j, i, TabMove
    if j == BALLS- 1: # Si on était en train de faire bouger le dernier véhicule
        j = 0     # On retourne au premier
    else: j += 1 # Sinon on passe au suivant


# Véhicule i = (objet, Position, speed, End: Move: Le véhicule a atteint le mur ?, DFA, DAA, Vitesse de Deceleration)

######################################################
#Fonctions pour l'interface
#####################################################

def start_it():
    global flag, i, j
    "démarrage de l'animation"
    for k in range(BALLS):
        if i[k][3] == True and flag == 0: # END == True et l'animation en pause
            i[k][1] = 0+(BALLS-1-k)*(BALL_RADIUS*2+BALL_RADIUS/10)     # Postion = 0
            i[k][3] = False # END = False
    if flag == 0:       # pour ne lancer qu'une seule boucle
        flag =1
        moveCircle()

def stop_it():
    "arret de l'animation"
    global flag, i
    flag =0

def change_feu():
    global FRouge, i, flag
    if FRouge == False:
        myCan.itemconfigure(f, fill = "red")
        FRouge = True
    else:
        myCan.itemconfigure(f, fill = "green")
        FRouge = False
        if i[j][3] == False: # si le vehicule n'est pas arreté au mur de fin
            start_it()

def majAcc(nouvelleValeur):
    global ACCELERATION
    # nouvelle valeur en argument
    ACCELERATION = float(nouvelleValeur)
    print ("Acceleration ", ACCELERATION)

def majSpeedL(nouvelleValeur):
    global SPEED_LIMIT
    # nouvelle valeur en argument
    SPEED_LIMIT = float(nouvelleValeur)
    print ("Vitesse Limit ", SPEED_LIMIT)

def majFPS(nouvelleValeur):
    global FRAMES_PER_SEC
    # nouvelle valeur en argument
    if flag == 0: # Pour ne pas changer les FPS pendant l'animation
        FRAMES_PER_SEC = float(nouvelleValeur)
    print ("FPS ", FRAMES_PER_SEC)

def majBalls(nouvelleValeur):
    global BALLS
    # nouvelle valeur en argument
    BALLS = int(nouvelleValeur)


root = Tk()
root.title("Véhicules Multiples")

#uiFrame = Frame(myCan,width=1000,height=500)
#uiFrame.configure(background='#e0e0e0')
#uiFrame.grid(row=0,column=0,sticky=N+S)

#outputFrame = Frame(self,width=1000,height=500,background='#C0C0C0')
#outputFrame.grid(row=0,column=1)

myCan = Canvas(root,width=WIDTH,height=HEIGHT,borderwidth=1,relief='sunken')
myCan.pack(side=RIGHT, padx =5, pady =5)
myCan.create_line(0,HEIGHT/2-BALL_RADIUS-WALL,WIDTH,HEIGHT/2-BALL_RADIUS-WALL, width=3)
myCan.create_line(0,HEIGHT/2+BALL_RADIUS+WALL,WIDTH,HEIGHT/2+BALL_RADIUS+WALL, width=3)
myCan.create_line(WIDTH,HEIGHT-300,WIDTH,HEIGHT-200, width=5, fill="red")
f = myCan.create_line(WIDTH-DFM,HEIGHT-280,WIDTH-DFM,HEIGHT-220, width=5, fill="green")
i = list(range(BALLS))
for k in range(BALLS): # on crée une liste qui contient tous les véhicules
    i[BALLS-1 - k]= [myCan.create_oval(BALL_RADIUS, HEIGHT/2-BALL_RADIUS, BALL_RADIUS, HEIGHT/2+BALL_RADIUS,fill = Colors[k])
        ,0+k*(BALL_RADIUS*2+BALL_RADIUS/10),StartSPEED,False,False,WIDTH-BALL_RADIUS, 0]
# Véhicule i = (objet, Position, speed, End: Move: Le véhicule a atteint le mur ?,
# DFA: Move: Le véhicule a atteint la distance de freinage ?,
# DAA: Distance avant que le vehicule doive s'arrêter, Vitesse de decelération)

# Création d'un widget Scale
Acc = StringVar()
Acc.set(ACCELERATION)
echelle = Scale(root,from_=0,to=3,resolution=0.01,orient=HORIZONTAL,length=200,width=20,label="Acceleration (m.s²)",tickinterval=0.5,variable=Acc,command=majAcc)
echelle.pack(padx=1,pady=1)

SpeedL = StringVar()
SpeedL.set(SPEED_LIMIT)
echelle = Scale(root,from_=20,to=40,resolution=1,orient=HORIZONTAL,length=200,width=20,label="Limite de vitesse (km/h)",tickinterval=5,variable=SpeedL,command=majSpeedL)
echelle.pack(padx=1,pady=1)


""""" à débuger
Fps = StringVar()
Fps.set(FRAMES_PER_SEC)
echelle = Scale(root,from_=40,to=100,resolution=1,orient=HORIZONTAL,length=200,width=20,
                label="Frame Per Second",tickinterval=10,variable=Fps,command=majFPS)
echelle.pack(padx=1,pady=1)


Balls = StringVar()
Balls.set(BALLS)
echelle = Scale(root,from_=1,to=2,resolution=1,orient=HORIZONTAL,length=200,width=20,label="Nombre de Véhicules",tickinterval=1,variable=Balls,command=majBalls)
echelle.pack(padx=1,pady=1)
"""""

newBtn1 = Button(root,text="GO",command=start_it)
newBtn1.pack()

newBtn2 = Button(root, text='Pause', command=stop_it)
newBtn2.pack()

newBtn3 = Button(root, text='Feu', command=change_feu)
newBtn3.pack()

newBtn4 = Button(root, text='Quit', command=root.quit)
newBtn4.pack()

root.mainloop()