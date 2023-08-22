import pygame
import random

BOX_WIDTH = 70
BOX_HEIGHT = 60
NUMBER_SIZE = 40

class NumberBox(pygame.sprite.Sprite):
    def __init__(self, cx, cy):
        super().__init__()
        self.image = pygame.Surface((BOX_WIDTH, BOX_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = (cx, cy)
        self.font = pygame.font.Font(size=NUMBER_SIZE)

        self.is_hit = False
        self.must_prime_num = False
        self.input_active = False

        self.num_text = ''
        self.__n = 0

    def set_number(self, n):
        self.__n = n
        self.num_text = str(n)
    
    def get_number(self):
        return self.__n
    
    def reset(self):
        # self.image.fill("black")
        self.__n = 0
        self.num_text = ''
        self.is_hit = False
    
    def text_input(self, ch):
        if ch >= '0' and ch <= '9' and len(self.num_text) < 2:
            self.num_text += ch
        
    def text_draw(self, text: str):
        textsurf = self.font.render(text, 1, "white")
        w = textsurf.get_width()
        h = textsurf.get_height()
        self.image.blit(textsurf, [BOX_WIDTH/2-w/2, BOX_HEIGHT/2-h/2])
    
    def check_prime_number(self):
        if not self.must_prime_num:
            return True
        # else: must be prime number
        if self.__n <= 1:
            # self.reset()
            return False
        for i in range(2, self.__n):
            if (self.__n % i) == 0:
                # self.reset()
                return False
        return True
    
    def update(self):
        if self.input_active:
            self.image.fill("gray")
            self.text_draw(self.num_text)
            self.__n = int(self.num_text) if self.num_text else 0
        else:
            self.num_text = str(self.__n) if self.__n != 0 else ''
            self.image.fill("black")
            self.text_draw(self.num_text)
            
        if self.is_hit:
            pygame.draw.circle(self.image, "red", (BOX_WIDTH/2, BOX_HEIGHT/2), 23, 2)


GRID_WIDTH = (BOX_WIDTH + 10) * 4
GRID_HEIGHT = (BOX_HEIGHT + 10) * 4

def is_prime_number(n: int) -> bool:
    if n <= 1:
        return False
    for i in range(2, n):
        if (n % i) == 0:
            return False
    return True

class Grid(pygame.sprite.Sprite):
    def __init__(self, cx, cy):
        super().__init__()
        self.image = pygame.Surface((GRID_WIDTH, GRID_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = (cx, cy)
        self.image.set_colorkey("black")      # 隱藏黑色

        self.__chance_count = 8
        self.__is_bingo = False
        self.__numbers = [i for i in range(1, 100)]
        self.__prime_numbers = []
        for n in self.__numbers:
            if is_prime_number(n):
                self.__prime_numbers.append(n)

        self.num_box_group = pygame.sprite.Group()
        self.__grid: list[list[NumberBox]] = [[] for i in range(4)]
        for i in range(4):
            for j in range(4):
                box = NumberBox(cx-GRID_WIDTH/4*1.5+j*GRID_WIDTH/4, cy-GRID_HEIGHT/4*1.5+i*GRID_HEIGHT/4)
                if i == j or (i+j) == 3:
                    box.must_prime_num = True
                self.__grid[i].append(box)
                self.num_box_group.add(box)
    
    def rand_numbers(self):
        prime_list = random.sample(self.__prime_numbers, 8)
        nlist = random.sample(self.__numbers, 16)
        for pn in prime_list:
            if pn in nlist:
                nlist.remove(pn)
        for i in range(4):
            for j in range(4):
                if self.__grid[i][j].must_prime_num:
                    self.__grid[i][j].set_number(prime_list.pop())
                else:
                    self.__grid[i][j].set_number(nlist.pop())

    def draw_number(self):
        num_pool = []
        for i in range(4):
            for j in range(4):
                if not self.__grid[i][j].is_hit:
                    num_pool.append(self.__grid[i][j])
        result = random.choice(num_pool)
        result.is_hit = True
        self.__chance_count -= 1
        self.check_bingo()
    
    def check_numbers(self) -> str:
        exist_num = []
        for i in range(4):
            for box in self.__grid[i]:
                exist_num.append(box.get_number())
        self.image.fill("black")
        # 未填數字
        if exist_num.count(0) > 0:
            return 'unfilled'
        # 不重複
        for i in range(len(exist_num)):
            if exist_num.count(exist_num[i]) > 1:
                y = int(i / 4)
                x = i % 4
                pygame.draw.rect(self.image, "red", (x*(BOX_WIDTH+10), y*(BOX_HEIGHT+10), BOX_WIDTH+10, BOX_HEIGHT+10), 3)
                ind = exist_num.index(exist_num[i], i+1, 16)
                y2 = int(ind / 4)
                x2 = ind % 4
                pygame.draw.rect(self.image, "red", (x2*(BOX_WIDTH+10), y2*(BOX_HEIGHT+10), BOX_WIDTH+10, BOX_HEIGHT+10), 3)
                return 'duplicate'
        # 斜線是質數
        for i in range(4):
            for j in range(4):
                if not self.__grid[i][j].check_prime_number():
                    pygame.draw.rect(self.image, "red", (j*(BOX_WIDTH+10), i*(BOX_HEIGHT+10), BOX_WIDTH+10, BOX_HEIGHT+10), 3)
                    return '({row}, {col}) should be prime number'.format(row=i+1, col=j+1)
        return 'valid'
        
    def check_bingo(self):
        horizontal_bingo_li, vertical_bingo_li = [], []
        diagnoal_bingo, back_diagnoal_bingo = False, False
        left = (BOX_WIDTH+10) / 2
        right = GRID_WIDTH - (BOX_WIDTH+10) / 2
        top = (BOX_HEIGHT+10) / 2
        bottom = GRID_HEIGHT - (BOX_HEIGHT+10) / 2
        if self.__chance_count >= 0 and self.__chance_count <= 4:
            for i in range(4):
                horizontal_bingo = self.__grid[i][0].is_hit and self.__grid[i][1].is_hit and self.__grid[i][2].is_hit and self.__grid[i][3].is_hit
                horizontal_bingo_li.append(horizontal_bingo)
                if horizontal_bingo:
                    pygame.draw.line(self.image, "red", (left, top+i*(BOX_HEIGHT+10)), (right, top+i*(BOX_HEIGHT+10)), 4)
                vertical_bingo = self.__grid[0][i].is_hit and self.__grid[1][i].is_hit and self.__grid[2][i].is_hit and self.__grid[3][i].is_hit
                vertical_bingo_li.append(vertical_bingo)
                if vertical_bingo:
                    pygame.draw.line(self.image, "red", (left+i*(BOX_WIDTH+10), top), (left+i*(BOX_WIDTH+10), bottom), 4)
            diagnoal_bingo = self.__grid[0][0].is_hit and self.__grid[1][1].is_hit and self.__grid[2][2].is_hit and self.__grid[3][3].is_hit
            if diagnoal_bingo:
                pygame.draw.line(self.image, "red", (left, top), (right, bottom), 4)
            back_diagnoal_bingo = self.__grid[0][3].is_hit and self.__grid[1][2].is_hit and self.__grid[2][1].is_hit and self.__grid[3][0].is_hit
            if back_diagnoal_bingo:
                pygame.draw.line(self.image, "red", (right, top), (left, bottom), 4)

        self.__is_bingo = True in horizontal_bingo_li or True in vertical_bingo_li or diagnoal_bingo or back_diagnoal_bingo
        
    def is_bingo(self):
        return self.__is_bingo
    
    def get_remain_chance(self):
        return self.__chance_count
    
    def get_grid_numbers(self) -> list[int]:
        nlist = []
        for i in range(4):
            for box in self.__grid[i]:
                nlist.append(box.get_number())
        return nlist
    
    def get_grid_hits(self) -> list[bool]:
        hlist = []
        for i in range(4):
            for box in self.__grid[i]:
                hlist.append(box.is_hit)
        return hlist
    
    def reset(self):
        self.image.fill("black")
        self.__chance_count = 8
        self.__is_bingo = False
        for i in range(4):
            for box in self.__grid[i]:
                box.reset()


# class NumberMenu(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.image = pygame.Surface((600, 100))
#         self.rect = self.image.get_rect()

