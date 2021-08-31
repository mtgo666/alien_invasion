#用于跟踪游戏统计信息
class GameStats:
    #跟踪游戏统计信息
    def __init__(self,ai_game) :
        self.settings=ai_game.settings
        self.reset_stats()

        #让游戏刚启动时处于非活动状态
        self.game_active=False

        #任何情况下都不应该重置最高得分
        with open('high_score.txt') as file_object:
            self.high_score=int(file_object.read().rstrip()) #每次从文件中最高得分,要利用rstrip方法去掉换行符

    def reset_stats(self):
        #初始化在游戏运行期间可能变化的统计信息
        self.ships_left=self.settings.ship_limit
        self.score=0 #得分
        self.level=1 #等级