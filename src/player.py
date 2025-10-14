import pygame
from animation import AnimateSprite

class Entity(AnimateSprite):

    def __init__(self,name,x,y):
        super().__init__(name)
        
        self.image=self.get_image(0,0)
        self.image.set_colorkey([0,0,0])
        self.rect=self.image.get_rect()
        
        self.position=[x,y]
        self.jumpy=self.position[1]
        
        self.feet=pygame.Rect(0,0,self.rect.width*0.5,12)
        self.old_position=self.position.copy()


    def save_location(self): 
        self.old_position=self.position.copy()


    def move_right(self): 
        self.position[0]+=self.speed
    def move_left(self): 
        self.position[0]-=self.speed
    def move_up(self):
        self.position[1]-=self.speed
    def move_up_2(self):
        self.position[1]-=8
    def move_down(self): 
        self.position[1]+=self.speed
    def move_gravity(self): 
        self.position[1]+=self.speed*2
    def move_antigravity(self): 
        self.position[1]-=self.speed*2
    def move_down_3(self): 
        self.position[1]+=self.speed*6
    def move_ur(self):
        self.position[1]-=2
        self.position[0]+=1
    def move_ul(self):
        self.position[1]-=2
        self.position[0]-=1  
    def move_dr(self):
        self.position[1]+=2
        self.position[0]+=1      
    def move_dl(self):
        self.position[1]+=2
        self.position[0]-=1


    def update(self):
        self.rect.topleft=self.position
        self.feet.midbottom=self.rect.midbottom

    def move_back(self):                    
        self.position=self.old_position
        self.rect.topleft=self.position
        self.midbottom=self.rect.midbottom

        
    



class Player(Entity):
    def __init__(self):
        super().__init__('robin',0,0)



class NPC(Entity):

    def __init__(self,name,nb_points):
        super().__init__(name,0,0)

        self.nb_points = nb_points
        self.points=[]
        self.current_point=0
        self.name=name
        self.speed=1
        


    def move(self):
        current_point=self.current_point
        target_point=self.current_point+1

        if target_point>=self.nb_points:
            target_point=0

        current_rect=self.points[current_point]
        target_rect=self.points[target_point]

        if current_rect.y<target_rect.y and abs(current_rect.x-target_rect.x)<3:
            self.move_down()
            self.change_animation('down')
        elif current_rect.y>target_rect.y and abs(current_rect.x-target_rect.x)<3:
            self.move_up()
            self.change_animation('up')
        elif current_rect.x<target_rect.x and abs(current_rect.y-target_rect.y)<3:
            self.move_right()
            self.change_animation('right')
        elif current_rect.x>target_rect.x and abs(current_rect.y-target_rect.y)<3:
            self.move_left()
            self.change_animation('left')

        if self.rect.colliderect(target_rect):
            self.current_point=target_point


    def teleport_spawn(self):
        location=self.points[self.current_point]
        self.position[0]=location.x
        self.position[1]=location.y
        self.save_location()

    def teleport_spawn0(self):
        location=self.points[0]
        self.position[0]=location.x
        self.position[1]=location.y
        self.save_location()



    def load_points(self,tmx_data):
        for num in range(1,self.nb_points+1):
            point=tmx_data.get_object_by_name(f"{self.name}_path{num}")
            rect=pygame.Rect(point.x,point.y,point.width,point.height)
            self.points.append(rect)
