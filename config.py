import pygame
import json
import os

largura, altura = 1280, 720
FPS = 60

# Paleta de cores Neon / Espacial
BRANCO   = (255, 255, 255)
PRETO    = (10, 10, 20)
CIANO    = (0, 240, 255)
VERDE    = (50, 255, 120)
VERMELHO = (255, 60, 80)
AMARELO  = (255, 220, 50)
ROXO     = (180, 70, 255)
LARANJA  = (255, 140, 40)
CINZA    = (40, 45, 65)

SETTINGS_FILE = "settings.json"
HIGHSCORES_FILE = "highscores.json"

DEFAULT_SETTINGS = {
    "vol_musica": 0.5,
    "vol_sfx": 0.7,
    "dificuldade": "Normal",   # Facil, Normal, Dificil
    "particulas": True,
    "screen_shake": True,
    "controles_touch": True
}

def carregar_config():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {**DEFAULT_SETTINGS, **data}
        except Exception:
            pass
    return DEFAULT_SETTINGS.copy()

def salvar_config(cfg):
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=4)
    except Exception as e:
        print(f"Erro ao salvar configurações: {e}")

def carregar_recordes():
    if os.path.exists(HIGHSCORES_FILE):
        try:
            with open(HIGHSCORES_FILE, "r", encoding="utf-8") as f:
                dados = json.load(f)
                if isinstance(dados, list):
                    return dados[:5]
        except Exception:
            pass
    return []

def registrar_recorde(pontos, dificuldade):
    if pontos <= 0:
        return False
    recordes = carregar_recordes()
    eh_novo_top1 = (len(recordes) == 0) or (pontos > recordes[0].get("pontos", 0))
    recordes.append({"pontos": int(pontos), "dificuldade": dificuldade})
    recordes.sort(key=lambda r: r["pontos"], reverse=True)
    recordes = recordes[:5]
    try:
        with open(HIGHSCORES_FILE, "w", encoding="utf-8") as f:
            json.dump(recordes, f, indent=4)
    except Exception as e:
        print(f"Erro ao salvar recordes: {e}")
    return eh_novo_top1

config_atual = carregar_config()

DIFICULDADES = {
    "Facil":   {"vel_inimigo": 3.0, "tiro_ms": 2400, "vida_jogador": 7, "vida_boss": 15, "chance_powerup": 0.35},
    "Normal":  {"vel_inimigo": 4.5, "tiro_ms": 1800, "vida_jogador": 5, "vida_boss": 25, "chance_powerup": 0.28},
    "Dificil": {"vel_inimigo": 6.5, "tiro_ms": 1200, "vida_jogador": 3, "vida_boss": 40, "chance_powerup": 0.22},
}

pygame.init()
pygame.font.init()

fonte_pequena   = pygame.font.SysFont("Arial", 24, bold=True)
fonte_padrao    = pygame.font.SysFont("Arial", 36, bold=True)
fonte_titulo    = pygame.font.SysFont("Arial", 76, bold=True)
fonte_game_over = pygame.font.SysFont("Arial", 90, bold=True)
