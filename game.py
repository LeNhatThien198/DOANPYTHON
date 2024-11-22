import pygame, sys, random
#Tạo hàm cho trò chơi
def draw_base():
    screen.blit(base,(base_x_pos,650))
    screen.blit(base,(base_x_pos+432,650))
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    gap_size = 680
    bottom_pipe = pipe_surface.get_rect(midtop =(500,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop =(500,random_pipe_pos-gap_size))
    return bottom_pipe, top_pipe
def move_pipe(pipes):
	for pipe in pipes :
		pipe.centerx -= 5
	return pipes
def remove_pipes(pipes): #xoá các ông không còn trong khung hình: Xóa để tránh lãng phí bộ nhớ
    return [pipe for pipe in pipes if pipe.right > 0]
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600 : 
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        hit_sound.play()
        return False
    return True 
def rotate_bird(bird1):
	new_bird = pygame.transform.rotozoom(bird1,-bird_movement*3,1)
	return new_bird
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird, new_bird_rect
def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,70))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,70))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (216,240))
        screen.blit(high_score_surface,high_score_rect)
def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score
def update_score_on_pipe(pipes, bird):
    for pipe in pipes:
         if 95 < pipe.centerx < 105 and pipe not in scored_pipes:# Chim vừa vượt qua ống này nhưng ống không nằm trong danh sách đã cộng điểm
            scored_pipes.append(pipe) # Thêm ống vào danh sách các ống đã vượt qua để tính điểm chính xác
            score_sound.play() # Âm thanh ghi điểm sẽ phát ra khi chim vượt qua ống
            return 1
    return 0

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
screen= pygame.display.set_mode((432,768))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',35)
#Tạo các biến cho trò chơi
gravity = 0.20
bird_movement = 0
game_active = True
score = 0
high_score = 0
#chèn background
bg = pygame.image.load('assets/background-day.png').convert()
bg = pygame.transform.scale2x(bg)
#chèn sàn
base = pygame.image.load('assets/base.png').convert()
base = pygame.transform.scale2x(base)
base_x_pos = 0
#tạo chim
bird_down = pygame.transform.scale2x(pygame.image.load('assets/downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('assets/midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('assets/upflap.png').convert_alpha())
bird_list= [bird_down,bird_mid,bird_up] #0 1 2
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center = (100,384))

#tạo timer cho bird
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap,300)
#tạo ống
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list =[]
#tạo timer
spawnpipe= pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1500)
pipe_height = [200,300,400]
#Tạo màn hình kết thúc
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(216,360))
#Chèn âm thanh
flap_sound = pygame.mixer.Sound('audio/wing.wav')
swoosh_sound = pygame.mixer.Sound('audio/swoosh.wav')
hit_sound = pygame.mixer.Sound('audio/hit.wav')
score_sound = pygame.mixer.Sound('audio/point.wav')
# Chèn nhạc nền
pygame.mixer.music.load('audio/Flappy Bird Theme Song.mp3') 
pygame.mixer.music.play(loops=-1, start=0.0)
# Khởi tạo danh sách ống đã được tính điểm
scored_pipes = [] 

#while loop của trò chơi
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement =-6
                flap_sound.play()
                swoosh_sound.play()
            if event.key == pygame.K_SPACE and game_active==False:
                game_active = True 
                pipe_list.clear() # Xóa tất cả các đường ống trong pipe_list khi bắt đầu lại trò chơi
                bird_rect.center = (100,384)
                bird_movement = 0 
                score = 0
                pygame.mixer.music.play(loops=-1, start=0.0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Nếu là chuột trái
                if game_active:
                    bird_movement = -6 # Chim đập cánh
                    flap_sound.play()
                    swoosh_sound.play()
                else: 
                    game_active = True
                    pipe_list.clear()  # Xóa tất cả các đường ống trong pipe_list khi bắt đầu lại trò chơi
                    bird_rect.center = (100, 384)  # Đặt lại vị trí cho chim
                    bird_movement = 0  # Đặt lại chuyển động cho chim
                    score = 0 
                    pygame.mixer.music.play(loops=-1, start=0.0)
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index =0 
            bird, bird_rect = bird_animation()    
                         
    screen.blit(bg,(0,0))
    if game_active:
        #chim
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)       
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_active= check_collision(pipe_list)
        #ống
        pipe_list = move_pipe(pipe_list)
        pipe_list = remove_pipes(pipe_list)
        draw_pipe(pipe_list)
        score += update_score_on_pipe(pipe_list, bird_rect)
        score_display('main game')
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')
        pygame.mixer.music.stop()
        

       
    #sàn
    base_x_pos -= 1
    draw_base()
    if base_x_pos <= -432:
        base_x_pos =0
    
    pygame.display.update()
    clock.tick(85)
