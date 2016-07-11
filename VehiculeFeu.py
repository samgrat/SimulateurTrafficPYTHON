# tkinter_app_27Nov2010.py
from tkinter import *
import time

# 1 m = 10 px
WIDTH = 1010            # OF SCREEN IN PIXELS
HEIGHT = 500            # OF SCREEN IN PIXELS
BALLS = 1               # IN SIMULATION
WALL = 5                # FROM SIDE IN PIXELS
DFM = 500               # Distance Feu/Mur
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
END = False             # test: Fin de l'animation ?
FRICTION = 0.8          # Coefficient cinétique de friction
MASS = 1500             # Kg Poids du vehicule
flag = 0                # critère d'arret
x = 0                   # position du véhicule
DFA = False             # test: distance de freinage atteinte ?
FRouge = False          # test: feu rouge ?
DAA = 0

################################################################################
def accelerate():
    global SPEED, DFA, dddd
    DFA = False
    if SPEED + ACCELERATION*0.02 <= SPEED_LIMIT/3.6 : # si le véhicule ne va pas dépasser la limite de vitesse (km/h vers m/s: /3.6)
        SPEED += ACCELERATION*0.02 # la boucle s'actualise toute les 20 ms d'où le *0.02
    elif SPEED > SPEED_LIMIT/3.6:            # si le véhicule a dépassé la vitesse limite il freine
        SPEED -= ACCELERATION*0.02           # ralentir

def decelerate():
    global SPEED, DECELERATION, DFA
    if DFA == False: #Pour n'affecter a Decceleration une valeur une seule fois
        DECELERATION = (SPEED*SPEED)/(2*(DAA))       # a = v²/2x
        DFA = True
        SPEED -= DECELERATION*0.02
    else:
        SPEED -= DECELERATION*0.02

def stop_it():
    "arret de l'animation"
    global flag
    flag =0

def moveCircle():
    global flag, x, END, DECELERATION, DFA, SPEED,DAA
    if SPEED != 0:                # si le demarrage ne se fait pas à vitesse nulle
        """"""""""""""""""""

        print ("Speed 2 ",SPEED)
        print ("Dmur ",(WIDTH-BALL_RADIUS-x)/10," Dstop ", (((SPEED)**2)/(2*FRICTION*9.81))+BALL_RADIUS/10 )

        """"""""""""""""""""
        if FRouge == True and x < WIDTH-DFM: # si le feu est rouge et que le vehicule ne l'a pas dépassé
            DAA = (WIDTH-DFM - BALL_RADIUS-x)/10 # La distance avant arret est celle du véhicule au feu
        else:
            DAA = (WIDTH-BALL_RADIUS-x)/10 #  La distance avant arret est celle du véhicule au mur

        #if Distance Avant Arret > distance de freinage + Distance de sécurité:
        if DAA > (((SPEED)**2)/(2*FRICTION*9.81))+BALL_RADIUS/10 and DFA == False:
            accelerate()
        elif DAA <= (((SPEED)**2)/(2*FRICTION*9.81))+BALL_RADIUS/10: # sinon on freine
            decelerate()
        else: #si le feu repasse au vert
            accelerate()
    else:
        print ("Speed 1 ",SPEED)
        SPEED += ACCELERATION*0.02
    if DAA>0 and SPEED > 0: # si la voiture n'a pas atteint le mur ou le feu et n'est pas arretée
        x+=SPEED/5
    else:
        if DAA == (WIDTH-BALL_RADIUS-x)/10 : # si la voiture a atteint le mur
            END = True
        SPEED = StartSPEED
        DFA = False
        stop_it()
    myCan.coords(i, x-BALL_RADIUS, HEIGHT/2-BALL_RADIUS, x+BALL_RADIUS, HEIGHT/2+BALL_RADIUS)
    if flag >0:
        root.after(20,moveCircle) # répetition de la boulce si le critere d'arret est bon


def start_it():
    global flag, x, END
    "démarrage de l'animation"
    if END == True:
        x = 0
        END = False
    if flag == 0:       # pour ne lancer qu'une seule boucle
        flag =1
        moveCircle()

def change_feu():
    global FRouge, SPEED, END, flag
    if FRouge == False:
        myCan.itemconfigure(f, fill = "red")
        FRouge = True
    else:
        myCan.itemconfigure(f, fill = "green")
        FRouge = False
        if END == False: # si le vehicule n'est pas arreté au mur de fin
            start_it()





root = Tk()
root.title("Véhicule Feu")

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
i = myCan.create_oval(x-BALL_RADIUS, HEIGHT/2-BALL_RADIUS, x+BALL_RADIUS, HEIGHT/2+BALL_RADIUS, fill = "green")


newBtn1 = Button(root,text="GO",command=start_it)
newBtn1.pack()

newBtn2 = Button(root, text='Pause', command=stop_it)
newBtn2.pack()

newBtn3 = Button(root, text='Feu', command=change_feu)
newBtn3.pack()

newBtn4 = Button(root, text='Quit', command=root.quit)
newBtn4.pack()

root.mainloop()