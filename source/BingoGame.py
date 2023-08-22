import pygame
from enum import Enum
from Grid import *
from ButtonUI import *
from PlayerHistory import *

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

class GameState(Enum):
    SETTING_NUMBER = 1
    PLAYING = 2
    END = 3
    LEADERBOARD = 4

state = GameState.SETTING_NUMBER
state_buffer = []

# pygame setup
pygame.init()
pygame.display.set_caption('BINGO')
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
main_font = pygame.font.Font(size=80)
hint_font = pygame.font.Font(size=28)
hint_surf = None
rule_font = pygame.font.Font(size=20)

game_recorder = PlayerHistory('Guest1')
round_count = game_recorder.get_index()

all_sprites = pygame.sprite.Group()
grid = Grid(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
# grid.rand_numbers()
all_sprites.add(grid)

play_button = PlayButton(1280/2-100, 720-150)
all_sprites.add(play_button)

random_button = RandomButton(1280/2+100, 720-150)
all_sprites.add(random_button)

restart_button = RestartButton(1280/2+300, WINDOW_HEIGHT/2)
all_sprites.add(restart_button)

leaderboard_button = LeaderboardButton(1280/2+300, WINDOW_HEIGHT/2-105)
all_sprites.add(leaderboard_button)

leaderboard = LeaderboardUI(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, game_recorder)
all_sprites.add(leaderboard)
while running:
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    rule_text1 = rule_font.render('Rules:', 1, "white")
    rule_text2 = rule_font.render('1. Choose 16 numbers between 1 and 99.', 1, "white")
    rule_text3 = rule_font.render('2. Diagonal should be prime number.', 1, "white")
    rule_text4 = rule_font.render('3. You have 8 chances to draw.', 1, "white")
    rule_text5 = rule_font.render('Click "Random" to auto fill in. Click "Play" to start drawing.', 1, "white")
    screen.blit(rule_text1, (10, 100))
    screen.blit(rule_text2, (10, 100+rule_text1.get_height()))
    screen.blit(rule_text3, (10, 100+rule_text1.get_height()*2))
    screen.blit(rule_text4, (10, 100+rule_text1.get_height()*3))
    screen.blit(rule_text5, (10, 100+rule_text1.get_height()*4))

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if state == GameState.SETTING_NUMBER:
            # left click on Number Box
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                num_box: NumberBox
                for num_box in grid.num_box_group.sprites():
                    if num_box.rect.collidepoint(event.pos):
                        num_box.input_active = True
                    else:
                        num_box.input_active = False
                # Set numbers by computer
                if random_button.rect.collidepoint(event.pos):
                    grid.rand_numbers()
            # type in and set number 
            if event.type == pygame.KEYDOWN:
                num_box: NumberBox
                for num_box in grid.num_box_group.sprites():
                    if num_box.input_active:
                        if event.key == pygame.K_BACKSPACE:
                            num_box.num_text = num_box.num_text[0:-1]
                        elif event.key == pygame.K_RETURN:
                            num_box.input_active = False
                        else:
                            num_box.text_input(event.unicode)
        if state == GameState.LEADERBOARD:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not leaderboard.rect.collidepoint(event.pos) or leaderboard.get_back_rect().collidepoint(event.pos):
                    state = state_buffer.pop()
                    leaderboard.is_open = False

        # Change state object
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Click Play button
            if play_button.rect.collidepoint(event.pos):
                if state == GameState.SETTING_NUMBER:
                    grid_state = grid.check_numbers()
                    if grid_state == 'valid':
                        hint_surf = None
                        round_count = game_recorder.get_index()
                        state = GameState.PLAYING
                    elif grid_state == 'unfilled':
                        hint_surf = hint_font.render('NOTICE: Number should not be blank', 1, "red")
                    elif grid_state == 'duplicate':
                        hint_surf = hint_font.render('NOTICE: Number should be distinct', 1, "red")
                    else:
                        hint_surf = hint_font.render('NOTICE: {hint}'.format(hint=grid_state), 1, "red")
                if state == GameState.PLAYING and grid.get_remain_chance() > 0:
                    grid.draw_number()
            # Click Restart button
            if restart_button.rect.collidepoint(event.pos):
                grid.reset()
                state = GameState.SETTING_NUMBER
            # Click leaderboard
            if leaderboard_button.rect.collidepoint(event.pos):
                state_buffer.append(state)
                state = GameState.LEADERBOARD
                leaderboard.is_open = True



    # RENDER YOUR GAME HERE

    if state == GameState.PLAYING:
        if grid.is_bingo() or grid.get_remain_chance() == 0:
            state = GameState.END
    
    if state == GameState.END:
        if grid.is_bingo():
            win_surf = main_font.render('BINGO!', 1, 'yellow')
            w = win_surf.get_width()
            screen.blit(win_surf, (640 - w/2, 100))
        elif grid.get_remain_chance() == 0:
            fail_surf = main_font.render('FAIL', 1, "gray")
            w = fail_surf.get_width()
            screen.blit(fail_surf, (640 - w/2, 100))
        if round_count == game_recorder.get_index():
            result = 1 if grid.is_bingo() else 0
            numbers = grid.get_grid_numbers()
            hits = grid.get_grid_hits()
            chances = grid.get_remain_chance()
            game_recorder.store_record(result, numbers, hits, chances)

    grid.num_box_group.update()
    all_sprites.update()
    grid.num_box_group.draw(screen)
    all_sprites.draw(screen)
    if hint_surf:
        screen.blit(hint_surf, (10, 690))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()