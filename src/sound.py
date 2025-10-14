import pygame
class Sound():


    def __init__(self):
        self.music=pygame.mixer.music.load("sound\\level_1_sound.MP3")
        self.music_volume=pygame.mixer.music.set_volume(0.25)
        self.music_play=pygame.mixer.music.play(loops=1)
        self.mario_jump=pygame.mixer.Sound("sound\\mario_jump.MP3")
        self.mario_death=pygame.mixer.Sound("sound\\mario_death.MP3")
        self.sound_volume()


    def sound_volume(self):
        self.mario_jump.set_volume(0.15)
        self.mario_death.set_volume(0.65)