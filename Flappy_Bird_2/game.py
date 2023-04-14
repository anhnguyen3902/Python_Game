from operator import truediv
import pygame, sys, random
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)

#tao ham cho tro choi
def update_lives(live):
    for i in range(live):
        screen.blit(live_surface, (10 + i * (live_surface.get_width() + 5), 10))
def draw_floor():
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos+432, 650))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos - 700))
    return bottom_pipe, top_pipe


def move_pipe(pipes):
    for pipe in pipes :
        pipe.centerx -= 2
    return pipes


def draw_pipe(pipes) :
    for pipe in pipes :
        if pipe.bottom >= 600 :
         screen.blit(pipe_surface, pipe)
        else :
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement*3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)), True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216, 100))
        screen.blit(score_surface, score_rect)
    
        high_score_surface = game_font. render(f'High Score: {int(high_score)}', True,(255,255,255))
        high_score_rect = score_surface.get_rect(center = (175, 630))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


def draw_menu():
    # Tạo chọn map
    map_text = game_font.render('Select Map:', True, (255, 255, 255))
    map_rect = map_text.get_rect(center=(216, 200))
    screen.blit(map_text, map_rect)

    map1_text = game_font.render('Map 1', True, (255, 255, 255))
    map1_rect = map1_text.get_rect(center=(150, 300))
    screen.blit(map1_text, map1_rect)

    map2_text = game_font.render('Map 2', True, (255, 255, 255))
    map2_rect = map2_text.get_rect(center=(282, 300))
    screen.blit(map2_text, map2_rect)

    # Tạo chọn bird
    bird_text = game_font.render('Select Bird:', True, (255, 255, 255))
    bird_rect = bird_text.get_rect(center=(216, 400))
    screen.blit(bird_text, bird_rect)

    bird1_text = game_font.render('Bird 1', True, (255, 255, 255))
    bird1_rect = bird1_text.get_rect(center=(150, 500))
    screen.blit(bird1_text, bird1_rect)

    bird2_text = game_font.render('Bird 2', True, (255, 255, 255))
    bird2_rect = bird2_text.get_rect(center=(282, 500))
    screen.blit(bird2_text, bird2_rect)

    screen.blit(bird, bird.get_rect(center=(220, 570)))


def handle_menu_event(event):
    global bird_down, bird_mid, bird_list, bg, pipe_surface, live_surface

    new_map = current_map
    new_bird = current_bird
    new_pipe = current_pipe

    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()

        # Chọn map
        if 100 <= mouse_pos[0] <= 200 and 250 <= mouse_pos[1] <= 350:
            new_map = 'night'
            new_pipe = 'green'
            if new_bird == 'bluebird' or new_bird == 'greenbird':
                new_bird = 'yellowbird'
        elif 232 <= mouse_pos[0] <= 332 and 250 <= mouse_pos[1] <= 350:
            new_map = 'day'
            new_pipe = 'gray'
            if new_bird == 'yellowbird' or new_bird == 'whitebird':
                new_bird = 'bluebird'

        # Chọn bird
        if new_map == 'night':
            if 100 <= mouse_pos[0] <= 200 and 450 <= mouse_pos[1] <= 550:
                new_bird = 'yellowbird'
            elif 232 <= mouse_pos[0] <= 332 and 450 <= mouse_pos[1] <= 550:
                new_bird = 'whitebird'
        elif new_map == 'day':
            if 100 <= mouse_pos[0] <= 200 and 450 <= mouse_pos[1] <= 550:
                new_bird = 'bluebird'
            elif 232 <= mouse_pos[0] <= 332 and 450 <= mouse_pos[1] <= 550:
                new_bird = 'greenbird'

        # set lại chim
        bird_down = pygame.transform.scale2x(pygame.image.load(f'assets/{new_bird}-downflap.png'))
        bird_mid = pygame.transform.scale2x(pygame.image.load(f'assets/{new_bird}-midflap.png'))
        bird_up = pygame.transform.scale2x(pygame.image.load(f'assets/{new_bird}-upflap.png'))
        live_surface= pygame.image.load(f'assets/{new_bird}-midflap.png')
        bird_list = [bird_down, bird_mid, bird_up]

        # set lại background
        bg = pygame.image.load(f'assets/background-{new_map}.png').convert()
        bg = pygame.transform.scale2x(bg)

        # set lại ống
        pipe_surface = pygame.image.load(f'assets/pipe-{new_pipe}.png').convert()
        pipe_surface = pygame.transform.scale2x(pipe_surface)

    return new_map, new_bird, new_pipe


pygame.init()
screen = pygame.display.set_mode((432, 768))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 40)
#tao bien cua tro choi
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

current_map = 'night'
current_bird = 'whitebird'
current_pipe = 'green'
#chèn background
bg = pygame.image.load(f'assets/background-{current_map}.png').convert()
bg = pygame.transform.scale2x(bg)
# chèn âm thanh
flap_sound = pygame.mixer.Sound(f'sfx_wing.wav')
hit_sound = pygame.mixer.Sound(f'sfx_hit.wav')
score_sound= pygame.mixer.Sound(f'sfx_point.wav')
score_sound_countdown=100
#chèn sàn
floor = pygame.image.load('assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0
# chèn mạng của chim
live_surface = pygame.image.load(f'assets/{current_bird}-midflap.png').convert_alpha()
live =3
#tạo chim
bird_down = pygame.transform.scale2x(pygame.image.load(f'assets/{current_bird}-downflap.png'))
bird_mid = pygame.transform.scale2x(pygame.image.load(f'assets/{current_bird}-midflap.png'))
bird_up = pygame.transform.scale2x(pygame.image.load(f'assets/{current_bird}-upflap.png'))
bird_list = [bird_down, bird_mid, bird_up]
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center = (100, 384))
#tao timer cho bird
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, 200)

#tạo ống
pipe_surface = pygame.image.load(f'assets/pipe-{current_pipe}.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

# tao timer
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)
pipe_height = [300, 400, 500]
#tao man hinh ket thuc
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png')).convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (216, 384))


#while loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = -1
                bird_movement = -5
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False and live !=0 :
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 384)
                bird_movement = 0
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                live =3
                pipe_list.clear()
                bird_rect.center = (100, 384)
                bird_movement = 0
                score = 0
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        
        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else :
                bird_index = 0
            bird, bird_rect = bird_animation()


    screen.blit(bg, (0, 0))
    update_lives(live)
    if game_active and live > 0:
        for pipe in pipe_list:
            if bird_rect.colliderect(pipe):
                live -= 1
                hit_sound.play()
                game_active = False
        if bird_rect.top <= -75 or bird_rect.bottom >= 650:
            live -= 1
            hit_sound.play()
            game_active = False
        update_lives(live)
        # chim
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        # ong
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01
        score_sound_countdown-=1
        if score_sound_countdown <=0:
            score_sound.play()
            score_sound_countdown=100
        score_display('main game')

    elif game_active == False and live>0:
        screen.blit(game_over_surface, game_over_rect)
    else :
        high_score = update_score(score, high_score)
        draw_menu()
        current_map, current_bird, current_pipe = handle_menu_event(event)
        score_display('game_over')
    #san
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432 :
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(100)
