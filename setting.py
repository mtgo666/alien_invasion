#设置类：将这个项目中所有的设置都存储在一个地方
class settings:
    #存储游戏《外星人入侵》中所有设置的类
    
    def __init__(self) :
        #初始化游戏的静态设置

        #屏幕设置
        self.screen_width=1200
        self.screen_height=800
        self.bg_color=(230,230,230)

        #飞船设置
        self.ship_speed=1.5
        self.ship_limit=2 #拥有的飞船数

        #子弹设置
        #self.bullet_width=3
        #self.bullet_height=15
        self.bullet_color=(60,60,60)
        self.bullet_allowed=3

        #外星人设置
        self.fleet_drop_speed=10 #有外星人碰到屏幕边缘时，外星人群向下移动的速度

        #加快游戏节奏的速度
        self.speedup_scale=1.1
        #外星人分数的提高速度
        self.score_scale=1.5
        #子弹的升级速度
        self.bullet_scale=1.2
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        #初始化随游戏进行而变化的设置
        self.ship_speed=1.5
        self.bullet_speed=3.0
        self.alien_speed=1.0
        self.fleet_direction=1 #self.direction为1时表示右移，为-1时表示左移

        #子弹的大小随等级改变
        self.bullet_width=3
        self.bullet_height=15
        #记分
        self.alien_points=10 #击落一个外星人得十分

    def increase_speed(self):
        #提高速度设置
        self.ship_speed*=self.speedup_scale
        self.bullet_speed*=self.speedup_scale
        self.alien_speed*=self.speedup_scale

        self.alien_points=int(self.alien_points*self.score_scale)

    def increase_bullet_level(self):
        #八级以后子弹开始升级
        self.bullet_width*=self.bullet_scale
        self.bullet_height*=self.bullet_scale


        
