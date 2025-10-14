from tkinter import *
import pygame
import pytmx
import pyscroll
from player import Player
from map import MapManager
from sound import Sound
from player import NPC

class Game :
    def __init__(self):
        pygame.joystick.init()
        # Create window
        self.screen=pygame.display.set_mode((800,600),pygame.RESIZABLE)
        pygame.display.set_caption("New Super Robin& Bros")

        self.joysticks=[pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        self.sound=Sound()
        

        #Generate a player
        self.player=Player()
        self.sound=Sound()
        self.pressed1={}
        self.pressed2={}
        self.pressed3=[0,0]
        self.pressed4={'button0':False,
                       'button2':False,
                       'button2':False,
                       'button3':False
                       }
        self.map_manager=MapManager(self.screen,self.player,self.sound,self.pressed2)
        self.jumpy=[0,0]
        

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if self.map_manager.current_map == 'world_1' or self.map_manager.current_map == 'world_2' :



            if pressed[pygame.K_UP] and pressed[pygame.K_RIGHT] or (self.pressed3[1]<0 and abs(1-self.pressed3[1])>=1.5 and self.pressed3[0]>0 and abs(1-self.pressed3[0])<=0.3):
                self.player.move_ur()
                self.player.change_animation('right')

            elif pressed[pygame.K_UP] and pressed[pygame.K_LEFT] or (self.pressed3[1]<0 and abs(1-self.pressed3[1])>=1.5 and self.pressed3[0]<0 and abs(1-self.pressed3[0])>=1.5):
                self.player.move_ul()
                self.player.change_animation('left')

            elif pressed[pygame.K_DOWN] and pressed[pygame.K_RIGHT] or (self.pressed3[1]>0 and abs(self.pressed3[1]-1)<=0.3 and self.pressed3[0]>0 and abs(1-self.pressed3[0])<=0.3):
                self.player.move_dr()
                self.player.change_animation('right')
            
            elif pressed[pygame.K_DOWN] and pressed[pygame.K_LEFT] or (self.pressed3[1]>0 and abs(self.pressed3[1]-1)<=0.3 and self.pressed3[0]<0 and abs(1-self.pressed3[0])>=1.5):
                self.player.move_dl()
                self.player.change_animation('left')

            elif pressed[pygame.K_UP] or self.pressed3[1]<0 and abs(1-self.pressed3[1])>=1.5:
                self.player.move_up()
                self.player.change_animation('up')

            elif pressed[pygame.K_DOWN] or self.pressed3[1]>0 and abs(self.pressed3[1]-1)<=0.3:
                self.player.move_down()
                self.player.change_animation('down')


            elif pressed[pygame.K_RIGHT] or self.pressed3[0]>0 and abs(1-self.pressed3[0])<=0.3:
                self.player.move_right()
                self.player.change_animation('right')


            elif pressed[pygame.K_LEFT] or self.pressed3[0]<0 and abs(1-self.pressed3[0])>=1.5:
                self.player.move_left()
                self.player.change_animation('left')


        elif self.map_manager.current_map == 'level_1' or self.map_manager.current_map == 'level_2' :

            
            if self.pressed1.get(pygame.K_RIGHT) or self.pressed3[0]==1:
                self.player.move_right()
                self.player.change_animation('right')
            elif self.pressed1.get(pygame.K_LEFT) or self.pressed3[0]==(-1.000030518509476):
                self.player.move_left()
                self.player.change_animation('left') 
     
            if self.pressed2.get(pygame.K_UP):
                if self.map_manager.current_map=='level_1':
                    self.check_jump()
                if self.map_manager.current_map=='level_2':
                    self.check_jump2()
                
                    
                

            
            
            
            if self.pressed4['button0']==True:

                if self.map_manager.current_map=='level_1':
                    self.check_jump()
                if self.map_manager.current_map=='level_2':
                    self.check_jump2()

            elif self.pressed4['button0']==True and self.player.feet.collidelist(self.map_manager.get_map().blockade) >-1:
                self.pressed4['button0']=True


    def check_jump(self):
        if self.player.feet.collidelist(self.map_manager.get_walls())>-1:
            self.jumpy[0]=self.player.position[1]
            self.jumpy[1]=0
        self.player.move_up_2()
        if self.player.feet.collidelist(self.map_manager.get_walls())<=-1:
            self.jumpy[1]=self.player.position[1]
            if abs(self.jumpy[0]-self.jumpy[1])>84 or self.player.feet.collidelist(self.map_manager.get_map().blockade)>-1:
                self.pressed2[1073741906]=False
                self.pressed4['button0']=False

    def check_jump2(self):
        for sprite in self.map_manager.get_group().sprites():
            if type(sprite) is NPC:
                if sprite.name=='buche':
                    if self.player.feet.collidelist(self.map_manager.get_walls())>-1 or sprite.feet.colliderect(self.player.rect):
                        self.jumpy[0]=self.player.position[1]
                        self.jumpy[1]=0
                    self.player.move_up_2()
                    if self.player.feet.collidelist(self.map_manager.get_walls())<=-1 or not sprite.feet.colliderect(self.player.rect):
                        self.jumpy[1]=self.player.position[1]
                        if abs(self.jumpy[0]-self.jumpy[1])>84 or self.player.feet.collidelist(self.map_manager.get_map().blockade)>-1:
                            self.pressed2[1073741906]=False
                            self.pressed4['button0']=False


    def update(self):
        self.map_manager.update2()
    


    def run(self):
                clock=pygame.time.Clock()
                # Loop oh the game
                running=True

                while running:
                    self.player.save_location()
                    self.handle_input()
                    self.update()
                    self.map_manager.draw()
                    pygame.display.flip()
                    for event in pygame.event.get():
                        if event.type==pygame.QUIT:
                            running=False    


                        elif event.type==pygame.JOYBUTTONDOWN:

                            if self.player.feet.collidelist(self.map_manager.get_walls()) <=-1:
                                self.pressed4['button0']=False
                                self.pressed4['button1']=False
                                self.pressed4['button2']=False
                                self.pressed4['button3']=False

                            elif abs(self.jumpy[0]-self.jumpy[1])<=84:
                                if pygame.joystick.Joystick(0).get_button(0):
                                    self.pressed4['button0']=True
                                    if self.map_manager.current_map=='level_1' or self.map_manager.current_map=='level_2':
                                        self.sound.mario_jump.play()
                                elif pygame.joystick.Joystick(0).get_button(1):
                                    self.pressed4['button1']=True
                                elif pygame.joystick.Joystick(0).get_button(2):
                                    self.pressed4['button2']=True
                                elif pygame.joystick.Joystick(0).get_button(3):
                                    self.pressed4['button3']=True

                                if self.player.feet.collidelist(self.map_manager.get_level())>-1:
                                    if pygame.joystick.Joystick(0).get_button(0):
                                        lambda:[self.map_manager.go_portal()]

                            for sprites in self.map_manager.get_group().sprites(): 
                                if type(sprites) is NPC:
                                        if sprites.name=='buche':
                                            if sprites.feet.colliderect(self.player.rect):
                                                self.pressed4['button0']=True
                                                if self.map_manager.current_map=='level_1' or self.map_manager.current_map=='level_2':
                                                    self.sound.mario_jump.play()

                        elif event.type==pygame.JOYBUTTONUP:
                            self.pressed4['button0']=False
                            self.pressed4['button1']=False
                            self.pressed4['button2']=False
                            self.pressed4['button3']=False
                            self.jumpy=[0,0]

                        elif event.type==pygame.JOYAXISMOTION:
                            if event.axis<2:
                                self.pressed3[event.axis]=event.value


                        if self.map_manager.current_map == 'level_1' or self.map_manager.current_map == 'level_2' :
                            if event.type ==pygame.KEYDOWN:

                                self.pressed1[event.key]=True

                                if self.player.feet.collidelist(self.map_manager.get_walls()) <=-1:
                                    self.pressed2[event.key]=False
                                    


                                elif abs(self.jumpy[0]-self.jumpy[1])<=84:
                                    self.sound.mario_jump.play()
                                    self.pressed2[event.key]=True
                                
                                for sprites in self.map_manager.get_group().sprites():
                                    if type(sprites) is NPC:
                                        if sprites.name=='buche':
                                            if sprites.feet.colliderect(self.player.rect):
                                                self.pressed2[event.key]=True

                            elif event.type==pygame.KEYUP:
                                self.pressed1[event.key]=False
                                self.pressed2[event.key]=False
                                self.jumpy=[0,0]

                            

    
                    clock.tick(60)

                pygame.quit()

