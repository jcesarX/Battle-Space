import pygame
from config import fonte_padrao, fonte_pequena, BRANCO, CIANO, VERDE, VERMELHO, AMARELO, CINZA, largura, altura

class Botao:
    def __init__(self, texto, x, y, w, h, acao, cor_borda=CIANO):
        self.texto = texto
        self.rect = pygame.Rect(x, y, w, h)
        self.acao = acao
        self.cor_borda = cor_borda

    def desenhar(self, tela):
        mouse_pos = pygame.mouse.get_pos()
        hover = self.rect.collidepoint(mouse_pos)
        cor_fundo = (40, 70, 110) if hover else CINZA
        pygame.draw.rect(tela, cor_fundo, self.rect, border_radius=12)
        pygame.draw.rect(tela, self.cor_borda if hover else (120, 140, 180), self.rect, 3, border_radius=12)
        txt = fonte_padrao.render(self.texto, True, BRANCO)
        tela.blit(txt, txt.get_rect(center=self.rect.center))

    def checar_clique(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect.collidepoint(evento.pos):
                self.acao()

class ControlesTouch:
    def __init__(self):
        self.btn_up    = pygame.Rect(40, altura - 210, 95, 85)
        self.btn_down  = pygame.Rect(40, altura - 110, 95, 85)
        self.btn_fire  = pygame.Rect(largura - 155, altura - 165, 115, 115)
        self.btn_pause = pygame.Rect(largura - 90, 20, 65, 50)

    def desenhar(self, tela):
        overlay = pygame.Surface((largura, altura), pygame.SRCALPHA)
        for rect, label in [(self.btn_up, "▲"), (self.btn_down, "▼"), (self.btn_fire, "FOGO"), (self.btn_pause, "||")]:
            pygame.draw.rect(overlay, (255, 255, 255, 45), rect, border_radius=16)
            pygame.draw.rect(overlay, (0, 240, 255, 130), rect, 2, border_radius=16)
            txt = fonte_pequena.render(label, True, (255, 255, 255, 210))
            overlay.blit(txt, txt.get_rect(center=rect.center))
        tela.blit(overlay, (0, 0))

class HUD:
    def __init__(self, max_vida=5):
        self.pontos = 0
        self.max_vida = max_vida
        self.vida_atual = max_vida

    def desenhar(self, tela, jogador=None):
        txt = fonte_padrao.render(f"PONTOS: {self.pontos}", True, BRANCO)
        tela.blit(txt, (24, 18))

        bw, bh = 220, 20
        pygame.draw.rect(tela, (50, 20, 30), (24, 65, bw, bh), border_radius=6)
        prop = max(0.0, self.vida_atual / self.max_vida)
        cor = VERDE if prop > 0.4 else VERMELHO
        pygame.draw.rect(tela, cor, (24, 65, int(bw * prop), bh), border_radius=6)
        pygame.draw.rect(tela, BRANCO, (24, 65, bw, bh), 2, border_radius=6)

        # Indicadores de Power-ups ativos
        if jogador:
            y_pu = 98
            if jogador.escudo:
                t = fonte_pequena.render("ESCUDO: ATIVO", True, CIANO)
                tela.blit(t, (24, y_pu))
                y_pu += 28
            if jogador.triplo_frames > 0:
                seg = jogador.triplo_frames / 60.0
                t = fonte_pequena.render(f"TIRO 3X: {seg:.1f}s", True, AMARELO)
                tela.blit(t, (24, y_pu))
                y_pu += 28
            if jogador.turbo_frames > 0:
                seg = jogador.turbo_frames / 60.0
                t = fonte_pequena.render(f"TURBO: {seg:.1f}s", True, VERDE)
                tela.blit(t, (24, y_pu))
