from random import randint, random
import time
import pygame

pygame.mixer.init()
pygame.mixer.music.load("assets/space.ogg")
pygame.mixer.music.play()
fire_sound = pygame.mixer.Sound("assets/fire.ogg")

win_width = 700 
win_height = 500
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Space Shooter")
background = pygame.transform.scale(pygame.image.load("assets/galaxy.jpg"), (win_width, win_height))
clock = pygame.time.Clock()
game = True
finish = False
paused = False

MIN_ENEMY_SPEED = 1
MAX_ENEMY_SPEED = 4

score = 0
missed = 0

pygame.font.init() 
font = pygame.font.Font("fonts/LilitaOne-Regular.ttf", 36)
font_big = pygame.font.Font(None, 72)

win_text = font_big.render("You win!", True, (50, 255, 50))
lose_text = font_big.render("You lose!", True, (255, 0, 0))
pause_text = font_big.render("Paused", True, (255, 255, 255))

last_time_fire = time.time()
#головний класс для спрайта
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_image, x, y, width, height, speed):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load(sprite_image), (width, height)
        )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))
        
        
#клас для гравця    
class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.x < win_width - self.rect.width:
            self.rect.x += self.speed
           
    def fire(self):
        global last_time_fire
        cur_time = time.time ()
        if cur_time - last_time_fire > 0.3:
            bullet = Bullet("assets/bullet.png", self.rect.centerx - 5, self.rect.y, 10, 20, 15)
            bullets.add(bullet)
            fire_sound.play() 
            last_time_fire = cur_time
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global missed
        if self.rect.y > win_height:
            self.rect.x = randint(5, win_width - self.rect.width)
            self.speed = randint(MIN_ENEMY_SPEED, MAX_ENEMY_SPEED)
            self.rect.y = -60 
            missed += 1
            
            
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
            
            
bullets = pygame.sprite.Group()
player = Player("assets/rocket.png", 200, win_height - 100, 50, 80, 5)

aliens = pygame.sprite.Group()
for i in range(6):
    x = randint(5, win_width - 120)
    y = -40
    speed = randint(MIN_ENEMY_SPEED, MAX_ENEMY_SPEED)
    alien = Enemy("assets/ufo.png", x,y ,100, 50, speed)
    aliens.add(alien)


paused_surface = pygame.Surface((win_width, win_height), pygame.SRCALPHA)
paused_color = (92, 0, 154, 128)
paused_surface.fill(paused_color)


while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not finish:
                player.fire()
            if event.key == pygame.K_ESCAPE and not finish:
                if paused:
                    paused = False
                else:
                    paused = True
                    
                
    if paused:
        
        win.blit(background, (0, 0))
        player.reset()
        aliens.draw(win)
        bullets.draw(win)
        win.blit(paused_surface, (0 ,0))
        win.blit(pause_text, (260, 220))
        win.blit(score_label, (10, 20))
        win.blit(missed_label, (10, 50))
        pygame.display.update()
        
        
        
    if not finish and not paused:
        win.blit(background, (0 ,0))
       
        player.update()
        player.reset()
        aliens.update()
        aliens.draw(win)
        
        bullets.update()
        bullets.draw(win)
        
        score_label = font.render(f"Score: {score}", True, (255, 255, 255))
        missed_label = font.render(f"Missed: {missed}", True, (255, 255, 255))
        
        win.blit(score_label, (10, 20))
        win.blit(missed_label, (10, 50))
        
        collides = pygame.sprite.groupcollide(aliens, bullets, True, True)
        for c in collides:
            score += 1
            x = randint(5, win_width - 100)
            y = -40
            speed = randint(MIN_ENEMY_SPEED, MAX_ENEMY_SPEED)
            alien = Enemy("assets/ufo.png", x,y ,100, 50, speed)
            aliens.add(alien)
        
        if pygame.sprite.spritecollide(player, aliens, False) or missed >= 14:
            finish = True
            win.blit(lose_text, (200, 250))
            
        if score >= 29:
            finish = True
            win.blit(win_text, (200, 250))
        pygame.display.update()    
    clock.tick(50)
