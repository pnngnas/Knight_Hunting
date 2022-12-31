import pygame, random

pygame.init()

#Defind SOME color
PINK = (158, 50, 168)
GREEN = (30, 189, 38)
ORANGE = (217, 101, 7)
BLUE = (10, 43, 173)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (209, 206, 23)


#Create surface
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#FPS
FPS = 60
clock = pygame.time.Clock()

#Define class
class Game():
    def __init__(self, player, monster_group):
        self.player = player
        self.monster_group = monster_group
        self.score = 0
        self.round = 1
        self.time = 0
        self.frame_count = 0
        self.target_monster = random.choice(monster_group.sprites())
        self.target_type = self.target_monster.type

        #font
        self.font = pygame.font.Font("./asset/font.ttf",32)
        self.colors = [BLUE, GREEN, PINK, ORANGE]

        #Define sound
        self.collect_sound = pygame.mixer.Sound("./asset/collect.mp3")
        self.backgr_music = pygame.mixer.Sound("./asset/music.mp3")
        self.miss_sound = pygame.mixer.Sound("./asset/miss.mp3")
        self.game_over_sound = pygame.mixer.Sound("./asset/gameover.wav")
        self.warp_sound = pygame.mixer.Sound("./asset/warp_sound.mp3")

    def check_collide(self):
        collied_monster = pygame.sprite.spritecollideany(player, monster_group)
        if collied_monster:
            if collied_monster.type == self.target_type:
                self.score += int (10000*self.round / (self.time + 1 ) )
                collied_monster.remove(monster_group)
                self.collect_sound.play()
                #Check monster group contain monster
                if monster_group:
                    self.choose_new_target()
                else:
                    self.round += 1
                    self.start_new_round()
            #MEET sai con
            else:
                self.player.lives -= 1
                self.player.warps()
                self.miss_sound.play()
                #Check lose
                if self.player.lives <= 0:
                    self.game_over_sound.play()
                    self.pause_game("You LOSE, Press ENTER to PlayAgain")
                    self.reset_game()

    def start_new_round(self):
        number_monster = 2 * self.round
        for monster in self.monster_group.sprites():
            monster_group.remove(monster)
        for i in range(1, number_monster + 1):
            monster_group.add(Monster(random.randint(0, WINDOW_WIDTH - 64),random.randint(100, WINDOW_HEIGHT - 100 - 64),random.randint(0,3)))
        self.choose_new_target()
        self.player.come_back()
        self.player.warp += 1


    def choose_new_target(self):
        self.target_monster = random.choice(monster_group.sprites())
        self.target_type = self.target_monster.type

    def update(self):
        self.frame_count += 1
        if self.frame_count == FPS:
            self.time += 1
            self.frame_count = 0

    def draw(self):

        score_text = self.font.render(f'Scores:  {self.score}', True, YELLOW)
        score_text_rect = score_text.get_rect()
        score_text_rect.topleft = (10, 10)

        lives_text = self.font.render(f'Lives:  {self.player.lives}', True, YELLOW)
        lives_text_rect = lives_text.get_rect()
        lives_text_rect.topright = (WINDOW_WIDTH -10 , 10)

        warps_text = self.font.render(f'Warps:  {self.player.warp}', True, YELLOW)
        warps_text_rect = warps_text.get_rect()
        warps_text_rect.topright = (WINDOW_WIDTH - 10, 40)

        display_surface.blit(score_text, score_text_rect)
        display_surface.blit(lives_text, lives_text_rect)
        display_surface.blit(warps_text, warps_text_rect)

        #Draw target monster
        display_surface.blit(self.target_monster.image, (WINDOW_WIDTH//2, 10, 64, 64))

        #Draw the rect restric
        pygame.draw.rect(display_surface,self.colors[self.target_type], (0, 100,WINDOW_WIDTH, WINDOW_HEIGHT - 200), 3)

    def pause_game(self, text):
        pause = True
        self.backgr_music.stop()
        font = pygame.font.Font("./asset/font.ttf", 46)
        pause_text = font.render(text, True, YELLOW)
        pause_text_rect = pause_text.get_rect()
        pause_text_rect.center = (WINDOW_WIDTH //2, WINDOW_HEIGHT //2 )
        while pause:
            display_surface.fill(BLACK)
            display_surface.blit(pause_text, pause_text_rect)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pause = False
        self.backgr_music.play(-1)



    def reset_game(self):
        self.player.reset()
        self.score = 0
        self.round = 1
        self.start_new_round()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./asset/knight.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH //2
        self.rect.bottom = WINDOW_HEIGHT
        self.lives = 4
        self.speed = 8
        self.warp = 2


    def update(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= self.speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 100:
            self.rect.y -= self.speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < WINDOW_HEIGHT - 100:
            self.rect.y += self.speed

    def warps(self):
        self.warp -= 1
        my_game.warp_sound.play()
        self.rect.centerx = WINDOW_WIDTH//2
        self.rect.bottom = WINDOW_HEIGHT

    def come_back(self):
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT

    def reset(self):
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT
        self.lives = 4
        self.warp = 2

class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.type = type
        blue_monster = pygame.image.load("./asset/blue_monster.png")
        green_monster = pygame.image.load("./asset/green_monster.png")
        pink_monster = pygame.image.load("./asset/pink_monster.png")
        orange_monster = pygame.image.load("./asset/orange_monster.png")
        self.images = [blue_monster, green_monster , pink_monster, orange_monster]
        self.image = self.images[self.type]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = random.randint(3,5)
        self.dx = random.choice([-1,1])
        self.dy = random.choice([-1,1])


    def update(self):
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed
        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            self.dx *= -1
        if self.rect.top <= 100 or self.rect.bottom >= WINDOW_HEIGHT - 100:
            self.dy *= -1

#SPRITE GRP
player_group = pygame.sprite.Group()
player = Player()
player_group.add(player)

monster_group = pygame.sprite.Group()
monster_group.add(Monster(random.randint(0, WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT - 100 - 64), random.randint(0, 3)))


my_game = Game(player, monster_group)
my_game.pause_game("Tap enter to play!")
my_game.backgr_music.play(-1)
my_game.start_new_round()
#MAIN GAME LOOP
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and my_game.player.warp > 0 and my_game.player.rect.bottom <= WINDOW_HEIGHT - 100:
                my_game.player.warps()

    #Fill the back
    display_surface.fill((0, 0, 0))

    #Check Collied
    my_game.check_collide()

    #BLIT ASSET
    my_game.update()
    my_game.draw()

    player_group.update()
    player_group.draw(display_surface)

    monster_group.update()
    monster_group.draw(display_surface)
    #Update display and clock
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()