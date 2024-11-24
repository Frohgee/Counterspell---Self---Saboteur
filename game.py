import pygame
import sys
import random
import math

#STARTS HERE
pygame.init()
pygame.display.set_caption("Self-Saboteur")

#initialize window dimensions 
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#player settings
player_width = 40
player_height = 40
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = 600 - player_height
player_speed = 12

#Loading background music
background_music = pygame.mixer.Sound('Brianskibmusic.wav')

#looping sound
background_music.play(loops=-1)

#enemy settings
enemy_width = 50
enemy_height = 60
enemy_x = 400
enemy_y = 400
enemy_speed = 8

#colours
RED = (255, 0, 0)
BLUE = (0,0,225)
WHITE = (255,255,255)
BLACK = (0,0,0)

#creating elements
player = pygame.Rect((player_x, player_y, player_width, player_height))
enemy = pygame.Rect((enemy_x, enemy_y, enemy_width, enemy_height))

#fps 
fps = 60
clock = pygame.time.Clock()

last_shot_time = 0  

#bullet setup
bullets = []
bullet_speed = 15
bullet_width, bullet_height = 40, 40
bullet_creation_times = {}

#loading/processing images
player_image = pygame.image.load('sprite.png')
player_image = pygame.transform.scale(player_image, (player_width, player_height))

bullet_image = pygame.image.load('blueball.png')
bullet_image = pygame.transform.scale(bullet_image, (40, 40))

enemy_image = pygame.image.load('oi.png')
enemy_image = pygame.transform.scale(enemy_image, (enemy_width, enemy_height))

direction_change_time = 0  
direction_duration = 500  
directions = ['left', 'right', 'up', 'down']  
current_direction = random.choice(directions)  

# def start(screen):
game_over = False

MAX_HEALTH = 3
health = MAX_HEALTH
score = 0

#For one bounce collision intilization
for bullet in bullets:
    bullet[3] = True

def start_screen():
    global rules
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 50)

    title_text = font.render("Self-Saboteur", True, WHITE)

    start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50)
    start_text = small_font.render("START", True, BLACK)

    while True:
        screen.fill(BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 150))

        pygame.draw.rect(screen, (0,250,0), start_button)
        screen.blit(start_text, (start_button.centerx - start_text.get_width() // 2, start_button.centery - start_text.get_height() // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):  
                    return True 
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  
                    return True

#prompts an end screen once the player dies (runs out oflives)
def end_screen(screen):
    global game_over, health, score
    game_over = True

    #stopping background music
    background_music.stop()

    #playing game over
    play_music('game over.mp3')

    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 50)
    game_over_text = font.render("Game Over", True, RED)
    score_text = font.render(f"Score: {score}", True, WHITE)
    restart_text = small_font.render("Space to Restart", True, WHITE)
    quit_text = small_font.render("Quit", True, WHITE)
    quit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70, 200, 50)

    while True:
        screen.fill((0, 0, 0))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 200))

        pygame.draw.rect(screen, RED, quit_button)
        screen.blit(restart_text, (210, 400))
        screen.blit(quit_text, (quit_button.centerx - quit_text.get_width() // 2, quit_button.centery - quit_text.get_height() // 2))
        screen.blit(score_text, (SCREEN_WIDTH //2 - score_text.get_width() // 2, 300))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_over:
                    bullets.clear()
                    health = 3
                    game_over = False
                    #looping sound
                    background_music.play(loops=-1)
                    #resetting score
                    score = 0
                    return  
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

#determines whether or not the player's mouse is at the bottom  
def bottom_shooting(player_x, player_y, mouse_x, mouse_y):
    dx = mouse_x - (player_x + player_width // 2)
    dy = mouse_y - (player_y + player_height // 2)

    return dy > 0  

#creates the bullet
def shoot():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    #collision
    bullet_enemy_bounce_collision = True
    dx = mouse_x - player_x
    dy = mouse_y - player_y
    distance = math.sqrt(dx**2 + dy**2)  
    if distance != 0:
        dx /= distance  
        dy /= distance  

    global bullets
    bullet_x = (player_x + player_width // 2 - bullet_width // 2)
    if bottom_shooting(player_x, player_y, mouse_x, mouse_y):
        bullet_y = (player_y) +40
    else:
        bullet_y = (player_y) - 40

    bullets.append([pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height), dx, dy, bullet_enemy_bounce_collision])
    #plays music every time a bullet is created
    play_music('laser.mp3')


def random_rectangle():
    max_width = SCREEN_WIDTH - 100  
    max_height = SCREEN_HEIGHT - 250   
    width = random.randint(200, max_width)  
    height = random.randint(200, max_height)  
    
    x = random.randint(50, SCREEN_WIDTH - width - 50)
    y = random.randint(50, SCREEN_HEIGHT - height - 50)
    
    return pygame.Rect(x, y, width, height)

def spawn_player_in_center_of_rectangle(rectangle):
    center_x = rectangle.centerx
    center_y = rectangle.centery
    
    return pygame.Rect(center_x, center_y, player_width, player_height)

def spawn_enemy_in_top_of_rectangle(rectangle):
    center_x = rectangle.centerx
    bottom_y = rectangle.top
    
    return pygame.Rect(center_x, bottom_y, enemy_width, enemy_height)


timer = 10
CHANGE_SHAPE = pygame.USEREVENT + 1
pygame.time.set_timer(CHANGE_SHAPE, 1000)  

last_damage_time = 0

def move_enemy(enemy):
    global direction_change_time, current_direction

    current_time = pygame.time.get_ticks()  

    if current_time - direction_change_time >= direction_duration:
        current_direction = random.choice(directions)  #
        direction_change_time = current_time  

    if current_direction == 'left':
        enemy.x -= enemy_speed  
    elif current_direction == 'right':
        enemy.x += enemy_speed  
    elif current_direction == 'up':
        enemy.y -= enemy_speed  
    elif current_direction == 'down':
        enemy.y += enemy_speed  

    if enemy.left <= current_rectangle.left:
        enemy.x = current_rectangle.left  
        current_direction = random.choice([direction for direction in directions if direction != 'left']) 

    if enemy.right >= current_rectangle.right:
        enemy.x = current_rectangle.right - enemy.width  
        current_direction = random.choice([direction for direction in directions if direction != 'right']) 

    if enemy.top <= current_rectangle.top:
        enemy.y = current_rectangle.top  
        current_direction = random.choice([direction for direction in directions if direction != 'up'])  

    if enemy.bottom >= current_rectangle.bottom:
        enemy.y = current_rectangle.bottom - enemy.height 
        current_direction = random.choice([direction for direction in directions if direction != 'down'])  

def play_music(file):
    effect = pygame.mixer.Sound(file)
    effect.play()

#start_screen(screen)
current_rectangle = random_rectangle()
player = spawn_player_in_center_of_rectangle(current_rectangle)
player_x, player_y = player.topleft  

enemy = spawn_enemy_in_top_of_rectangle(current_rectangle)

def game_loop():
    running = True
    while running:
        global current_rectangle, last_shot_time, player, player_x, player_y, enemy, timer
        clock.tick(fps)
        screen.fill((0,0,0))

        pygame.draw.rect(screen, WHITE, current_rectangle, 2)
            
        current_time = pygame.time.get_ticks()  
        if current_time - last_shot_time >= 500: 
            shoot()
            last_shot_time = current_time  

        def bluebullet_hit(bullet):
            global health

            for bullet in bullets[:]: 
                    if bullet[0].colliderect(player):
                            bullets.remove(bullet) 
                            health -= 1  
                    if health <= 0:
                        #play hurt sounds
                        play_music('Brain Bust (1).mp3')
                        end_screen(screen)
                

        def player_enemy_collision(player, enemy):
            global health 

            if player.colliderect(enemy):
                health -= 1  
                if health <= 0:
                    #play hurt sounds
                    play_music('Brain Bust (1).mp3')
                    end_screen(screen)
        
        def bullet_enemy_collision(bullets, enemy):
            global score
            for bullet in bullets[:]: 
                if bullet[0].colliderect(enemy) and bullet[3] == True:  
                    bullets.remove(bullet)  
                    score += 10

        def player_enemy_collision(player, enemy):
            global health, last_damage_time

            if player.colliderect(enemy) and current_time - last_damage_time > 1000:
                health -= 1  
                last_damage_time = current_time
                if health <= 0:
                    end_screen(screen)

        for bullet in bullets[:]:
            bullet[0].x += bullet[1] * bullet_speed  #movex
            bullet[0].y += bullet[2] * bullet_speed  #movey

            if bullet[0].left <= current_rectangle.left:
                bullet[0].x = current_rectangle.left + 1
                bullet[1] -= bullet[1] * 2
                bullet[3] = False

            if bullet[0].right >= current_rectangle.right:
                bullet[0].x = current_rectangle.right - bullet[0].width - 1  
                bullet[1] = -bullet[1] 
                bullet[3] = False

            if bullet[0].top <= current_rectangle.top:
                bullet[0].y = current_rectangle.top + 1  
                bullet[2] = -bullet[2]  
                bullet[3] = False

            if bullet[0].bottom >= current_rectangle.bottom:
                bullet[0].y = current_rectangle.bottom - bullet[0].height - 1  
                bullet[2] = -bullet[2]
                bullet[3] = False

            bluebullet_hit(bullet) 
            
            screen.blit(bullet_image, bullet[0].topleft)

            if not screen.get_rect().colliderect(bullet[0]):
                bullets.remove(bullet)

        for i in range(health):
            pygame.draw.rect(screen, (0, 255, 0), (10 + i * 40, 10, 30, 10))  
                    

        key = pygame.key.get_pressed()

        pygame.draw.rect(screen, WHITE, current_rectangle, 2)

        if key[pygame.K_w] and player.top > current_rectangle.top:
            player_y -= player_speed
        if key[pygame.K_a] and player.left > current_rectangle.left:
            player_x -= player_speed
        if key[pygame.K_s] and player.bottom < current_rectangle.bottom:
            player_y += player_speed
        if key[pygame.K_d] and player.right < current_rectangle.right:
            player_x += player_speed

        player.topleft = (player_x, player_y)
        screen.blit(player_image, (player_x, player_y)) 

        move_enemy(enemy)

        screen.blit(enemy_image, (enemy.x, enemy.y)) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == CHANGE_SHAPE:
                timer -= 1
                if timer <= 0:
                    bullets.clear()
                    current_rectangle = random_rectangle()
                    player = spawn_player_in_center_of_rectangle(current_rectangle)  
                    player_x, player_y = player.topleft  
                    enemy = spawn_enemy_in_top_of_rectangle(current_rectangle)
                    enemy_x, enemy_y = enemy.topleft
                    x_direction = random.choice([-1, 1])
                    y_direction = random.choice([-1, 1])
                    timer = 10 # Reset to 30 seconds
        
        
        bullet_enemy_collision(bullets, enemy)
        
        player_enemy_collision(player, enemy)

        font = pygame.font.Font(None, 36)
        timer_text = font.render(f"Time Until Shape Change: {timer}s", True, WHITE)
        screen.blit(timer_text, (SCREEN_WIDTH - 365, 15))

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text,(SCREEN_WIDTH - 365, 50))

        pygame.display.update()

    pygame.quit()

def main():
    while True:
        if start_screen():  # If space or the start button is pressed, start the game
            game_loop()  # Enter the game loop
        else:
            break  # Exit if the user quits or closes the window

main()