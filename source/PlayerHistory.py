import pygame

class PlayerHistory:
    def __init__(self, playername, index = 1):
        self.__player = playername
        self.__index = index
        self.__game_result = dict() # key: index, value: bingo/fail/unfinished, 1/0/-1
        self.__grid_numbers = dict() # key: index, value: list[list[int]] 4*4
        self.__hits = dict() # key: index, value = list[list[bool]] 4*4
        self.__remain_chance = dict() # key: index, value: 0~8
    
    def get_player_name(self):
        return self.__player
    
    def get_index(self):
        return self.__index

    def __set_game_result(self, index, value):
        self.__game_result[index] = value

    def __set_grid_numbers(self, index, value):
        self.__grid_numbers[index] = value
    
    def __set_hits(self, index, value):
        self.__hits[index] = value

    def __set_remain_chance(self, index, value):
        self.__remain_chance[index] = value

    def store_record(self, result: int, numbers: list[int], hits: list[bool], chances: int):
        self.__set_game_result(self.__index, result)
        self.__set_grid_numbers(self.__index, numbers)
        self.__set_hits(self.__index, hits)
        self.__set_remain_chance(self.__index, chances)
        self.__index += 1
    
    def get_game_result(self, last:int = 20) -> list:
        values = self.__game_result.values()
        values_li = list(values)
        values_li.reverse()
        return values_li[0:last]
    
    def get_grid_numbers(self, last:int = 20) -> list:
        values = self.__grid_numbers.values()
        values_li = list(values)
        values_li.reverse()
        return values_li[0:last]

    def get_hits(self, last:int = 20) -> list:
        values = self.__hits.values()
        values_li = list(values)
        values_li.reverse()
        return values_li[0:last]
    
    def get_remain_chance(self, last:int = 20) -> list:
        values = self.__remain_chance.values()
        values_li = list(values)
        values_li.reverse()
        return values_li[0:last]
    
    def get_win_lose(self):
        values = self.__game_result.values()
        values_li = list(values)
        wins = values_li.count(1)
        loses = values_li.count(0)
        return (wins, loses)

class LeaderboardUI(pygame.sprite.Sprite):
    def __init__(self, cx, cy, history: PlayerHistory):
        super().__init__()
        self.image = pygame.Surface((500, 500))
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.center = (cx, cy)
        self.font = pygame.font.Font(size=40)

        self.is_open = False

        self.__history = history

        self.__title_surf = self.font.render('Leaderboard', 1, "purple")
        self.__back_button = self.font.render('BACK', 1, "purple")
    
    def get_back_rect(self):
        w = self.__back_button.get_width()
        h = self.__back_button.get_height()
        return pygame.Rect(self.rect.left+400, self.rect.top+20, w, h)
    
    def update(self):
        if self.is_open:
            self.image.fill("white")
            playername = self.font.render(self.__history.get_player_name(), 1, "purple")
            (wins, loses) = self.__history.get_win_lose()
            result = self.font.render('{w} Bingo/{l} Fail'.format(w=wins, l=loses), 1, "purple")
            result_w = result.get_width()
            
            self.image.blit(self.__title_surf, (50, 50))
            self.image.blit(self.__back_button, (400, 20))
            pygame.draw.line(self.image, "purple", (50, 100), (450, 100), 3)
            self.image.blit(playername, (60, 120))
            self.image.blit(result, (450-result_w, 120))
        else:
            self.image.fill("black")