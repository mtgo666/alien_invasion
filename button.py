import pygame.font

class Button:
    def __init__(self,ai_game,msg):
        #初始化按钮的属性
        self.screen=ai_game.screen
        self.screen_rect=self.screen.get_rect()

        #设置按钮的尺寸和其他属性
        self.width,self.heigt=200,50
        self.button_color=(0,255,0)
        self.text_color=(255,255,255)
        self.font=pygame.font.SysFont("arial",48)

        #创建按钮的rect对象，并使其居中
        self.rect=pygame.Rect(0,0,self.width,self.heigt)
        self.rect.center=self.screen_rect.center

        #按钮的标签只需创建一次
        self._prep_msg(msg) #将显示的字符串渲染成图像

    def _prep_msg(self,msg):
        #将msg渲染成图像，并使其在按钮上居中
        self.msg_image=self.font.render(msg,True,self.text_color,self.button_color)
        self.msg_image_rect=self.msg_image.get_rect()
        self.msg_image_rect.center=self.rect.center #让文本图像在按钮上居中

    def draw_button(self):
        #绘制一个用颜色填充的按钮，再绘制文本
        self.screen.fill(self.button_color,self.rect)  #在屏幕上绘制表示按钮的矩形
        self.screen.blit(self.msg_image,self.msg_image_rect)

