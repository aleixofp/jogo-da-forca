from random import random
import sys, pygame, unidecode

pygame.init()

SIZE = WIDTH, HEIGHT = 640, 480

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Jogo da Forca')

font = pygame.freetype.SysFont('Arial', 12, bold=True, italic=False)

running = False

# lê as palavras do palavra.txt
with open ('palavras.txt', 'r', encoding='UTF-8') as f:
    palavras = f.read().splitlines()

# inicia um novo jogo
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

    # pega o palavra aleatória    
    palavra = unidecode.unidecode(palavras[int(random() * len(palavras))]) 

    # cria um array com informações de cada letra da palavra, como:
    # letra: letra da palavra
    # mostrando: se a letra está sendo mostrada ou não
    # pos: posição da letra no quadro do jogo
    for i in range(len(palavra)):
        letras_palavra.append({'letra': palavra[i].lower(), 'pos': ((40+(i*32)+16)+4, (HEIGHT / 2)-30), 'mostrando': False})

    game_loop()

# loop principal
def game_loop():
    while running:
        update()
        render()

# atualiza o jogo
def update():
    handle_events()

# desenha o jogo
def render():

    global end_game

    # preenche a tela com a cor preta
    screen.fill((255, 255, 255))

    # desenha as letras que o usuário acertou
    for i in range(len(palavra)):
        pygame.draw.line(screen, (0, 0, 255), (40+(i*32)+16, (HEIGHT / 2)), (70+(i*32)+16, (HEIGHT / 2)), width=4)
        if letras_palavra[i]['mostrando']:
            text_surface, rect = font.render(palavra[i].upper(), fgcolor=(234, 100, 5), bgcolor=None, rotation=0, size=32)
            screen.blit(text_surface, letras_palavra[i]['pos'])

    # lógica de fim de jogo (vitória)
    # caso todas letras estiverem 'mostrando' na tela, e ainda não acabou as tentativas
    # quer dizer que o jogador ganhou
    if len([x for x in letras_palavra if x['mostrando'] == False]) == 0:
        text_surface, rect = font.render('Parabéns!', fgcolor=(255, 0, 0), bgcolor=None, rotation=0, size=48)
        screen.blit(text_surface, (50, (HEIGHT / 2)+100))
        end_game = True

    # lógica de fim de jogo (derrota)
    # se tentativas = 0, o jogo acaba e o usuário perde
    if tentativas == 0:
        text_surface, rect = font.render('Game Over!', fgcolor=(255, 0, 0), bgcolor=None, rotation=0, size=48)
        screen.blit(text_surface, (50, (HEIGHT / 2)+100))
        end_game = True

        # desenha as letras que faltaram na palavra
        for restante in [lp for lp in letras_palavra if lp['mostrando'] == False]:
            text_surface, rect = font.render(restante['letra'].upper(), fgcolor=(0, 0, 255), bgcolor=None, rotation=0, size=32)
            screen.blit(text_surface, restante['pos'])
    
    # desenha as letras que o usuário digitou
    # a cor depende se a letra está na palavrao ou não: verde está, vermelho não está
    for ld in letras_digitadas:
        color = (0, 255, 0) if ld in palavra else (255, 0, 0)
        text_surface, rect = font.render(ld.upper(), fgcolor=color, bgcolor=None, rotation=0, size=32)
        screen.blit(text_surface, (88 + (letras_digitadas.index(ld) * 32), (HEIGHT / 2) - 100))

    # desenha a estrutura da forca
    pygame.draw.line(screen, (0, 0, 0), (WIDTH / 2, 0), ((WIDTH / 2) + 200, 0), width=6)
    pygame.draw.line(screen, (255, 0, 255), ((WIDTH / 2) + 200, 0), ((WIDTH / 2) + 200, 60), width=2)

    # desenha o personagem de acordo com as tentativas
    # ordem: cabeça, corpo, braço direito, braço esquerdo, perna direita e perna esquerda
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
    
    pygame.display.flip()

# eventos do teclado
def handle_events():

    global tentativas

    # eventos detectados
    for event in pygame.event.get():

        # se clicar no x, fecha o jogo
        if event.type == pygame.QUIT: sys.exit()

        # se alguma tecla for pressionada
        if event.type == pygame.KEYDOWN:

            # se o jogo tiver finalizado, inicia um novo
            if end_game:
                init_game()
            else:

                # se a tecla digitada for "ESC", fecha o jogo
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            
                # captura a letra digitada, e transforma em minúsculo
                k = pygame.key.name(event.key).lower()

                # se for uma letra (não pode ser espaço, shift, enter, ctrl etc)
                if len(k) == 1:

                    # se o usuário ainda não tentou adivinhar a letra
                    if k not in letras_digitadas:
                        letras_digitadas.append(k)

                        # se a letra está na palavra
                        if k in palavra.lower():
                            # percorre a lista "letras_palavra" que foi populada no começo do jogo
                            # para setá-la para 'mostrando', para que a letra seja renderizada
                            for il in letras_palavra:
                                if il['letra'] == k.lower():
                                    il['mostrando'] = True
                                    
                        # se não tiver, tentativas diminui
                        else:
                            tentativas = tentativas - 1
                            print(tentativas)

init_game()