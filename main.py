from random import random
import sys, pygame, unidecode

pygame.init()

SIZE = WIDTH, HEIGHT = 640, 480

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Jogo da Forca')

font = pygame.freetype.SysFont('Arial', 12, bold=True, italic=False)

running = False

with open ('palavras.txt', 'r', encoding='UTF-8') as f:
    palavras = f.read().splitlines()

def init_game():
    global running
    global letras_digitadas
    global palavra
    global letras_palavra
    global tentativas
    global end_game

    letras_digitadas = []
    letras_palavra = []
    running = True
    tentativas = 6
    end_game = False
    
    palavra = unidecode.unidecode(palavras[int(random() * len(palavras))]) 
    for i in range(len(palavra)):
        letras_palavra.append({'letra': palavra[i].lower(), 'pos': ((40+(i*32)+16)+4, (HEIGHT / 2)-30), 'mostrando': False})

    game_loop()

def game_loop():
    while running:
        update()
        render()

def update():
    handle_events()

def render():

    global end_game

    screen.fill((255, 255, 255))

    for i in range(len(palavra)):
        pygame.draw.line(screen, (0, 0, 255), (40+(i*32)+16, (HEIGHT / 2)), (70+(i*32)+16, (HEIGHT / 2)), width=4)
        if letras_palavra[i]['mostrando']:
            text_surface, rect = font.render(palavra[i].upper(), fgcolor=(234, 100, 5), bgcolor=None, rotation=0, size=32)
            screen.blit(text_surface, letras_palavra[i]['pos'])

    if len([x for x in letras_palavra if x['mostrando'] == False]) == 0:
        text_surface, rect = font.render('Parabéns!', fgcolor=(255, 0, 0), bgcolor=None, rotation=0, size=48)
        screen.blit(text_surface, (50, (HEIGHT / 2)+100))
        end_game = True

    if tentativas == 0:
        text_surface, rect = font.render('Game Over!', fgcolor=(255, 0, 0), bgcolor=None, rotation=0, size=48)
        screen.blit(text_surface, (50, (HEIGHT / 2)+100))
        end_game = True

        for restante in [lp for lp in letras_palavra if lp['mostrando'] == False]:
            text_surface, rect = font.render(restante['letra'].upper(), fgcolor=(0, 0, 255), bgcolor=None, rotation=0, size=32)
            screen.blit(text_surface, restante['pos'])
    
    for ld in letras_digitadas:
        color = (0, 255, 0) if ld in palavra else (255, 0, 0)
        text_surface, rect = font.render(ld.upper(), fgcolor=color, bgcolor=None, rotation=0, size=32)
        screen.blit(text_surface, (88 + (letras_digitadas.index(ld) * 32), (HEIGHT / 2) - 100))

    #text_tentativas, rect = font.render(f'Tentativas: {tentativas}', fgcolor=(255, 0, 0), bgcolor=None, rotation=0, size=32)
    #screen.blit(text_tentativas, (50, (HEIGHT / 2)-200))

    if tentativas < 6:
        pygame.draw.circle(screen, (0, 0, 0), ((WIDTH / 2) + 200, 80), 20, width=2)
    if tentativas < 5:
        pygame.draw.line(screen, (0, 0, 0), ((WIDTH / 2) + 200, 100), ((WIDTH / 2) + 200, 170), width=2)
    if tentativas < 4:
        pygame.draw.line(screen, (0, 0, 0), ((WIDTH / 2) + 200, 120), ((WIDTH / 2) + 200 - 50, 100), width=2)
    if tentativas < 3:
        pygame.draw.line(screen, (0, 0, 0), ((WIDTH / 2) + 200, 120), ((WIDTH / 2) + 200 + 50, 100), width=2)
    if tentativas < 2:
        pygame.draw.line(screen, (0, 0, 0), ((WIDTH / 2) + 200, 170), ((WIDTH / 2) + 200 - 50, 190), width=2)
    if tentativas < 1:
        pygame.draw.line(screen, (0, 0, 0), ((WIDTH / 2) + 200, 170), ((WIDTH / 2) + 200 + 50, 190), width=2)

    pygame.draw.line(screen, (0, 0, 0), (WIDTH / 2, 0), ((WIDTH / 2) + 200, 0), width=6)
    pygame.draw.line(screen, (255, 0, 255), ((WIDTH / 2) + 200, 0), ((WIDTH / 2) + 200, 60), width=2)
    
    pygame.display.flip()

def handle_events():

    global tentativas

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if end_game:
                init_game()
            else:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            
                k = pygame.key.name(event.key).lower()
                if len(k) == 1:                
                    if k not in letras_digitadas:
                        letras_digitadas.append(k)
                        if k in palavra.lower():
                            for il in letras_palavra:
                                if il['letra'] == k.lower():
                                    il['mostrando'] = True
                        else:
                            tentativas = tentativas - 1
                            print(tentativas)

init_game()