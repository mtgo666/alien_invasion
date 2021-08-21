import sys
from time import sleep
import pygame
#from pygame.constants import KEYUP
from setting import settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreBoard import ScoreBoard

filename='high_score.txt' #记录最高分的文件

class AlienInvasion:
   #管理游戏资源和行为的类
    def __init__(self) :
        #初始化游戏并创建游戏资源
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("wmzb.mp3")
        self.sound=pygame.mixer.Sound("bom.wav") #添加声音变量
        pygame.mixer.music.play(-1)
        self.settings=settings()
        self.screen=pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        #创建一个用于存储游戏统计信息的实例
        self.stats=GameStats(self)
        self.sb=ScoreBoard(self) #创建记分牌

        self.ship=Ship(self)
        self.bullets=pygame.sprite.Group() #该编组用于存储子弹
        self.aliens=pygame.sprite.Group() #该编组用于存储外星人群
        self._create_fleet()

        #创建play按钮
        self.play_button=Button(self,"Play")

    def run_game(self):
         pygame.mixer.init()
         pygame.mixer.music.load("wmzb.mp3")  #游戏开始时播放音乐
         pygame.mixer.music.play(-1)
        #开启游戏的主循环
         while True:
            #pygame.mixer.music.play(-1)
            #监视键盘和鼠标事件
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            #print(len(self.bullets))
            #每次循环都重绘屏幕
            self._update_screen()
    
    def _check_events(self):
        #响应鼠标和按键事件
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                #filename='high_score.txt' 
                with open(filename,'w') as file_object:
                    file_object.write(str(self.stats.high_score))
                sys.exit()

            elif event.type==pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type==pygame.KEYUP:
                self._check_keyup_events(event)
            
            elif event.type==pygame.MOUSEBUTTONDOWN:  #检测是否按下play按钮
                mouse_pos=pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self,mouse_pos):
        #在玩家单机play按钮时开始新游戏
        button_clicked=self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            
            #重置游戏设置
            self.settings.initialize_dynamic_settings()
            #重置游戏统计信息
            self.stats.reset_stats()
            self.stats.game_active=True
            self.sb.prep_score() #每次新游戏开始时重置得分
            self.sb.prep_level() #每次新游戏开始时重置等级
            self.sb.prep_ships() #让玩家知道自己有多少艘飞船

            #清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            #创建一群新的外星人并让飞船居中
            self._create_fleet()
            self.ship.center_ship()

            #隐藏鼠标光标
            pygame.mouse.set_visible(False)


    def _check_keydown_events(self,event):
        #处理keydown事件
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=True
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=True
        elif event.key==pygame.K_q:  #按q退出游戏
            with open(filename,'w') as file_object:
                file_object.write(str(self.stats.high_score))
            sys.exit()
        elif event.key==pygame.K_SPACE:
            self._fire_bullet()
    
    def _check_keyup_events(self,event):
        #处理keyup事件
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=False
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=False
    
    def _fire_bullet(self):
        if len(self.bullets)<self.settings.bullet_allowed: #每次创建新子弹前都检查下当前子弹数是否小于能存储的子弹数
            new_bullet=Bullet(self)  #创建出一个子弹实例
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        #管理子弹的方法
        self.bullets.update() #更新子弹的位置

        #删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom<=0:
                self.bullets.remove(bullet)
        
        self._check_bullets_aliens_collisions() #检测子弹和外星人碰撞

    
    def _check_bullets_aliens_collisions(self):
        #检测子弹和外星人碰撞，如果是，就删除相应的子弹和外星人
        #函数sprite.groupcollide()将一个编组中的每个元素的rect和另一个编组中的每个元素的rect进行比较，并返回一个字典
        collisions=pygame.sprite.groupcollide(self.bullets,self.aliens,True,True) #两个实参true让pygame删除发生碰撞的子弹和外星人
        if collisions:
            #pygame.mixer.music.stop()
            pygame.mixer.Sound.play(self.sound) #碰撞时发出声音
            for aliens in collisions.values():
                self.stats.score+=self.settings.alien_points*len(aliens) #如果一个子弹消灭了两个外星人，确保能得两个外星人的分
                self.sb.prep_score()
                self.sb.check_high_score() #每次消灭外星人更新得分后检查是否诞生最高分
        if not self.aliens:
            #删除现有的子弹并创建一群新外星人
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #提高等级
            self.stats.level+=1
            self.sb.prep_level()
            if self.stats.level>8:
                self.settings.increase_bullet_level()

    def _ship_hit(self):
        #响应飞船被外星人撞到
        if self.stats.ships_left>0:
            #将ship_left减一并更新余下的飞船数
            self.stats.ships_left-=1
            self.sb.prep_ships()

            #清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            #创建一群新的外星人，并将飞船放在底部中央
            self._create_fleet()
            self.ship.center_ship()

            #暂停
            sleep(1.0)
        else:
            self.stats.game_active=False

            #游戏结束后显示鼠标光标
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        #检查是否有外星人位于屏幕边缘并更新外星人群中所有外星人的位置
        self._check_fleet_edges()
        self.aliens.update()

        #检测外星人和飞船间的碰撞
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()

        #检测是否有外星人到达屏幕底端
        self._check_aliens_bottom()
    
    def _create_fleet(self):    #fleet:船队；舰队
        #创建外星人群

        #创建一个外星人并计算一行能容纳多少外星人
        alien=Alien(self)
        alien_width,alien_height=alien.rect.size    #获取外星人的高度和宽度，属性size是个元组，包含了rect对象的高度和宽度
        avaliable_space_x=self.settings.screen_width-(2*alien_width)
        number_alien_x=avaliable_space_x//(2*alien_width)

        #计算屏幕上可容纳多少行外星人
        ship_height=self.ship.rect.height
        avaliable_space_y=(self.settings.screen_height-(3*alien_height)-ship_height)
        number_rows=avaliable_space_y//(2*alien_height)

        #创建外星人群
        for row_number in range(number_rows):
            for alien_number in range(number_alien_x):
                self._create_alien(alien_number,row_number)

    def _create_alien(self,alien_number,row_number):
            #创建第一个外星人并将其加入当前行
            alien=Alien(self)
            alien_width,alien_height=alien.rect.size 
            alien.x=alien_width+2*alien_width*alien_number
            alien.rect.x=alien.x
            alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
            self.aliens.add(alien)

    def _check_fleet_edges(self):
        #有外星人到达屏幕边缘时采取相应的措施
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _check_aliens_bottom(self):
        #检测是否有外星人到达屏幕底端
        screen_rect=self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom>=screen_rect.bottom:
                #像飞船被撞到那样处理
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        #将整体外星人下移，并改变他们的方向
        for alien in self.aliens.sprites():
            alien.rect.y+=self.settings.fleet_drop_speed
        self.settings.fleet_direction*=-1
     
    def _update_screen(self):
        #更新屏幕上的图像，并切换到新屏幕
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.aliens.draw(self.screen) #把编组aliens中的每个元素都绘制出来

            #显示得分
            self.sb.show_score()

            #如果游戏处于非活动状态，就绘制play按钮
            if not self.stats.game_active:
                self.play_button.draw_button()
            pygame.display.flip() #更新显示到屏幕上

if __name__=='__main__':
    #创建游戏实例并运行游戏
    ai=AlienInvasion()
    ai.run_game()
