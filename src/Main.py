from tkinter import *
import pygame
from game import Game

window=Tk()
window.title("NSRB")
window.geometry("1200x675+180+100")
window.minsize(1200,675)
window.maxsize(1200,675)
window.iconbitmap("sprites\\mario1.ico")
window.bind('<Escape>',lambda e: window.destroy())


photo=PhotoImage(file='sprites\\robin_alone.png').subsample(1)
canvas_0=Canvas(window,width=1200,height=675,bg='#0060AD')
canvas_0.create_image(1200/2,675/2,image=photo)
canvas_0.create_text(670,120, text="New Super Robin Bros",font=("Lucida Handwriting",25,'bold','underline'))
canvas_0.pack()


def run():
    #if __name__=='__main__':()
    pygame.init()
    pygame.joystick.init()
    game=Game()
    game.run()


button_0=Button(window,text='     Play     ',fg='White',bg="Black",font=("Dragon FREE",14), command=lambda:[window.destroy(),run()])
button_0.place(x=1000,y=300)

button_1=Button(window,text='     Quit     ',fg='White',bg="Black",font=("Dragon FREE",14), command=window.destroy)
button_1.place(x=1000,y=370)

window.mainloop()  