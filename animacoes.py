import pygame
import random
import math
from config import fonte_pequena

class Particula:
    def __init__(self, x, y, vx, vy, cor, raio, vida_frames):
        self.x = float(x)
        self.y = float(y)
        self.vx = vx
        self.vy = vy
        self.cor = cor
        self.raio = raio
        self.vida = vida_frames
        self.vida_max = vida_frames

    def atualizar(self):
        self.x += self.vx
        self.y += self.vy
        self.vida -= 1
        self.vx *= 0.96
        self.vy *= 0.96

    def desenhar(self, tela):
        if self.vida <= 0:
            return
        alpha = int(255 * (self.vida / self.vida_max))
        r = max(1, int(self.raio * (self.vida / self.vida_max)))
        surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.cor, alpha), (r, r), r)
        tela.blit(surf, (int(self.x - r), int(self.y - r)))

class OndaChoque:
    def __init__(self, x, y, cor=(255, 200, 80), raio_max=90):
        self.x = int(x)
        self.y = int(y)
        self.cor = cor
        self.raio = 6
        self.raio_max = raio_max
        self.ativo = True

    def atualizar(self):
        self.raio += 5
        if self.raio >= self.raio_max:
            self.ativo = False

    def desenhar(self, tela):
        if not self.ativo:
            return
        alpha = max(0, int(220 * (1 - self.raio / self.raio_max)))
        surf = pygame.Surface((self.raio * 2, self.raio * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.cor, alpha), (self.raio, self.raio), self.raio, 4)
        tela.blit(surf, (self.x - self.raio, self.y - self.raio))

class TextoFlutuante:
    def __init__(self, x, y, texto, cor=(255, 255, 100)):
        self.x = float(x)
        self.y = float(y)
        self.texto = texto
        self.cor = cor
        self.vida = 50

    def atualizar(self):
        self.y -= 1.2
        self.vida -= 1

    def desenhar(self, tela):
        if self.vida <= 0:
            return
        surf = fonte_pequena.render(self.texto, True, self.cor)
        surf.set_alpha(int(255 * (self.vida / 50)))
        tela.blit(surf, (int(self.x), int(self.y)))

class SistemaEfeitos:
    def __init__(self):
        self.particulas = []
        self.ondas = []
        self.textos = []
        self.shake_frames = 0
        self.shake_intensidade = 0

    def explosao(self, x, y, escala=1.0, cores=None, ativar_particulas=True, ativar_shake=True):
        if cores is None:
            cores = [(255, 220, 80), (255, 120, 20), (255, 50, 50), (255, 255, 255)]
        if ativar_particulas:
            qtd = int(28 * escala)
            for _ in range(qtd):
                ang = random.uniform(0, math.tau)
                vel = random.uniform(1.5, 7.5 * escala)
                cor = random.choice(cores)
                self.particulas.append(
                    Particula(x, y, math.cos(ang) * vel, math.sin(ang) * vel, cor, random.randint(3, 8), random.randint(20, 42))
                )
            self.ondas.append(OndaChoque(x, y, cores[0], int(75 * escala)))
        if ativar_shake:
            self.tremer(int(10 * escala), int(6 * escala))

    def rastro(self, x, y, cor=(0, 200, 255)):
        self.particulas.append(
            Particula(x, y + random.randint(-6, 6), random.uniform(-4.5, -2.0), random.uniform(-0.6, 0.6), cor, random.randint(2, 5), 16)
        )

    def adicionar_texto(self, x, y, texto, cor=(255, 255, 100)):
        self.textos.append(TextoFlutuante(x, y, texto, cor))

    def tremer(self, duracao, intensidade):
        self.shake_frames = max(self.shake_frames, duracao)
        self.shake_intensidade = max(self.shake_intensidade, intensidade)

    def get_offset_shake(self):
        if self.shake_frames > 0:
            self.shake_frames -= 1
            return (random.randint(-self.shake_intensidade, self.shake_intensidade),
                    random.randint(-self.shake_intensidade, self.shake_intensidade))
        return (0, 0)

    def atualizar(self):
        for p in self.particulas:
            p.atualizar()
        self.particulas = [p for p in self.particulas if p.vida > 0]

        for o in self.ondas:
            o.atualizar()
        self.ondas = [o for o in self.ondas if o.ativo]

        for t in self.textos:
            t.atualizar()
        self.textos = [t for t in self.textos if t.vida > 0]

    def desenhar(self, tela):
        for o in self.ondas:
            o.desenhar(tela)
        for p in self.particulas:
            p.desenhar(tela)
        for t in self.textos:
            t.desenhar(tela)
