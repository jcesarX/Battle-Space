import pygame
import os
from config import CIANO, VERMELHO, AMARELO, ROXO, BRANCO, VERDE, LARANJA

pygame.init()
try:
    pygame.mixer.init()
except Exception:
    pass

def criar_nave_jogador():
    surf = pygame.Surface((90, 60), pygame.SRCALPHA)
    pygame.draw.polygon(surf, (0, 150, 255, 140), [(0, 20), (20, 30), (0, 40)])
    pygame.draw.polygon(surf, (30, 100, 200), [(15, 5), (65, 22), (15, 55), (30, 30)])
    pygame.draw.polygon(surf, CIANO, [(15, 5), (65, 22), (15, 55), (30, 30)], 2)
    pygame.draw.polygon(surf, (220, 240, 255), [(20, 20), (88, 30), (20, 40), (10, 30)])
    pygame.draw.ellipse(surf, (0, 255, 255), (42, 23, 22, 14))
    return surf

def criar_missil(cor=(0, 200, 255)):
    surf = pygame.Surface((42, 16), pygame.SRCALPHA)
    pygame.draw.ellipse(surf, (*cor, 130), (0, 0, 42, 16))
    pygame.draw.rect(surf, BRANCO, (8, 5, 28, 6), border_radius=3)
    return surf

def criar_inimigo():
    surf = pygame.Surface((66, 60), pygame.SRCALPHA)
    pygame.draw.polygon(surf, (180, 30, 50), [(64, 10), (5, 30), (64, 50), (48, 30)])
    pygame.draw.polygon(surf, VERMELHO, [(64, 10), (5, 30), (64, 50), (48, 30)], 2)
    pygame.draw.circle(surf, AMARELO, (36, 30), 8)
    return surf

def criar_vilao_medio():
    surf = pygame.Surface((110, 96), pygame.SRCALPHA)
    pygame.draw.polygon(surf, (120, 20, 160), [(105, 8), (15, 28), (5, 48), (15, 68), (105, 88), (80, 48)])
    pygame.draw.polygon(surf, ROXO, [(105, 8), (15, 28), (5, 48), (15, 68), (105, 88), (80, 48)], 3)
    pygame.draw.circle(surf, (255, 80, 200), (52, 48), 15)
    pygame.draw.circle(surf, BRANCO, (52, 48), 6)
    return surf

def criar_boss():
    surf = pygame.Surface((210, 200), pygame.SRCALPHA)
    pygame.draw.polygon(surf, (90, 10, 30), [(200, 15), (40, 55), (10, 100), (40, 145), (200, 185), (165, 100)])
    pygame.draw.polygon(surf, VERMELHO, [(200, 15), (40, 55), (10, 100), (40, 145), (200, 185), (165, 100)], 4)
    pygame.draw.circle(surf, (255, 50, 0, 180), (100, 100), 34)
    pygame.draw.circle(surf, AMARELO, (100, 100), 20)
    pygame.draw.circle(surf, BRANCO, (100, 100), 9)
    return surf

def criar_tiro_inimigo(cor=(255, 80, 80)):
    surf = pygame.Surface((24, 24), pygame.SRCALPHA)
    pygame.draw.circle(surf, (*cor, 110), (12, 12), 12)
    pygame.draw.circle(surf, cor, (12, 12), 7)
    pygame.draw.circle(surf, BRANCO, (12, 12), 3)
    return surf

def criar_powerup(cor, simbolo):
    surf = pygame.Surface((44, 44), pygame.SRCALPHA)
    pygame.draw.circle(surf, (*cor, 90), (22, 22), 22)
    pygame.draw.circle(surf, (*cor, 210), (22, 22), 16)
    pygame.draw.circle(surf, BRANCO, (22, 22), 16, 2)
    fonte = pygame.font.SysFont("Arial", 20, bold=True)
    txt = fonte.render(simbolo, True, (15, 15, 25))
    surf.blit(txt, txt.get_rect(center=(22, 22)))
    return surf

imagens = {
    "jogador": criar_nave_jogador(),
    "missil": criar_missil(CIANO),
    "missil_triplo": criar_missil(AMARELO),
    "inimigo": criar_inimigo(),
    "vilao_medio": criar_vilao_medio(),
    "boss": criar_boss(),
    "tiro_inimigo": criar_tiro_inimigo((255, 70, 70)),
    "tiro_boss": criar_tiro_inimigo((255, 180, 0)),
    "pu_escudo": criar_powerup(CIANO, "E"),
    "pu_triplo": criar_powerup(AMARELO, "3X"),
    "pu_turbo": criar_powerup(VERDE, "V"),
    "pu_vida": criar_powerup(LARANJA, "+"),
}

def carregar_som(caminho):
    if not os.path.exists(caminho):
        return None
    try:
        return pygame.mixer.Sound(caminho)
    except Exception:
        return None

sons = {
    "tela_inicial": "sounds/music_tela_inicial.mp3",
    "fundo_batalha": "sounds/music_fundo_batalha.mp3",
    "boss": "sounds/music_boss.mp3",
    "explosao": carregar_som("sounds/music_explosao.wav"),
    "start": carregar_som("sounds/music_start.wav"),
    "tiro": carregar_som("sounds/music_tiro_laser.wav"),
}

def tocar_som(nome, volume=0.7):
    som = sons.get(nome)
    if som:
        som.set_volume(volume)
        som.play()

def tocar_musica(nome, volume=0.5):
    caminho = sons.get(nome)
    if caminho and os.path.exists(caminho):
        try:
            pygame.mixer.music.load(caminho)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)
        except Exception:
            pass
