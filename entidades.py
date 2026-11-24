import pygame
import random
import math
from config import largura, altura, CIANO
from assets import imagens

class Entidade:
    def __init__(self, x, y, imagem):
        self.x = float(x)
        self.y = float(y)
        self.imagem = imagem
        self.flash_frames = 0

    def desenhar(self, tela):
        if self.flash_frames > 0:
            self.flash_frames -= 1
            branco = self.imagem.copy()
            branco.fill((255, 255, 255, 200), special_flags=pygame.BLEND_RGBA_ADD)
            tela.blit(branco, (int(self.x), int(self.y)))
        else:
            tela.blit(self.imagem, (int(self.x), int(self.y)))

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.imagem.get_width(), self.imagem.get_height())

    @property
    def largura(self):
        return self.imagem.get_width()

    @property
    def altura(self):
        return self.imagem.get_height()

    @property
    def centro(self):
        return (self.x + self.largura / 2, self.y + self.altura / 2)

class Jogador(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, imagens["jogador"])
        self.vel_base = 10
        self.invulneravel_frames = 0
        self.cooldown_tiro = 0
        self.angulo = 0
        # Power-ups ativos
        self.escudo = False
        self.triplo_frames = 0
        self.turbo_frames = 0

    @property
    def vel(self):
        return self.vel_base * (1.55 if self.turbo_frames > 0 else 1.0)

    def mover(self, teclas, touch_dir=0):
        dy = 0
        if teclas[pygame.K_UP] or teclas[pygame.K_w] or touch_dir < 0:
            dy = -self.vel
        elif teclas[pygame.K_DOWN] or teclas[pygame.K_s] or touch_dir > 0:
            dy = self.vel

        self.y = max(10, min(altura - self.altura - 10, self.y + dy))
        alvo_ang = 8 if dy < 0 else (-8 if dy > 0 else 0)
        self.angulo += (alvo_ang - self.angulo) * 0.2

        if self.invulneravel_frames > 0:
            self.invulneravel_frames -= 1
        if self.cooldown_tiro > 0:
            self.cooldown_tiro -= 1
        if self.triplo_frames > 0:
            self.triplo_frames -= 1
        if self.turbo_frames > 0:
            self.turbo_frames -= 1

    def desenhar(self, tela):
        if self.invulneravel_frames > 0 and (self.invulneravel_frames // 4) % 2 == 0:
            return
        img_rot = pygame.transform.rotate(self.imagem, self.angulo)
        rect = img_rot.get_rect(center=self.centro)
        tela.blit(img_rot, rect.topleft)

        # Barreira visual do Escudo
        if self.escudo:
            cx, cy = int(self.centro[0]), int(self.centro[1])
            surf = pygame.Surface((120, 120), pygame.SRCALPHA)
            pygame.draw.circle(surf, (0, 240, 255, 55), (60, 60), 54)
            pygame.draw.circle(surf, (*CIANO, 210), (60, 60), 54, 3)
            tela.blit(surf, (cx - 60, cy - 60))

class PowerUp(Entidade):
    TIPOS = {
        "escudo": ("pu_escudo", "ESCUDO ATIVO!", (0, 240, 255)),
        "triplo": ("pu_triplo", "TIRO TRIPLO!", (255, 220, 50)),
        "turbo":  ("pu_turbo",  "TURBO VELOCIDADE!", (50, 255, 120)),
        "vida":   ("pu_vida",   "+1 VIDA!", (255, 140, 40)),
    }

    def __init__(self, x, y, tipo=None):
        if tipo is None:
            tipo = random.choices(["escudo", "triplo", "turbo", "vida"], weights=[30, 35, 25, 10])[0]
        self.tipo = tipo
        img_key, self.texto, self.cor = self.TIPOS[tipo]
        super().__init__(x, y, imagens[img_key])
        self.vel_x = -3.5
        self.fase = random.uniform(0, math.tau)
        self.y_base = float(y)

    def mover(self):
        self.x += self.vel_x
        self.fase += 0.08
        self.y = max(20, min(altura - self.altura - 20, self.y_base + math.sin(self.fase) * 22))

    def fora_da_tela(self):
        return self.x < -60

class Missil(Entidade):
    def __init__(self, x, y, vel_y=0, triplo=False):
        img = imagens["missil_triplo"] if triplo else imagens["missil"]
        super().__init__(x, y, img)
        self.vel_x = 22.0
        self.vel_y = float(vel_y)

    def mover(self):
        self.x += self.vel_x
        self.y += self.vel_y

    def fora_da_tela(self):
        return self.x > largura + 50 or self.y < -40 or self.y > altura + 40

class TiroInimigo(Entidade):
    def __init__(self, x, y, vel_x=-8, vel_y=0, boss=False):
        img = imagens["tiro_boss"] if boss else imagens["tiro_inimigo"]
        super().__init__(x, y, img)
        self.vel_x = float(vel_x)
        self.vel_y = float(vel_y)

    def mover(self):
        self.x += self.vel_x
        self.y += self.vel_y

    def fora_da_tela(self):
        return self.x < -50 or self.x > largura + 50 or self.y < -50 or self.y > altura + 50

class Inimigo(Entidade):
    def __init__(self, vel_x=4.5, tiro_ms=1800):
        super().__init__(0, 0, imagens["inimigo"])
        self.vel_x = vel_x
        self.tiro_ms = tiro_ms
        self.reset()

    def reset(self):
        self.x = random.randint(largura + 80, largura + 700)
        self.y = random.randint(20, altura - self.altura - 20)
        self.tiros = []
        self.tempo_ultimo_tiro = pygame.time.get_ticks()

    def mover(self):
        self.x -= self.vel_x
        agora = pygame.time.get_ticks()
        if agora - self.tempo_ultimo_tiro > self.tiro_ms:
            self.tiros.append(TiroInimigo(self.x, self.y + self.altura // 2 - 12, vel_x=-8))
            self.tempo_ultimo_tiro = agora

        for t in self.tiros:
            t.mover()
        self.tiros = [t for t in self.tiros if not t.fora_da_tela()]

        if self.x < -self.largura:
            self.reset()

    def desenhar(self, tela):
        super().desenhar(tela)
        for t in self.tiros:
            t.desenhar(tela)

class VilaoMedio(Entidade):
    def __init__(self, x, y, direcao_vertical=1):
        super().__init__(x, y, imagens["vilao_medio"])
        self.vida = 4
        self.tiros = []
        self.tempo_ultimo_tiro = pygame.time.get_ticks()
        self.vel_x = 0.0
        self.vel_y = 2.5 * direcao_vertical
        self.ativo = True

    def mover(self):
        agora = pygame.time.get_ticks()
        if agora - self.tempo_ultimo_tiro > 1400:
            for off in (-20, 0, 20):
                self.tiros.append(TiroInimigo(self.x, self.y + self.altura // 2 + off, vel_x=-6))
            self.tempo_ultimo_tiro = agora

        for t in self.tiros:
            t.mover()
        self.tiros = [t for t in self.tiros if not t.fora_da_tela()]

        self.x += self.vel_x
        self.y += self.vel_y
        if self.y <= 10 or self.y >= altura - self.altura - 10:
            self.vel_y *= -1

    def desenhar(self, tela):
        if not self.ativo:
            return
        super().desenhar(tela)
        for t in self.tiros:
            t.desenhar(tela)

class Boss(Entidade):
    def __init__(self, vida_max=25):
        super().__init__(largura + 200, altura // 2 - 100, imagens["boss"])
        self.vida_max = vida_max
        self.vida = vida_max
        self.tiros = []
        self.tempo_ultimo_tiro = pygame.time.get_ticks()
        self.direcao = 1
        self.angulos = [(-10, 0), (-8, -4), (-8, 4), (-6, -7), (-6, 7)]

    def iniciar(self, vida_max):
        self.vida_max = vida_max
        self.vida = vida_max
        self.x = largura - 240
        self.y = altura // 2 - self.altura // 2
        self.tiros.clear()
        self.tempo_ultimo_tiro = pygame.time.get_ticks()

    def mover(self):
        self.y += self.direcao * 3.5
        if self.y <= 20:
            self.direcao = 1
        elif self.y >= altura - self.altura - 20:
            self.direcao = -1

        agora = pygame.time.get_ticks()
        if agora - self.tempo_ultimo_tiro > 1100:
            for dx, dy in self.angulos:
                self.tiros.append(TiroInimigo(self.x, self.y + self.altura // 2, vel_x=dx, vel_y=dy, boss=True))
            self.tempo_ultimo_tiro = agora

        for t in self.tiros:
            t.mover()
        self.tiros = [t for t in self.tiros if not t.fora_da_tela()]

    def desenhar(self, tela):
        super().desenhar(tela)
        for t in self.tiros:
            t.desenhar(tela)
        bw = 460
        bx = largura // 2 - bw // 2
        pygame.draw.rect(tela, (40, 10, 20), (bx, 20, bw, 22), border_radius=8)
        prop = max(0.0, self.vida / self.vida_max)
        pygame.draw.rect(tela, (255, 60, 80), (bx, 20, int(bw * prop), 22), border_radius=8)
        pygame.draw.rect(tela, (255, 255, 255), (bx, 20, bw, 22), 2, border_radius=8)
