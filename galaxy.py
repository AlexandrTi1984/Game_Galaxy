import pygame
import random
from os import path
import json
from operator import itemgetter

WIDTH = 480  # ширина игрового окна
HEIGHT = 600 # высота игрового окна
FPS = 60 # частота кадров в секунду
# Цвета (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
# настройка папки ассетов
img_dir = path.join(path.dirname(__file__),'img')
snd_dir = path.join(path.dirname(__file__),'snd')

# создаем игру и окно
pygame.init()
pygame.mixer.init() # для звука
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('My Galaxy game')
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((50, 40))
        # self.image.fill(GREEN)
        self.image = random.choice(Player_images)
        self.image.set_colorkey(BLACK) # убрать лишний фон с картинки
        self.rect = self.image.get_rect()
        #чертим круг для столкновения с метеором по кругу  ищем оптимальное значение. фото квадратное желательно
        self.radius = 33
        #pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
        self.rect.centerx = (WIDTH / 2)
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        # стрельба при удержании пробела
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        #Улучшение силы если взял ачивку улучшение
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        #стрельба 3 шариками
        self.superbullet = False
    def update(self):
        self.speedx = 0 # делаем движение вправо и влево, верх и низ
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()
        if keystate[pygame.K_UP]:
            self.speedy = -8
        if keystate[pygame.K_DOWN]:
            self.speedy = 8
        self.rect.x += self.speedx
        self.rect.y +=self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top <0:
            self.rect.top = 4
        # показать, если скрыт после смерти
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        #тайм маут для бонуса сила
        if self.power >=2 and pygame.time.get_ticks() - self.power_time >= POWER_TIME:
            self.power -= 1
            self.superbullet = False
            self.power_time = pygame.time.get_ticks()
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1 :
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2 and self.superbullet == False:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                bullet = Bullet(self.rect.centerx, self.rect.top)
            if self.power >= 2 and self.superbullet == True:
                bullet1 = Bulett_Special(self.rect.right, self.rect.centery,'right')
                bullet2 = Bulett_Special(self.rect.left, self.rect.centery,'left')
                bullet = Bulett_Special(self.rect.centerx, self.rect.top,'center')
            if self.power >=2: #Добавляем спрайты и звук
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet)
                bullets.add(bullet)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
    def hide(self): #скрытие игрока на время после его убийства
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)
    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((30,40))
        # self.image.fill(RED)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK) # убрать лишний фон с картинки
        self.image = self.image_orig.copy() #копируем для вращение - анимации
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85/ 2) #ищем оптимальный вариант
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1,8)
        self.speedx = random.randrange(-3, 3)
        #анимация, повороты
        self.rot = 0
        self.rot_speed = random.randrange(-8,8)
        self.last_update = pygame.time.get_ticks()
        self.count = 8 # начальное количество мобов
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH+20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, 40)
            self.speedy = random.randrange(1, 8)
            self.rotate()
    def rotate(self):  #вращение моба
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            # вращение спрайтов
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

class Bullet(pygame.sprite. Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((10,20))
        # self.image.fill(WHITE)
        self.image = bullet_img
        self.image.set_colorkey(BLACK) # убрать лишний фон с картинки
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speddy = -10
    def update(self):
        self.rect.y += self.speddy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom <0:
            self.kill()
class Bulett_Special(pygame.sprite. Sprite):
    def __init__(self,x,y,my_direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(img_dir,'bulletSpecial2.jpg')).convert()
        self.image.set_colorkey(WHITE) # убрать лишний фон с картинки
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speddy = -10
        self.way = my_direction  # направление , вправо, влево, центр
    def update(self):  # стрельбя треугольником
            self.rect.y += self.speddy
            if self.way == 'left':
                self.rect.centerx -=2
            if self.way == 'right':
                self.rect.centerx +=2
            # убить, если он заходит за верхнюю часть экрана
            if self.rect.bottom <0:
                self.kill()
class Bulett_Special_Boss(pygame.sprite. Sprite):
    def __init__(self,x,y,my_direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(img_dir,'bulletSpecial1.jpg')).convert()
        self.image.set_colorkey(WHITE) # убрать лишний фон с картинки
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speddy = 3
        self.way = my_direction  # направление , вправо, влево, центр
    def update(self):  # стрельбя треугольником
            self.rect.y += self.speddy
            if self.way == 'right':
                self.rect.centerx += 1
            if self.way == 'left':
                self.rect.centerx -= 1
            # убить, если он заходит за нижнюю часть экрана
            if self.rect.top > HEIGHT:
                self.kill()
class Explosion(pygame.sprite.Sprite): #взрывы
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_aim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_aim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image=explosion_aim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
class Power(pygame.sprite.Sprite):  #Улучшения
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun','bomb','life','copy','superbullet'])
        self.image = power_images[self.type]
        #self.image.set_colorkey(BLACK) # убрать лишний фон с картинки
        self.image.set_colorkey(WHITE) # убрать лишний фон с картинки
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2
    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.top >HEIGHT:
            self.kill()
# Копия игрока для смещения к игроку ачивкой
class Copy_player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(img_dir,'playerCopy.png')).convert()
        self.image.set_colorkey(WHITE)  # убрать лишний фон с картинки
        self.rect = self.image.get_rect()
#Позиция появления клона
        self.rect.centerx = 30
        self.rect.bottom = HEIGHT
        self.speedx = 3
        # стрельба при удержании пробела
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
    def update(self):
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.kill()
        self.shoot()
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet1 = Bullet(self.rect.left, self.rect.centery)
            bullet2 = Bullet(self.rect.right, self.rect.centery)
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            all_sprites.add(bullet)
            bullets.add(bullet)
            bullets.add(bullet1)
            bullets.add(bullet2)
            shoot_sound.play()
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(Boss_images)
        self.image.set_colorkey(BLACK)  # убрать лишний фон с картинки
        self.rect = self.image.get_rect()
        # чертим круг для столкновения с метеором по кругу  ищем оптимальное значение. фото квадратное желательно
        self.radius = 37
        #pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.centery = 40
        self.rect.bottom = 100
        self.speedx = 4
        self.shield = 50
        # стрельба при удержании пробела
        self.shoot_delay = 1000
        self.last_shot = pygame.time.get_ticks()
        self.visible = False
        self.hide_timer = pygame.time.get_ticks()
        self.superbullet = False
    def update(self):
        if random.randint(1,2) == 1:
            self.rect.x += self.speedx
        else:
            self.rect.x -= self.speedx
        if self.rect.x > WIDTH-60:
            self.rect.x = WIDTH-60
            self.rect.x -= self.speedx
        if self.rect.x < 0:
            self.rect.x = 0
            self.rect.x += self.speedx
        if self.shield <=0:
            self.kill()
        self.shoot()
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet1_boss = Bulett_Special_Boss(self.rect.left, self.rect.centery, 'left')
            bullet2_boss = Bulett_Special_Boss(self.rect.right, self.rect.centery, 'right')
            bullet3_boss = Bulett_Special_Boss(self.rect.centerx, self.rect.top, 'center')
            all_sprites.add(bullet1_boss)
            all_sprites.add(bullet2_boss)
            all_sprites.add(bullet3_boss)
            bullets_boss.add(bullet1_boss)
            bullets_boss.add(bullet2_boss)
            bullets_boss.add(bullet3_boss)

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)
def new_mob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
def draw_bar_shield(surf, x, y, pct):
    if pct < 0:
        pct =0
    Bar_length = 100
    Bar_hieght = 10
    fill = (pct / 100) * Bar_length
    outline_rect = pygame.Rect(x,y, Bar_length, Bar_hieght)
    fill_rect = pygame.Rect(x,y, fill, Bar_hieght)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect,2)
def draw_bar_shield_Boss(surf, x, y, pct):
    if pct < 0:
        pct =0
    Bar_length = 200
    Bar_hieght = 20
    fill = (pct / 100) * Bar_length
    outline_rect = pygame.Rect(x,y, Bar_length, Bar_hieght)
    fill_rect = pygame.Rect(x,y, fill, Bar_hieght)
    pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect,2)
def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x +30 * i
        img_rect.y = y
        surf.blit(img, img_rect)
def show_go_screen():  #экран окончания игры + начало игры + рекорды
    screen.blit(background, background_rect)
    draw_text(screen, "Galaxy", 50, WIDTH / 2, HEIGHT / 4 + 100)
    draw_text(screen, 'Press key LEFT or RIGHT or FIRE',22, WIDTH / 2, HEIGHT / 2 + 100)
    draw_text(screen, 'Press ENTER to begin',18, WIDTH / 2, HEIGHT *3 / 4 +100)

   # ============== Показ топ 5 рекордов ========================
# Display the high-scores.
    draw_text(screen, "TOP - 5 Score", 30, WIDTH / 2, 5)
    highscores=load()
    for y, (hi_name, hi_score) in enumerate(highscores):
        if y <=4:
            draw_text(screen, f'{hi_name} {hi_score}', 16, WIDTH / 2, y * 30 + 45)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

# = = = Сохранение и загрузка рекордов   = = = =
def save(highscores):
    with open('highscores.json', 'w') as file:
        json.dump(highscores, file)  # Write the list to the json file.
def load():
    try:
        with open('highscores.json', 'r') as file:
            highscores = json.load(file)  # Read the json file.
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist.
    # Sorted by the score.
    return sorted(highscores, key=itemgetter(1), reverse=True)

#Отображение текста со счетом
font_name = pygame.font.match_font('arial')
# Загрузка всей игровой графики
background = pygame.image.load(path.join(img_dir,'sky.jpg')).convert()
background_rect = background.get_rect()
Player_images = []
player_list_img = ['playerShip1_green.png','playerShip2_green.png','playerShip3_green.png']
for img in player_list_img:
    Player_images.append(pygame.image.load(path.join(img_dir, img)).convert())
Boss_images = []
Boss_list_img = ['enemy1.png','enemy2.png','enemy3.png','enemy4.png']
for img in Boss_list_img:
    Boss_images.append(pygame.image.load(path.join(img_dir, img)).convert())

#player_img = pygame.image.load(path.join(img_dir,'playerShip1_green.png')).convert()
#Загрузка музыки
shoot_sound = pygame.mixer.Sound(path.join(snd_dir,'sfx_laser1.ogg'))
death_sound_player = pygame.mixer.Sound(path.join(snd_dir,'rumble1.ogg'))
expl_sounds = []
for snd in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir,snd)))
pygame.mixer.music.load(path.join(snd_dir,'game music.mp3'))
#pygame.mixer.music.set_volume(1)
#meteor_img = pygame.image.load(path.join(img_dir,'meteorBrown_small1.png')).convert()
meteor_images = []
meteor_list = ['meteorBrown_small1.png','meteorGrey_tiny2.png','meteorGrey_tiny1.png',
'meteorGrey_small2.png','meteorGrey_med2.png','meteorGrey_small1.png'
]
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

bullet_img = pygame.image.load(path.join(img_dir,'laserGreen04.png')).convert()
all_sprites =pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
bullets_boss = pygame.sprite.Group()
powerups = pygame.sprite.Group()
copy_players = pygame.sprite.Group()
boss = pygame.sprite.Group()
player = Player()
big_boss = Boss()
# all_sprites.add(big_boss)
all_sprites.add(player)
my_score = 0
name_player = 'AlexTi'
mobs_count = 5
POWER_TIME = 4000  #4 СЕКУНД для ачивка стрельба
for i in range(mobs_count):  # создаем 8 астероидов.
    new_mob()
pygame.mixer.music.play(loops= -1)
#загрузка картинок (анимация) взрывов для астероидов и коробля. Большие для мобов, маленький для коробля
# и трансформация размера
explosion_aim = {}
explosion_aim['lg']=[]
explosion_aim['sm']=[]
explosion_aim['player']=[]
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir,filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img,(75,75))
    img_sm = pygame.transform.scale(img,(32,32))
    explosion_aim['lg'].append(img_lg)
    explosion_aim['sm'].append(img_sm)
    #взрыв игрока
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir,filename)).convert()
    img.set_colorkey(BLACK)
    explosion_aim['player'].append(img)
#Иконки жизни игрока
player_img_ico = pygame.image.load(path.join(img_dir,'ufoGreen.png')).convert()
player_img_mini = pygame.transform.scale(player_img_ico, (25, 19))
player_img_mini.set_colorkey(BLACK)
#Изображения и звук доп усилия Жизнь и оружие
power_images = {}
power_images['shield'] = pygame.image.load(path.join(img_dir,'shield_gold.png')).convert()
power_images['gun'] = pygame.image.load(path.join(img_dir,'bolt_gold.png')).convert()
power_images['bomb'] = pygame.image.load(path.join(img_dir,'bomb.jpg')).convert()
power_images['life']= pygame.image.load(path.join(img_dir,'ufoGreenlife.png')).convert()
power_images['copy']= pygame.image.load(path.join(img_dir,'playerCopyMIni.png')).convert()
power_images['superbullet']= pygame.image.load(path.join(img_dir,'bulletSpecial.jpg')).convert()
shield_sound = pygame.mixer.Sound(path.join(snd_dir,'power_shield.mp3'))
power_sound = pygame.mixer.Sound(path.join(snd_dir,'power_weapon.mp3'))
bomb_sound = pygame.mixer.Sound(path.join(snd_dir,'bomb.wav'))
# Игровой Цикл игры
game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        #сброс всех данных для старта с 0 нуля
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        big_boss = Boss()
        # all_sprites.add(big_boss)
        all_sprites.add(player)
        my_score = 0
        for i in range(mobs_count):
            new_mob()
    # держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    # Закрытие окна
    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT:
            running = False
        # elif event.type ==pygame.KEYDOWN:
        #     if event.key ==pygame.K_SPACE:
        #         player.shoot()
    # Обновление
    all_sprites.update()
    # Появление Босса на --- очках
    if my_score == 20 or my_score == 200 or my_score == 450 or my_score == 700 or my_score == 1000 or my_score == 1300 or my_score == 1700:
        for m in mobs:
            m.kill()
            expl = Explosion(m.rect.center, 'lg')
            all_sprites.add(expl)
        all_sprites.add(big_boss)
        big_boss.visible = True

    #Проверка столкновения игрока с улучшением
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10,30)
            shield_sound.play()
            if player.shield >  100:
                player.shield = 100
        if hit.type == 'gun':
            player.superbullet = False
            power_sound.play()
            player.powerup()
        if hit.type == 'bomb':
            bomb_sound.play()
            for m in mobs:
                m.kill()
                expl = Explosion(m.rect.center, 'lg')
                all_sprites.add(expl)
            for i in range(mobs_count):
                new_mob()
        if hit.type == 'life':  # Больше 5 жизней не даем
            shield_sound.play()
            if player.lives <=4:
                player.lives += 1
        if hit.type == 'copy': # Создание клона на 5 сек
            shield_sound.play()
            clon = Copy_player()
            all_sprites.add(clon)
            copy_players.add(clon)
        if hit.type == 'superbullet':
            player.superbullet = True
            player.powerup()
        power_sound.play()
    # Проверка поподание пули в моба
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        my_score += 1
        if my_score % 50 == 0: # Увеличиваем количество мобов для сложности
            mobs_count +=1
        random.choice(expl_sounds).play() #Рандомный взрыв из списка
       #my_score += 50 - hit.radius # Разное количество в зависимости от объема метеорита
        #добавляем спрайт взрыва, т.к попал в моба
        expl = Explosion(hit.rect.center,'lg')
        all_sprites.add(expl)
        #Выпадание бонуса
        if random.random()> 0.80:
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        new_mob() # добавляем моба через функцию
    # Проверка, не ударил ли моб игрока В spritecollide изменим значение с False на True,
    # потому что нужно, чтобы астероид исчезал после попадания.
    hits = pygame.sprite.spritecollide(player,mobs,True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= 20
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        new_mob()
        if player.shield <=0:
            death_explosion = Explosion(player.rect.center,'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1 #Если убили - отнимаем одну жизнь и здоровье 100%
            player.shield = 100
            death_sound_player.play()
           # player.kill()
        # Проверка - попала ли пуля босса в игрока ставит TRUE чтоб пуля исчезла
    if big_boss.visible == True:
        hits = pygame.sprite.spritecollide(player, bullets_boss, True, pygame.sprite.collide_circle)
        for hit in hits:
            player.shield -= 20
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            if player.shield <= 0:
                death_explosion = Explosion(player.rect.center, 'player')
                all_sprites.add(death_explosion)
                player.hide()
                player.lives -= 1  # Если убили - отнимаем одну жизнь и здоровье 100%
                player.shield = 100
                death_sound_player.play()
            # Проверка попадания пули игрока в босса
        hits = pygame.sprite.spritecollide(big_boss, bullets, True)
        for hit in hits:
            big_boss.shield -=2
            if big_boss.shield <= 0:
                big_boss.shield = 100 # возвращаем хп к исходному
                big_boss.kill()
                big_boss.visible = False
                for i in range(mobs_count):
                    new_mob()
            my_score += 2  # 2 очка за попадание в боса
            random.choice(expl_sounds).play()  # Рандомный взрыв из списка
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)

            # Если игрок умер, игра окончена
    if player.lives ==0 and not death_explosion.alive():
        game_over = True
        # ============== Запись в файл и сортировка по очкам ========================
        highscores = load()
        highscores.append([name_player, my_score])
        save(sorted(highscores, key=itemgetter(1), reverse=True))
        print('Game Over')

    # Рендеринг и отрисовка
    screen.fill(BLACK)
    screen.blit(background,background_rect)
    all_sprites.draw(screen)
    draw_text(screen, f'Score: {str(my_score)}',20, WIDTH /2, 10) #рисуем счет через функцию
    draw_bar_shield(screen, 5, 5, player.shield) #рисуем шкалу здоровья через функцию
    draw_lives(screen, WIDTH -150, 5, player.lives, player_img_mini)  # отображение количества жизней
    if big_boss.visible == True:
        draw_bar_shield_Boss(screen, 5, 40, big_boss.shield)  # рисуем шкалу здоровья через функцию) для босса
    # после отрисовки всего, переворачиваем экран
    pygame.display.flip()
    # Визуализация (сборка)

pygame.quit()