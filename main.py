import pygame
import sys
pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
FPS = 60
BLACK = (172,212,115)
GREEN = (55,54,53)
ADD_NEW_FLAME_RATE = 45
CLOCK = pygame.time.Clock()
font = pygame.font.Font('Futura XBlk BT.ttf',20)
teto_img = pygame.image.load('teto.png')
teto_img_rect = teto_img.get_rect()
teto_img_rect.left = 0
piso_img = pygame.image.load('teto.png')
piso_img_rect = piso_img.get_rect()
piso_img_rect.left = 0

tela = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('MOSQUITO MANIA')

class Topscore:
    def __init__(self):
        self.high_score = 0
    def top_score(self, score):
        if score > self.high_score:
            self.high_score = score
        return self.high_score
      
topscore = Topscore()

class Enemy(pygame.sprite.Sprite):
    enemy_velocity = 5
    frame_delay = 70
  
    def __init__(self):
        self.enemy_imgs = [pygame.image.load('e1.png'),pygame.image.load('e2.png'),pygame.image.load('e3.png')]
        self.index = 0
        self.frame_count = 0
        self.image = self.enemy_imgs[0]
        self.enemy_img_rect = self.image.get_rect()
        self.enemy_img_rect.width -= 10
        self.enemy_img_rect.height -= 10
        self.enemy_img_rect.top = WINDOW_HEIGHT/2
        self.enemy_img_rect.right = WINDOW_WIDTH - 20
        self.up = True
        self.down = False
        self.last_frame_time = pygame.time.get_ticks()
        
    def update(self):
                # Verifica se é hora de atualizar a animação
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_time > self.frame_delay:
            self.index = (self.index + 1) % len(self.enemy_imgs)
            self.image = self.enemy_imgs[self.index]
            self.last_frame_time = current_time
        
        
        tela.blit(self.image, self.enemy_img_rect)
        if self.enemy_img_rect.top <= teto_img_rect.bottom:
            self.up = False
            self.down = True
        elif self.enemy_img_rect.bottom >= piso_img_rect.top:
            self.up = True
            self.down = False
            
        if self.up:
            self.enemy_img_rect.top -= self.enemy_velocity
        elif self.down:
            self.enemy_img_rect.top += self.enemy_velocity
        
class Fogo(pygame.sprite.Sprite):
    fogo_velocity = 10
    frame_delay = 82
  
    def __init__(self):
        self.fogo_imgs = [pygame.image.load('f1.png'),pygame.image.load('f2.png'),pygame.image.load('f3.png')]
        self.index = 0
        self.frame_count = 0
        self.image = self.fogo_imgs[0]
        # self.fogo_img = pygame.transform.scale(self.fogo, (20,20))
        self.fogo_img_rect = self.image.get_rect()
        self.fogo_img_rect.right = enemy.enemy_img_rect.left
        self.fogo_img_rect.top = enemy.enemy_img_rect.top + 30
        self.last_frame_time = pygame.time.get_ticks()
        self.sound = pygame.mixer.Sound('fogo.wav')
        self.sound.play()

    def update(self):
        # Verifica se é hora de atualizar a animação
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_time > self.frame_delay:
            self.index = (self.index + 1) % len(self.fogo_imgs)
            self.image = self.fogo_imgs[self.index]
            self.last_frame_time = current_time
            
        tela.blit(self.image, self.fogo_img_rect)
        if self.fogo_img_rect.left > 0:
            self.fogo_img_rect.left -= self.fogo_velocity 

class Heroi(pygame.sprite.Sprite):
    velocity = 1
    frame_delay = 32
    
    def __init__(self):
        self.heroi_imgs = [pygame.image.load('h1.png'),pygame.image.load('h2.png'),pygame.image.load('h3.png')]
        self.index = 0
        self.frame_count = 0
        self.image = self.heroi_imgs[0]
        self.heroi_img_rect = self.image.get_rect()
        self.heroi_img_rect.left = 20
        self.heroi_img_rect.top = WINDOW_HEIGHT/2 - 100
        self.down = True
        self.up = False
        self.last_frame_time = pygame.time.get_ticks()
        
    def update(self):
        # Verifica se é hora de atualizar a animação
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_time > self.frame_delay:
            self.index = (self.index + 1) % len(self.heroi_imgs)
            self.image = self.heroi_imgs[self.index]
            self.last_frame_time = current_time
        
        
        tela.blit(self.image, self.heroi_img_rect)
        if self.heroi_img_rect.top <= teto_img_rect.bottom:
            game_over()
            if SCORE > self.heroi_score:
                self.heroi_score = SCORE
        if self.heroi_img_rect.bottom >= piso_img_rect.top:
            game_over()
            if SCORE > self.heroi_score:
                self.heroi_score = SCORE
        if self.up:
            self.heroi_img_rect.top -= 4
        if self.down:
            self.heroi_img_rect.bottom += 4

def game_over():
    # pygame.mixer.music.stop()
    # music = pygame.mixer.sound('heroi_morte.wav')
    # music.play()
    topscore.top_score(SCORE)
    game_over_img = pygame.image.load('over.png')
    game_over_img_rect = game_over_img.get_rect()
    game_over_img_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    tela.blit(game_over_img, game_over_img_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # music.stop()
                game_loop()
                #ESTAVA FALTANDO PARENTESES NO FIM DO UPDATE
        pygame.display.update()
    
def start_game():
    tela.fill(BLACK)
    start_img = pygame.image.load('start.png')
    start_img_rect = start_img.get_rect()
    start_img_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    tela.blit(start_img, start_img_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                game_loop()
        pygame.display.update()

def check_level(SCORE):
    global LEVEL
    if SCORE in range(0,10):
        teto_img_rect.bottom = 50
        piso_img_rect.top = WINDOW_HEIGHT - 50
        LEVEL = 1
    elif SCORE in range(10,20):
        teto_img_rect.bottom = 100
        piso_img_rect.top = WINDOW_HEIGHT - 100
        LEVEL = 2
    elif SCORE in range(20,30):
        teto_img_rect.bottom = 150
        piso_img_rect.top = WINDOW_HEIGHT - 150
        LEVEL = 3
    elif SCORE > 30:
        teto_img_rect.bottom = 200
        piso_img_rect.top = WINDOW_HEIGHT - 200
        LEVEL = 4

def game_loop():
    while True:
      global enemy
      enemy = Enemy()
      fogo = Fogo()
      heroi = Heroi()
      add_new_fogo_counter = 0
      global SCORE
      SCORE = 0
      global HIGH_SCORE
      fogo_list = []
      pygame.mixer.music.load('tema.wav')
      pygame.mixer.music.play(-1, 0.0)
      while True:
          tela.fill(BLACK)
          check_level(SCORE)
          enemy.update()
          add_new_fogo_counter += 1
          
          if heroi.index >= len(heroi.heroi_imgs):
              heroi.index = 0
          heroi.image = heroi.heroi_imgs[heroi.index]
          heroi.index += 1
          
          
          if add_new_fogo_counter == ADD_NEW_FLAME_RATE:
              add_new_fogo_counter = 0
              new_fogo = Fogo()
              fogo_list.append(new_fogo)
          for f in fogo_list:
              if f.fogo_img_rect.left <= 0:
                  fogo_list.remove(f)
                  SCORE += 1
              f.update()
              #A LOGICA TA ERRADA, O HEROI NAO PULA
              #Resolvido: ao inves de event.key, eu escrevi event.type(linha 199)
          for event in pygame.event.get():
              if event.type == pygame.QUIT:
                  pygame.quit()
                  sys.exit()
              if event.type == pygame.KEYDOWN:
                  if event.key == pygame.K_UP:
                      heroi.up = True
                      heroi.down = False
                  elif event.key == pygame.K_DOWN:
                      heroi.down = True
                      heroi.up = False
              if event.type == pygame.KEYUP:
                  if event.key == pygame.K_UP:
                      heroi.up = False
                      heroi.down= True
                  elif event.key == pygame.K_DOWN:
                      heroi.down = True
                      heroi.up = False
                      
          score_font = font.render('Score:'+str(SCORE), True, GREEN)
          score_font_rect = score_font.get_rect()
          score_font_rect.center = (200, teto_img_rect.bottom + score_font_rect.height/2)
          tela.blit(score_font, score_font_rect)
          
          level_font = font.render('Level:'+str(LEVEL ), True, GREEN )
          level_font_rect = level_font.get_rect()
          level_font_rect.center = (500, teto_img_rect.bottom + score_font_rect.height/2)
          tela.blit(level_font, level_font_rect)
          
          top_score_font = font.render('Top Score:'+str(topscore.high_score), True, GREEN)
          top_score_font_rect = top_score_font.get_rect()
          top_score_font_rect.center = (800, teto_img_rect.bottom + score_font_rect.height/2)
          tela.blit(top_score_font, top_score_font_rect)
          
          tela.blit(teto_img, teto_img_rect)
          tela.blit(piso_img, piso_img_rect)
          heroi.update()
          for f in fogo_list:
              if f.fogo_img_rect.colliderect(heroi.heroi_img_rect):
                  game_over()
                  if SCORE > heroi.heroi_score:
                     heroi.heroi_score = SCORE
          pygame.display.update()
          CLOCK.tick(FPS)
              
          
      
start_game()