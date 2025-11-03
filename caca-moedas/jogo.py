import pygame
from pygame.locals import * 
from sys import exit
import random

pygame.init()

largura = 800
altura = 600
pontuacao = 0

x = largura / 2
y = altura / 2

jogador = pygame.Rect(x, y, 40, 30)

pontos = []
for _ in range(1):
    ponto_x = random.randint(0, largura - 20) 
    ponto_y = random.randint(0, altura - 20)
    pontos.append(pygame.Rect(ponto_x, ponto_y, 15, 15))

obstaculos = []
for _ in range(5):
    while True:
        obstaculo_x = random.randint(0, largura - 20)
        obstaculo_y = random.randint(0, altura - 20)
        bolinha = pygame.Rect(obstaculo_x, obstaculo_y, 20, 20)
        if not jogador.colliderect(bolinha):
            obstaculos.append(bolinha)
            break

ultimo_tempo_mudanca = 0
intervalo_mudanca = 3

font = pygame.font.Font(None, 40)
tempo_inicial = 30
tempo_esgotado = False
relogio = pygame.time.Clock()

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo")

# Função para resetar o jogo
def reiniciar_jogo():
    global jogador, pontos, obstaculos, pontuacao, tempo_esgotado, ultimo_tempo_mudanca, ticks
    pontuacao = 0
    jogador = pygame.Rect(largura/2, altura/2, 40, 30)

    pontos = []
    for _ in range(1):
        ponto_x = random.randint(0, largura - 20) 
        ponto_y = random.randint(0, altura - 20)
        pontos.append(pygame.Rect(ponto_x, ponto_y, 15, 15))

    obstaculos = []
    for _ in range(5):
        while True:
            obstaculo_x = random.randint(0, largura - 20)
            obstaculo_y = random.randint(0, altura - 20)
            bolinha = pygame.Rect(obstaculo_x, obstaculo_y, 20, 20)
            if not jogador.colliderect(bolinha):
                obstaculos.append(bolinha)
                break

    ultimo_tempo_mudanca = 0
    tempo_esgotado = False
    pygame.time.set_timer(USEREVENT, 0)  # resetar timers
    pygame.time.get_ticks()
    return pygame.time.get_ticks() // 1000

ticks = pygame.time.get_ticks() // 1000

# Botão de reinício
botao_reiniciar = pygame.Rect(largura//2 - 80, altura//2 + 50, 160, 50)

while True:
    relogio.tick(30)
    tela.fill((0, 0, 0))
    colisao = False
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == MOUSEBUTTONDOWN and tempo_esgotado:
            if botao_reiniciar.collidepoint(event.pos):
                ticks = reiniciar_jogo()

    tempo_atual = pygame.time.get_ticks() // 1000
    if not tempo_esgotado:
        if tempo_atual - ultimo_tempo_mudanca > intervalo_mudanca:
            for bolinha in obstaculos:
                while True:
                    bolinha.x = random.randint(0, largura - 20)
                    bolinha.y = random.randint(0, altura - 20)
                    if not jogador.colliderect(bolinha):
                        break
            ultimo_tempo_mudanca = tempo_atual

    tempo_restante = tempo_inicial - (tempo_atual - ticks)

    if tempo_restante <= 0:
        tempo_restante = 0
        tempo_esgotado = True

    keys = pygame.key.get_pressed()
    if not tempo_esgotado:
        if keys[K_a]:
            jogador.x -= 20
        if keys[K_d]:
            jogador.x += 20
        if keys[K_s]:
            jogador.y += 20
        if keys[K_w]:
            jogador.y -= 20

    pygame.draw.rect(tela, (0, 200, 0), jogador) 

    for ponto in pontos:
        pygame.draw.ellipse(tela, (255, 255, 0), ponto)
        if jogador.colliderect(ponto) and not tempo_esgotado:
            pontuacao += 1
            ponto.x = random.randint(0, largura - 20)
            ponto.y = random.randint(0, altura - 20)

    for bolinha in obstaculos:
        pygame.draw.ellipse(tela, (255, 0, 0), bolinha)
        if jogador.colliderect(bolinha):
            tempo_esgotado = True
            colisao = True

    if pontuacao >= 7:
        ganhou = True
        tempo_esgotado = True
    else:
        ganhou = False

    if not tempo_esgotado:
        timer_text = font.render(f'Tempo: {tempo_restante}', True, (255, 255, 255))
        tela.blit(timer_text, (largura // 2 - timer_text.get_width() // 2, 30))
    elif ganhou:
        texto_vencedor = font.render("Parabéns você venceu o desafio", True, (255, 255, 255))
        tela.blit(texto_vencedor, (largura // 2 - texto_vencedor.get_width() // 2, altura // 2 - texto_vencedor.get_height() // 2))
    elif tempo_esgotado and colisao:
        end_text = font.render('Você esbarrou no obstáculo, PERDEU MANÉ', True, (255, 255, 255))
        tela.blit(end_text, (largura // 2 - end_text.get_width() // 2, altura // 2 - end_text.get_height() // 2))
    else:
        end_text = font.render('Tempo esgotado, PERDEU MANÉ', True, (255, 255, 255))
        tela.blit(end_text, (largura // 2 - end_text.get_width() // 2, altura // 2 - end_text.get_height() // 2))

    # Desenhar botão reiniciar se o jogo acabou
    if tempo_esgotado:
        pygame.draw.rect(tela, (100, 100, 255), botao_reiniciar, border_radius=10)
        texto_botao = font.render("Reiniciar", True, (255, 255, 255))
        tela.blit(texto_botao, (botao_reiniciar.centerx - texto_botao.get_width() // 2,
                                botao_reiniciar.centery - texto_botao.get_height() // 2))

    total_de_pontos = font.render(f"PONTUAÇÃO: {pontuacao}", True, (255, 255, 255))
    tela.blit(total_de_pontos, (10, 10))

    pygame.display.update()
