# tkinter_app_27Nov2010.py
from tkinter import *
import time
# mise a jour bout à bout Movetion/vitesse/END/DFA dernier objet to premier
#  1 m = 10 px
WIDTH = 1010            # OF SCREEN IN PIXELS
HEIGHT = 500            # OF SCREEN IN PIXELS
BALLS = 1               # Nombre de véhicules lors de l'animation
WALL = 5                # FROM SIDE IN PIXELS
DFM = 500               # Distance Feu/Mur
#WALL_FORCE = 400        # ACCELERATION PER MOVE
#SPEED_LIMIT = 30        # FOR ball VELOCITY
StartSPEED = 0              # m  / s : vitesse de départ
ACCELERATION = 1.39     # m / s²
#DECELERATION = 0
BALL_RADIUS = 10        # FOR ballS IN PIXELS
SPEED_LIMIT = 40         # km / h
#OFFSET_START = 20       # FROM WALL IN PIXELS
#FRAMES_PER_SEC = 40     # SCREEN UPDATE RATE
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
    global flag, i, BALLS

    if i[3] == False :
        if FRouge == True and i[1] < WIDTH-DFM: # si le feu est rouge et que le vehicule ne l'a pas dépassé
            i[5] = (WIDTH-DFM - BALL_RADIUS-i[1])/10 # La distance avant arret est celle du véhicule au feu
        else:
            i[5] = (WIDTH-BALL_RADIUS-i[1])/10 #  La distance avant arret est celle du véhicule au mur

        if i[2] != 0:                # si le demarrage ne se fait pas à vitesse nulle SPEED != 0

            print ("Vitesse Vehicule"," ", i[2]*3.6)

            #if Distance Avant Arret > distance de freinage + Distance de sécurité:
            if i[5] > (((i[2])**2)/(2*FRICTION*9.81))+BALL_RADIUS/10 and i[4] == False: # DAA > Distance Freinage requise et DFA == False
                accelerate() # Accélérer

            elif i[5] <= (((i[2])**2)/(2*FRICTION*9.81))+BALL_RADIUS/10: # sinon on freine
                decelerate() # Décélérer

            else: #si le feu repasse au vert
                accelerate()

        else: accelerate()

        if i[5]>0 and i[2] > 0: # si la voiture n'a pas atteint le mur ou le feu et n'est pas arretée
            i[1]+=i[2]/5 # Position = SPEED/5 (On bouge le véhicule en fonction de sa vitesse calculée plus haut)
        else:
            i[2] = StartSPEED # Reinitialisation de la vitesse
            i[4] = False
            if i[5] == (WIDTH-BALL_RADIUS-i[1])/10 : # si la voiture a atteint le mur
                i[3] = True #END = True
                stop_it() # stoppe l'animation


    if flag >0: # Si l'animation n'a pas été mise en pause
        myCan.coords(i[0], i[1]-BALL_RADIUS, HEIGHT/2-BALL_RADIUS, i[1]+BALL_RADIUS, HEIGHT/2+BALL_RADIUS)
        root.after(20,moveCircle) # répetition de la boule si le critere d'arret est bon

def accelerate():
    global i
    i[4] = False # on réentame un accélération donc on va rénitialiser la decel pour la prochaine
    if i[2] + ACCELERATION*0.02 <= SPEED_LIMIT/3.6 : # si le véhicule ne va pas dépasser la limite de vitesse (km/h vers m/s: /3.6)
        i[2] += ACCELERATION*0.02 # la boucle s'actualise toute les 20 ms d'où le *0.02
    elif i[2] > SPEED_LIMIT/3.6:                     # si le véhicule a dépassé la vitesse limite il freine
        i[2] -= ACCELERATION*0.02
                                                              # sinon il maintient sa vitesse

def decelerate():
    global i
    if i[4] == False: #Pour n'affecter a Decceleration une valeur une seule fois
        i[6] = (i[2]*i[2])/(2*(i[5]))        # Vitesse de déceleration = v²/2x
        print ("Decel ", i[6])
        i[4] = True
        i[2] -= i[6]*0.02
    else:
        i[2] -= i[6]*0.02

# Véhicule i = (objet, Position, speed, End: Move: Le véhicule a atteint le mur ?, DFA, DAA, Vitesse de Deceleration)

######################################################
#Fonctions pour l'interface
#####################################################

def start_it():
    global flag, i
    "démarrage de l'animation"
    if i[3] == True: # END == True
        i[1] = 0     # Postion = 0
    if flag == 0:       # pour ne lancer qu'une seule boucle
        flag =1
        i[3] = False # END = False
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
        if i[3] == False: # si le vehicule n'est pas arreté au mur de fin
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


def majBalls(nouvelleValeur):
    global BALLS
    # nouvelle valeur en argument
    BALLS = int(nouvelleValeur)


root = Tk()
root.title("Véhicule Curseurs")

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
i= [myCan.create_oval(BALL_RADIUS, HEIGHT/2-BALL_RADIUS, BALL_RADIUS, HEIGHT/2+BALL_RADIUS, fill = "blue"),0,StartSPEED,False,False,WIDTH-BALL_RADIUS, 0]
print(myCan.create_oval(BALL_RADIUS, HEIGHT/2-BALL_RADIUS, BALL_RADIUS, HEIGHT/2+BALL_RADIUS, fill = "blue"))
# Véhicule i = (objet, Position, speed, End: Move: Le véhicule a atteint le mur ?, DFA: Move: Le véhicule a atteint la distance de freinage ?,
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