from dataclasses import dataclass
import pygame,pytmx,pyscroll
from player import NPC
from sound import Sound
from tkinter import *



@dataclass
class Portal:
    from_world:str
    origin_point:str
    target_world:str
    teleport_point:str

@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    ceiling: list[pygame.Rect]
    bad: list[pygame.Rect]
    blockade: list[pygame.Rect]
    level: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data:pytmx.TiledMap
    portal:list[Portal]
    npc: list[NPC]


class MapManager:
    def  __init__(self,screen,player,sound,pressed2):
        self.maps={}
        self.screen=screen
        self.player=player
        self.sound=sound
        self.pressed2=pressed2
        self.move_forward={"move":FALSE}
        self.current_map="world_1"
        self.register_map("world_1",portal=[
            Portal(from_world='world_1',origin_point='enter.level_1',target_world='level_1',teleport_point='spawn.enter.level_1'),
            Portal(from_world='world_1',origin_point='enter.world_2',target_world='world_2',teleport_point='spawn.enter.world_2')
        ], npc=[
            
        ])
        self.register_map("level_1",portal=[
            Portal(from_world='level_1',origin_point='enter.level_1',target_world='level_1',teleport_point='spawn.enter.level_1'),
            Portal(from_world='level_1',origin_point='exit.level_1',target_world='world_1',teleport_point='spawn.exit.level_1')
        ], npc=[
            NPC("boss",nb_points=2),
            NPC("paul",nb_points=2)
        ])
        self.register_map("world_2",portal=[
            Portal(from_world='world_2',origin_point='exit.world_2',target_world='world_1',teleport_point='spawn.exit.world_1'),
            Portal(from_world='world_2',origin_point='enter.level_2',target_world='level_2',teleport_point='spawn.enter.level_2')
        ], npc=[

        ])
        self.register_map('level_2',portal=[
            Portal(from_world='level_2',origin_point='enter.level_2',target_world='level_2',teleport_point='spawn.enter.level_2'),
            Portal(from_world='level_2',origin_point='exit.level_2',target_world='world_2',teleport_point='spawn.exit.level_2')
        ], npc=[
            NPC("buche",nb_points=2),
            NPC("paul",nb_points=2),
            NPC("paul1",nb_points=2),
            NPC("boss",nb_points=2),
            NPC("boss1",nb_points=2)
        ])

        
        self.teleport_player("player")
        self.teleport_npc()

    
    def go_portal(self):
         #Portals
        for portals in self.get_map().portal:

            if portals.from_world==self.current_map:
                point=self.get_object(portals.origin_point)
                rect=pygame.Rect(point.x,point.y,point.width,point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal=portals
                    self.current_map=portals.target_world
                    self.teleport_player(portals.teleport_point)


    def check_collision(self):
        if self.current_map=='world_1' or self.current_map=='world_2':
            #Collisions
            for sprite in self.get_group().sprites():
                if sprite.feet.collidelist(self.get_walls()) >-1:
                    sprite.move_back()

                if sprite.feet.collidelist(self.get_level()) <= -1:
                    self.go_portal()
                if sprite.feet.collidelist(self.get_level()) > -1 :
                    for obj in pytmx.util_pygame.load_pygame(f"map/{self.current_map}.tmx"):
                        if obj.name=="enter.level_1":
                            self.text_level(1)
                        elif obj.name=="enter.level_2":
                            self.text_level(2)


        elif self.current_map=='level_1' or self.current_map=='level_2':
            for sprite in self.get_group().sprites():
                if sprite==self.player:


                    if self.current_map=='level_1':        

                        if sprite.feet.collidelist(self.get_walls())<=-1:        #Gravity setting for level_1
                            sprite.move_gravity()

                        if sprite.feet.collidelist(self.get_bad())>-1:          #Bad setting for level_1
                            self.sound.mario_death.play()
                            self.teleport_player(f'spawn.enter.{self.current_map}')

                    if self.current_map=='level_2':   
                                                      
                        if sprite.feet.collidelist(self.get_walls()) <=-1:      #Gravity setting for level_2
                            for sprites in self.get_group().sprites():
                                if type(sprites) is NPC:
                                    if sprites.name=='buche':
                                        if sprites.feet.colliderect(self.player.rect):
                                            None
                                        else:
                                            sprite.move_gravity()


                        for sprites in self.get_group().sprites():
                            if type(sprites) is NPC:
                                if sprites.name=='buche':
                                    if sprite.feet.collidelist(self.get_bad())>-1:      #Bad setting for level_2
                                        self.sound.mario_death.play()
                                        sprites.teleport_spawn0()
                                        self.move_forward["move"]=FALSE
                                        self.teleport_player(f'spawn.enter.{self.current_map}')


                    
                    if sprite.feet.collidelist(self.get_map().blockade)>-1:
                        if sprite.feet.collidelist(self.get_walls())>-1:
                            sprite.move_back()
                        else:
                            sprite.move_back()
                            sprite.move_gravity()
                    if sprite.feet.collidelist(self.get_level()) > -1 :
                        self.go_portal()
                    

    

                if type(sprite) is NPC:
                    if sprite.name=='boss':
                        if sprite.feet.colliderect(self.player.rect):
                            self.sound.mario_death.play()
                            pygame.event.wait(20)
                            self.teleport_player(f'spawn.enter.{self.current_map}')
                    if sprite.name=='boss1':
                        if sprite.feet.colliderect(self.player.rect):
                            self.sound.mario_death.play()
                            pygame.event.wait(20)
                            self.teleport_player(f'spawn.enter.{self.current_map}')
                    if sprite.name=='paul':
                        sprite.speed=2
                        if sprite.feet.colliderect(self.player.rect):
                            self.sound.mario_death.play()
                            self.teleport_player(f'spawn.enter.{self.current_map}')
                    if sprite.name=='paul1':
                        sprite.speed=2
                        if sprite.feet.colliderect(self.player.rect):
                            self.sound.mario_death.play()
                            self.teleport_player(f'spawn.enter.{self.current_map}')
                    if sprite.name=='buche':
                        sprite.speed=1
                        for sprites in self.get_group().sprites():
                            if type(sprites) is NPC:
                                if sprites.name!='buche':
                                    if sprites.feet.colliderect(self.player.rect):
                                        sprite.teleport_spawn0()
                                        self.move_forward["move"]=FALSE
                        if sprite.feet.collidelist(self.get_walls())>-1:
                            print("hello")
                            sprite.speed=0.3
                        
                            
                        
                

                




    def text_level(self,num):
        window=Tk()
        window.bind('<Escape>',lambda e: window.destroy())
        label=Label(window,text=f"Souhaitez-vous entrer dans le monde {num}",font =("Cambria", 12))
        window.geometry("300x150+715+250")
        button_1=Button(window, text="Yes",font =("Cambria", 9),command=lambda:[self.go_portal(),window.destroy()])
        button_2=Button(window, text="No",font =("Cambria",9),command=lambda:[self.player.move_back(),window.destroy()])
        label.place(x=10,y=50)
        button_1.place(x=30,y=80)
        button_2.place(x=225,y=80)
        window.mainloop()

    def teleport_player(self,name):
        point=self.get_object(name)
        self.player.position[0]=point.x
        self.player.position[1]=point.y
        self.player.save_location()

    """
    def teleport_teleporter(self):
        self.teleporter.move_ur()
        self.teleporter.position[0]=self.player.position[0]
        self.teleporter.position[1]=self.player.position[1]
        self.player.save_location()
    """
    




    def register_map(self,name,portal=[],npc=[],geom=[]):
        #Chargement de la carte
        tmx_data=pytmx.util_pygame.load_pygame(f"map/{name}.tmx")
        map_data=pyscroll.data.TiledMapData(tmx_data)
        map_layer=pyscroll.orthographic.BufferedRenderer(map_data,self.screen.get_size())
        map_layer.zoom=2
        

        #groupe de calques
        group=pyscroll.PyscrollGroup(map_layer=map_layer,default_layer=5)
        group.add(self.player)
        #group.remove(self.player)

        for npcs in npc:
            group.add(npcs)


        #Collisions
        walls=[]
        level=[]
        ceiling=[]
        bad=[]
        blockade=[]

        for obj in tmx_data.objects:
            if obj.type=='collision':
                walls.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))

            elif obj.type=='level':
                level.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))
            
            elif obj.type=='ceiling':
                ceiling.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))

            elif obj.type=='bad':
                bad.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))
            
            elif obj.type=='blockade':
                blockade.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))

        #Créerun objet map
        self.maps[name]=Map(name,walls,ceiling,bad,blockade,level,group,tmx_data,portal,npc)


    def get_map(self): return self.maps[self.current_map]

    def get_group(self): return self.get_map().group

    def get_walls(self): return self.get_map().walls

    def get_ceiling(self): return self.get_map().ceiling

    def get_bad(self): return self.get_map().bad

    def get_level(self): return self.get_map().level

    def get_object(self,name): return self.get_map().tmx_data.get_object_by_name(name)


    def teleport_npc(self):
        for map in self.maps:
            map_data=self.maps[map]
            npc=map_data.npc

            for npcs in npc:
                npcs.load_points(map_data.tmx_data)
                npcs.teleport_spawn()



    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update2(self):
        self.get_group().update()
        self.check_collision()

        #for npcs in self.get_map().npc:
            #npcs.move()

        for sprite in self.get_group().sprites():
            if type(sprite) is NPC:
                if sprite.name!="buche":
                    sprite.move()
                if sprite.name=="buche":
                    if self.player.feet.collidelist(self.get_level())>-1:
                        sprite.teleport_spawn0()
                        self.move_forward["move"]=FALSE
                    if self.move_forward["move"]==YES:
                        sprite.move()
                    if self.player.feet.colliderect(sprite):
                        self.move_forward["move"]=YES

        


                