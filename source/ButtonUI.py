import pygame

class ButtonUI(pygame.sprite.Sprite):
    def __init__(self, cx, cy, name, width, height, fontsize=40, color = "white"):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.center = (cx, cy)

        self.font = pygame.font.Font(size=fontsize)
        textsurf = self.font.render(name, 1, color)
        w = textsurf.get_width()
        h = textsurf.get_height()
        self.image.blit(textsurf, [width/2-w/2, height/2-h/2])

class PlayButton(ButtonUI):
    def __init__(self, cx, cy):
        super().__init__(cx, cy, 'Play', 100, 50)

class RestartButton(ButtonUI):
    def __init__(self, cx, cy):
        super().__init__(cx, cy, 'Restart', 130, 50)

class RandomButton(ButtonUI):
    def __init__(self, cx, cy):
        super().__init__(cx, cy, 'Random', 130, 50)
    
class LeaderboardButton(ButtonUI):
    def __init__(self, cx, cy):
        super().__init__(cx, cy, 'Leaderboard', 150, 50, 30)
