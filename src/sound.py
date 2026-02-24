import pygame
from pathlib import Path

class Sound():


    def __init__(self):
        sound_dir = Path(__file__).parent.parent / "sound"
        self.music=pygame.mixer.music.load(str(sound_dir / "level_1_sound.mp3"))
        self.music_volume=pygame.mixer.music.set_volume(0.25)
        self.music_play=pygame.mixer.music.play(loops=1)
        self.mario_jump=pygame.mixer.Sound(str(sound_dir / "mario_jump.mp3"))
        self.mario_death=pygame.mixer.Sound(str(sound_dir / "mario_death.mp3"))
        self.sound_volume()


    def sound_volume(self):
        self.mario_jump.set_volume(0.15)
        self.mario_death.set_volume(0.65)