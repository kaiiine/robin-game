from tkinter import Tk, Canvas, Button, PhotoImage
from pathlib import Path
import pygame
from game import Game


# --- Paths robustes (par rapport à ce fichier) ---
BASE_DIR = Path(__file__).resolve().parent          # .../src
PROJECT_DIR = BASE_DIR.parent                       # .../robin-game
SPRITES_DIR = PROJECT_DIR / "sprites"
BG_IMAGE = SPRITES_DIR / "robin_alone.png"


def run_game():
    pygame.init()
    pygame.joystick.init()
    game = Game()
    game.run()


def main():
    window = Tk()
    window.title("NSRB")
    window.geometry("1200x675+180+100")
    window.minsize(1200, 675)
    window.maxsize(1200, 675)
    window.bind("<Escape>", lambda e: window.destroy())

    # IMPORTANT: garder une référence (photo) vivante
    photo = PhotoImage(file=str(BG_IMAGE)).subsample(1)

    canvas = Canvas(window, width=1200, height=675, bg="#0060AD", highlightthickness=0)
    canvas.pack()

    canvas.create_image(1200 / 2, 675 / 2, image=photo)
    canvas.create_text(
        670,
        120,
        text="New Super Robin Bros",
        font=("Lucida Handwriting", 25, "bold", "underline"),
        fill="black",
    )

    def on_play():
        window.destroy()
        run_game()

    Button(
        window,
        text="     Play     ",
        fg="White",
        bg="Black",
        font=("Dragon FREE", 14),
        command=on_play,
    ).place(x=1000, y=300)

    Button(
        window,
        text="     Quit     ",
        fg="White",
        bg="Black",
        font=("Dragon FREE", 14),
        command=window.destroy,
    ).place(x=1000, y=370)

    # Empêche la GC de supprimer l'image
    window._bg_photo = photo

    window.mainloop()


if __name__ == "__main__":
    main()
