import pygame 
import os
import random
from moviepy.editor import VideoFileClip
import json
# 變數
WIDTH = 700
HEIGHT = 600
FPS = 45
RED = (255,0,0)
WHILT = (255, 255, 255)
BALCK = (0, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 130, 71)
hg_score = {
  "best_score": 0
}

with open('easy.json', 'r') as data:
    hg_score = json.load(data)

def save_record():
    with open('easy.json', 'w') as data:
        json.dump(hg_score, data, indent = 4)
score = 0

#螢幕設計
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DETERMINATION Demo")
clock = pygame.time.Clock()
pygame.mixer.init()

# image
player_img = pygame.image.load(os.path.join("image", "determination.png")).convert()
rock_img = pygame.image.load(os.path.join("image", "rock.png")).convert()
background_img = pygame.image.load(os.path.join("image", "background.png")).convert()

gif_path = 'image/undyning undyne.gif'
clip = VideoFileClip(gif_path)
frames = clip.iter_frames()

pygame_frames = []
for frame in frames:
    pygame_frame = pygame.image.fromstring(frame.tobytes(), clip.size, "RGB")
    pygame_frames.append(pygame_frame)


# musiec
rock_sound = pygame.mixer.Sound(os.path.join("sound", "spear.wav"))
rock_sound.set_volume(0.2)

font_name = os.path.join("font", "MonsterFriendFore.ttf")
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, RED)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def draw_init():
    screen.blit(background_img, (0, 0))
    draw_text(screen, "DETERMINATION_Easy", 30, WIDTH/2, HEIGHT/4) 
    draw_text(screen, "Press \"Z\" to Start", 18, WIDTH/2, HEIGHT-200)
    draw_text(screen, "Press \"X\" to Back", 18, WIDTH/2, HEIGHT*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_z:
                    waiting = False
                    return False

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (20, 20))
        self.rect = self.image.get_rect()
        self.radius = 3
        # pygame.draw.circle(self.image, GREEN, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.y = 450
    
    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += 5
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= 5
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += 5
        if key_pressed[pygame.K_UP]:
            self.rect.y -= 5
        
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH    
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = rock_img
        self.image = pygame.transform.scale(rock_img, (12, 30))
        self.image.set_colorkey(WHILT)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-200, -40)
        self.speedy = random.randrange(3, 5)
        self.speedx = 0 #random.randrange(-3, 4)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -90)
            self.speedy = random.randrange(6, 15)
            self.speedx =  0 #random.randrange(-3, 4)
            rock_sound.play()
            



all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
rocks = pygame.sprite.Group()
for i in range(8):
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

getTicksLastFrame = 0
total_tick = 0
show_init = True
frame_index = 0
running = True
reset = True
while running:
    t = pygame.time.get_ticks()
    # deltaTime in seconds.
    deltaTime = (t - getTicksLastFrame) / 1000.0
    getTicksLastFrame = t
    if not show_init:
        total_tick += 1
        score += deltaTime
        print(score)
    if show_init:
        if score > hg_score["best_score"]:
            hg_score["best_score"] = score
            save_record()
        close = draw_init()
        if close:
            break
        show_init = False
        all_sprites = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        rocks = pygame.sprite.Group()
        for i in range(30):
            r = Rock()
            all_sprites.add(r)
            rocks.add(r)

    clock.tick(FPS)
    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_x:
                show_init = True
                score = 0
                rock_sound.stop()
            if event.key == pygame.K_z:
                score = 0

    # 更新遊戲
    all_sprites.update()
    
    hits = pygame.sprite.spritecollide(player, rocks, False, pygame.sprite.collide_circle)
    if hits:
        show_init = True
        rock_sound.stop()
    


    # 畫面顯示
    screen.fill(BALCK)
    screen.blit(pygame_frames[frame_index], (250, 20))
    pygame.display.flip()
    frame_index = (frame_index + 1) % len(pygame_frames)
    # clock.tick(20)
    all_sprites.draw(screen)
    pygame.display.update()
pygame.quit()