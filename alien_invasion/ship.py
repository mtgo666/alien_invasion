#ship类负责管理飞船大部分行为
import pygame
from pygame.sprite import Sprite

class Ship(Sprite): #继承Sprite类

    def __init__(self,ai_game) :
        #初始化飞船并设置其初始位置
        super().__init__()
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        self.screen_rect=ai_game.screen.get_rect()

        #加载飞船图像并获取外接矩形
        self.image=pygame.image.load('images/ship.bmp')
        self.rect=self.image.get_rect()  #rect:矩形

        #对于每艘新飞船，都将其放在屏幕底部的中央
        self.rect.midbottom=self.screen_rect.midbottom

        #在飞船的属性x中存储小数值
        self.x=float(self.rect.x)

        #移动标志
        self.moving_right=False
        self.moving_left=False
    
    def update(self):
        #根据移动标志调整飞船位置
        if self.moving_right and self.rect.right<self.screen_rect.right:
            self.x+=self.settings.ship_speed
        if self.moving_left and self.rect.left>0:
            self.x-=self.settings.ship_speed
        
        #根据self.x来更新控制飞船位置的rect对象
        self.rect.x=self.x

    def blitme(self):
        #在指定位置绘制飞船
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        #让飞船在屏幕底端居中
        self.rect.midbottom=self.screen_rect.midbottom
        self.x=float(self.rect.x)


