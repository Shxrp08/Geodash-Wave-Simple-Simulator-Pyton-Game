# =========================================================
# WAVE GAME - GEOMETRY DASH STYLE (FINAL PERFECT)
# =========================================================

import pygame
import random

# =========================================================
# INIT
# =========================================================

pygame.init()
WIDTH = 1000
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wave Game - Geometry Dash Style")
clock = pygame.time.Clock()

BLACK = (15, 15, 15)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
RED = (255, 70, 70)
font = pygame.font.SysFont("Arial", 24)

# =========================================================
# HIGH SCORE
# =========================================================

best_score = 0
try:
    with open("highscore.txt", "r") as file:
        data = file.read()
        if data != "":
            best_score = int(data)
except:
    best_score = 0

# =========================================================
# FN BUAT RINTANGAN
# =========================================================

def create_obstacle(gap_size):
    gap_size = int(gap_size) 
    
    # Bikin jarak aman biar ujung lancip ga kepotong layar
    min_center = gap_size // 2 + 50
    max_center = HEIGHT - (gap_size // 2) - 50
    center_y = random.randint(min_center, max_center)

    obstacle = {
        "x": WIDTH + 100,
        "center": center_y,
        "gap": gap_size
    }
    obstacles.append(obstacle)

# =========================================================
# FN GAME OVER
# =========================================================

def game_over(score):
    global best_score
    if int(score) > best_score:
        best_score = int(score)
        with open("highscore.txt", "w") as file:
            file.write(str(best_score))

    waiting = True
    while waiting:
        screen.fill(BLACK)
        text1 = font.render("GAME OVER", True, RED)
        text2 = font.render(f"Score : {int(score)}", True, WHITE)
        text3 = font.render(f"Best : {best_score}", True, CYAN)
        text4 = font.render("Tekan SPACE buat main lg", True, WHITE)

        screen.blit(text1, (WIDTH//2 - 90, 170))
        screen.blit(text2, (WIDTH//2 - 90, 220))
        screen.blit(text3, (WIDTH//2 - 90, 260))
        screen.blit(text4, (WIDTH//2 - 140, 320))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

# =========================================================
# LOOP GAME UTAMA
# =========================================================

while True:
    player_x = 150
    player_y = HEIGHT // 2
    
    wave_speed = 6
    trail = []
    trail_length = 35
    obstacles = []
    spawn_timer = 0
    gap_size = 180
    score = 0
    playing = True

    while playing:
        clock.tick(60)
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        mouse_pressed = pygame.mouse.get_pressed()[0]

        # GERAK WAVE 45 DERAJAT SINKRON
        move_y = wave_speed
        obstacle_speed = wave_speed 

        if mouse_pressed:
            player_y -= move_y
        else:
            player_y += move_y

        if player_y < 0: player_y = 0
        if player_y > HEIGHT: player_y = HEIGHT

        # GESER EKOR KE KIRI
        for i in range(len(trail)):
            trail[i] = (trail[i][0] - obstacle_speed, trail[i][1])

        trail.append((player_x, player_y))
        if len(trail) > trail_length:
            trail.pop(0)

        if len(trail) > 1:
            pygame.draw.lines(screen, CYAN, False, trail, 3)

        # SPAWN RINTANGAN
        spawn_timer += 1
        if spawn_timer >= 75:
            create_obstacle(gap_size)
            spawn_timer = 0

        # UPDATE & GAMBAR RINTANGAN
        for obs in obstacles:
            obs["x"] -= obstacle_speed
            
            top_height = obs["center"] - obs["gap"] // 2
            bottom_y = obs["center"] + obs["gap"] // 2
            bottom_height = HEIGHT - bottom_y

            # SEGITIGA ATAS (Bentuk \/ simetris)
            top_triangle = [
                (obs["x"], 0),
                (obs["x"] + top_height, top_height),
                (obs["x"] + (top_height * 2), 0)
            ]

            # SEGITIGA BAWAH (Bentuk /\ simetris)
            bottom_triangle = [
                (obs["x"], HEIGHT),
                (obs["x"] + bottom_height, bottom_y),
                (obs["x"] + (bottom_height * 2), HEIGHT)
            ]

            pygame.draw.polygon(screen, RED, top_triangle)
            pygame.draw.polygon(screen, RED, bottom_triangle)

            # CEK TABRAKAN ATAS
            if player_x >= obs["x"] and player_x <= obs["x"] + (top_height * 2):
                if player_x <= obs["x"] + top_height:
                    limit_y = player_x - obs["x"] 
                else:
                    limit_y = top_height - (player_x - (obs["x"] + top_height))
                
                if player_y <= limit_y:
                    playing = False

            # CEK TABRAKAN BAWAH
            if player_x >= obs["x"] and player_x <= obs["x"] + (bottom_height * 2):
                if player_x <= obs["x"] + bottom_height:
                    limit_y = HEIGHT - (player_x - obs["x"])
                else:
                    limit_y = bottom_y + (player_x - (obs["x"] + bottom_height))
                
                if player_y >= limit_y:
                    playing = False

            # TAMBAH SCORE
            max_w = max(top_height * 2, bottom_height * 2)
            if player_x > obs["x"] + max_w and not obs.get("scored", False):
                score += 1
                obs["scored"] = True

        # HAPUS RINTANGAN LEWAT
        obstacles = [o for o in obstacles if o["x"] > -500]

        # MAKIN SULIT
        score += 0.02
        wave_speed = 6 + (score / 40)
        gap_size = 180 - (score * 1.5)
        if gap_size < 110:
            gap_size = 110

        # TULISAN SCORE
        score_text = font.render(f"Score : {int(score)}", True, WHITE)
        best_text = font.render(f"Best : {best_score}", True, CYAN)
        screen.blit(score_text, (20, 20))
        screen.blit(best_text, (20, 55))

        pygame.display.update()

    game_over(score)