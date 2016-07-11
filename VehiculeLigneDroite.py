# tkinter_app_27Nov2010.py
from tkinter import *
import time

# 1 m = 10 px
WIDTH = 1010            # OF SCREEN IN PIXELS
HEIGHT = 500            # OF SCREEN IN PIXELS
BALLS = 1               # IN SIMULATION
WALL = 5                # FROM SIDE IN PIXELS
#WALL_FORCE = 400        # ACCELERATION PER MOVE
#SPEED_LIMIT = 30        # FOR ball VELOCITY
SPEED = 1              # m  / s : vitesse de départ
StartSPEED = SPEED
ACCELERATION = 1.39     # m / s²
DECELERATION = 0
BALL_RADIUS = 10        # FOR ballS IN PIXELS
SPEED_LIMIT = 40         # km / h
#OFFSET_START = 20       # FROM WALL IN PIXELS
#FRAMES_PER_SEC = 40     # SCREEN UPDATE RATE
END = False             # Fin de l'animation ?
FRICTION = 0.8          # Coefficient cinétique de friction
MASS = 1500             # Kg Poids du vehicule
flag = 0                # critère d'arret
x = 0                   # position du véhicule
DFA = 0                   # distance de freinage atteinte ?

################################################################################
def accelerate():
    global SPEED
    if SPEED + ACCELERATION*0.02 <= SPEED_LIMIT/3.6 : # si le véhicule ne va pas dépasser la limite de vitesse (km/h vers m/s: /3.6)
        SPEED += ACCELERATION*0.02 # la boucle s'actualise toute les 20 ms d'où le *0.02
    elif SPEED > SPEED_LIMIT/3.6:            # si le véhicule a dépassé la vitesse limite il freine
        SPEED -= ACCELERATION*0.02           # ralentir

def decelerate():
    global SPEED, DECELERATION, DFA
    if DFA == 0: #Pour n'affecter a Decceleration une valeur une seule fois
        DECELERATION = (SPEED*SPEED)/(2*((WIDTH-BALL_RADIUS-x)/10))         # a = v²/2x
        DFA = 1
        SPEED -= DECELERATION*0.02
    else:
        SPEED -= DECELERATION*0.02

def stop_it():
    "arret de l'animation"
    global flag
    flag =0

def start_it():
    global flag, x, END, a
    "démarrage de l'animation"
    if END == True:
        x = 0
        END = False
    if flag == 0:       # pour ne lancer qu'une seule boucle
        flag =1
        moveCircle()

def moveCircle():
    global flag, x, END, DECELERATION, DFA, SPEED
    if SPEED != 0:                # si le demarrage ne se fait pas à vitesse nulle

        #if    distance au mur      >      distance de freinage       + Distance de sécurité    :
        if (WIDTH-BALL_RADIUS-x)/10 > (((SPEED)**2)/(2*FRICTION*9.81))+BALL_RADIUS/10 and DFA == 0:
            accelerate() #accélérer
        else:
            decelerate() #ralentir
    else:
        print ("Speed 1 ",SPEED)
        accelerate()

    if x<WIDTH-BALL_RADIUS and SPEED > 0: # si la voiture n'a pas atteint la fin et n'est pas arretée
        x+=SPEED/5
    else:
        END = True
        SPEED = StartSPEED
        DFA= 0
        stop_it()
    myCan.coords(i, x-BALL_RADIUS, HEIGHT/2-BALL_RADIUS, x+BALL_RADIUS, HEIGHT/2+BALL_RADIUS)
    if flag >0:
        root.after(20,moveCircle) # répetition de la boucle si le critere d'arret est bon

root = Tk()
root.title("Véhicule Ligne Droite")

myCan = Canvas(root,width=WIDTH,height=HEIGHT,borderwidth=1,relief='sunken')
myCan.pack(side=RIGHT, padx =5, pady =5)
myCan.create_line(0,HEIGHT/2-BALL_RADIUS-WALL,WIDTH,HEIGHT/2-BALL_RADIUS-WALL, width=3)
myCan.create_line(0,HEIGHT/2+BALL_RADIUS+WALL,WIDTH,HEIGHT/2+BALL_RADIUS+WALL, width=3)
myCan.create_line(WIDTH,HEIGHT-300,WIDTH,HEIGHT-200, width=5, fill="red")
i = myCan.create_oval(x-BALL_RADIUS, HEIGHT/2-BALL_RADIUS, x+BALL_RADIUS, HEIGHT/2+BALL_RADIUS, fill = "green")


newBtn1 = Button(root,text="GO",command=start_it)
newBtn1.pack()

newBtn2 = Button(root, text='Arrêter', command=stop_it)
newBtn2.pack()

newBtn3 = Button(root, text='Quit', command=root.quit)
newBtn3.pack()

root.mainloop()