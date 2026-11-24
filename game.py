import pygame
import sys
import random
from config import (
    largura, altura, FPS, BRANCO, CIANO, VERMELHO, AMARELO, VERDE, PRETO,
    fonte_titulo, fonte_padrao, fonte_pequena, fonte_game_over,
    config_atual, salvar_config, DIFICULDADES,
    carregar_recordes, registrar_recorde
)
from assets import tocar_som, tocar_musica
from entidades import Jogador, Missil, Inimigo, Boss, VilaoMedio, PowerUp
from interface import Botao, HUD, ControlesTouch
from animacoes import SistemaEfeitos

class FundoEspacial:
    def __init__(self):
        self.camadas = []
        for qtd, vel, raio, cor in [
            (70, 0.6, 1, (130, 150, 200)),
            (45, 1.6, 2, (190, 220, 255)),
            (20, 3.2, 3, (255, 255, 255)),
        ]:
            estrelas = [[random.randint(0, largura), random.randint(0, altura)] for _ in range(qtd)]
            self.camadas.append({"estrelas": estrelas, "vel": vel, "raio": raio, "cor": cor})

    def atualizar(self):
        for c in self.camadas:
            for e in c["estrelas"]:
                e[0] -= c["vel"]
                if e[0] < 0:
                    e[0] = largura
                    e[1] = random.randint(0, altura)

    def desenhar(self, tela):
        tela.fill(PRETO)
        for c in self.camadas:
            for e in c["estrelas"]:
                pygame.draw.circle(tela, c["cor"], (int(e[0]), int(e[1])), c["raio"])

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.canvas = pygame.Surface((largura, altura))
        self.clock = pygame.time.Clock()
        self.estado = "menu"
        self.fundo = FundoEspacial()
        self.efeitos = SistemaEfeitos()
        self.touch = ControlesTouch()
        self.pausado = False
        self.novo_recorde = False

        cx = largura // 2 - 160
        self.btn_jogar    = Botao("Iniciar Jogo", cx, 290, 320, 60, self.iniciar_jogo)
        self.btn_recordes = Botao("Recordes", cx, 368, 320, 60, self.abrir_recordes, AMARELO)
        self.btn_config   = Botao("Configurações", cx, 446, 320, 60, self.abrir_config)
        self.btn_sair     = Botao("Sair", cx, 524, 320, 60, self.sair_jogo, VERMELHO)

        self.btn_reiniciar = Botao("Jogar Novamente", cx, 440, 320, 62, self.iniciar_jogo)
        self.btn_menu      = Botao("Voltar ao Menu", cx, 525, 320, 62, self.voltar_menu)
        self.btn_voltar_rec = Botao("Voltar ao Menu", cx, 560, 320, 60, self.voltar_menu, CIANO)

        self.criar_botoes_config()
        self.resetar()

    def criar_botoes_config(self):
        cx = largura // 2 - 220
        self.botoes_config = [
            Botao("", cx, 180, 440, 52, self.toggle_musica),
            Botao("", cx, 250, 440, 52, self.toggle_sfx),
            Botao("", cx, 320, 440, 52, self.toggle_dificuldade),
            Botao("", cx, 390, 440, 52, self.toggle_particulas),
            Botao("", cx, 460, 440, 52, self.toggle_touch),
            Botao("Salvar e Voltar", largura // 2 - 160, 550, 320, 60, self.voltar_menu, AMARELO),
        ]
        self.atualizar_textos_config()

    def atualizar_textos_config(self):
        self.botoes_config[0].texto = f"Música: {int(config_atual['vol_musica'] * 100)}%"
        self.botoes_config[1].texto = f"Efeitos (SFX): {int(config_atual['vol_sfx'] * 100)}%"
        self.botoes_config[2].texto = f"Dificuldade: {config_atual['dificuldade']}"
        self.botoes_config[3].texto = f"Partículas/Shake: {'ON' if config_atual['particulas'] else 'OFF'}"
        self.botoes_config[4].texto = f"Controles Touch: {'ON' if config_atual['controles_touch'] else 'OFF'}"

    def toggle_musica(self):
        config_atual["vol_musica"] = round((config_atual["vol_musica"] + 0.25) % 1.25, 2)
        try:
            pygame.mixer.music.set_volume(config_atual["vol_musica"])
        except Exception:
            pass
        salvar_config(config_atual)
        self.atualizar_textos_config()

    def toggle_sfx(self):
        config_atual["vol_sfx"] = round((config_atual["vol_sfx"] + 0.25) % 1.25, 2)
        salvar_config(config_atual)
        self.atualizar_textos_config()

    def toggle_dificuldade(self):
        ordem = ["Facil", "Normal", "Dificil"]
        idx = (ordem.index(config_atual["dificuldade"]) + 1) % len(ordem)
        config_atual["dificuldade"] = ordem[idx]
        salvar_config(config_atual)
        self.atualizar_textos_config()

    def toggle_particulas(self):
        novo = not config_atual["particulas"]
        config_atual["particulas"] = novo
        config_atual["screen_shake"] = novo
        salvar_config(config_atual)
        self.atualizar_textos_config()

    def toggle_touch(self):
        config_atual["controles_touch"] = not config_atual["controles_touch"]
        salvar_config(config_atual)
        self.atualizar_textos_config()

    def abrir_config(self):
        self.estado = "config"

    def abrir_recordes(self):
        self.estado = "recordes"

    def voltar_menu(self):
        self.estado = "menu"
        tocar_musica("tela_inicial", config_atual["vol_musica"])

    def sair_jogo(self):
        pygame.quit()
        sys.exit()

    def resetar(self):
        dif = DIFICULDADES[config_atual["dificuldade"]]
        self.jogador = Jogador(120, altura // 2 - 30)
        self.misseis = []
        self.powerups = []
        self.inimigos = [Inimigo(dif["vel_inimigo"], dif["tiro_ms"]) for _ in range(3)]
        self.viloes_medios = []
        self.viloes_derrotados = False
        self.boss = Boss(dif["vida_boss"])
        self.boss_ativo = False
        self.hud = HUD(dif["vida_jogador"])
        self.efeitos = SistemaEfeitos()
        self.pausado = False
        self.novo_recorde = False

    def iniciar_jogo(self):
        tocar_som("start", config_atual["vol_sfx"])
        tocar_musica("fundo_batalha", config_atual["vol_musica"])
        self.resetar()
        self.estado = "jogando"

    def disparar_jogador(self):
        if self.jogador.cooldown_tiro == 0:
            x_tiro = self.jogador.x + self.jogador.largura - 10
            y_tiro = self.jogador.y + self.jogador.altura // 2 - 8
            if self.jogador.triplo_frames > 0:
                self.misseis.append(Missil(x_tiro, y_tiro, vel_y=0, triplo=True))
                self.misseis.append(Missil(x_tiro, y_tiro - 12, vel_y=-4.5, triplo=True))
                self.misseis.append(Missil(x_tiro, y_tiro + 12, vel_y=4.5, triplo=True))
            else:
                self.misseis.append(Missil(x_tiro, y_tiro))
            self.jogador.cooldown_tiro = 6 if self.jogador.turbo_frames > 0 else 12
            tocar_som("tiro", config_atual["vol_sfx"])

    def tentar_dropar_powerup(self, x, y, forcar=False):
        chance = DIFICULDADES[config_atual["dificuldade"]]["chance_powerup"]
        if forcar or random.random() < chance:
            self.powerups.append(PowerUp(x, y))

    def aplicar_powerup(self, pu):
        if pu.tipo == "escudo":
            self.jogador.escudo = True
        elif pu.tipo == "triplo":
            self.jogador.triplo_frames = 8 * FPS
        elif pu.tipo == "turbo":
            self.jogador.turbo_frames = 8 * FPS
        elif pu.tipo == "vida":
            self.hud.vida_atual = min(self.hud.max_vida, self.hud.vida_atual + 1)
        self.efeitos.adicionar_texto(self.jogador.x, self.jogador.y - 20, pu.texto, pu.cor)
        tocar_som("start", config_atual["vol_sfx"])

    def finalizar_partida(self, estado_final):
        self.novo_recorde = registrar_recorde(self.hud.pontos, config_atual["dificuldade"])
        self.estado = estado_final
        tocar_musica("tela_inicial", config_atual["vol_musica"])

    def sofrer_dano(self):
        if self.jogador.invulneravel_frames > 0:
            return
        if self.jogador.escudo:
            self.jogador.escudo = False
            self.jogador.invulneravel_frames = 45
            self.efeitos.explosao(*self.jogador.centro, escala=0.9, cores=[CIANO, BRANCO], ativar_particulas=config_atual["particulas"], ativar_shake=config_atual["screen_shake"])
            self.efeitos.adicionar_texto(self.jogador.x, self.jogador.y - 20, "ESCUDO QUEBRADO!", CIANO)
            return

        self.hud.vida_atual -= 1
        self.jogador.invulneravel_frames = 75
        self.efeitos.explosao(*self.jogador.centro, escala=0.8, ativar_particulas=config_atual["particulas"], ativar_shake=config_atual["screen_shake"])
        if self.hud.vida_atual <= 0:
            self.finalizar_partida("game_over")

    def atualizar_jogo(self):
        teclas = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()

        touch_dir = 0
        if config_atual["controles_touch"] and mouse_pressed:
            if self.touch.btn_up.collidepoint(mouse_pos):
                touch_dir = -1
            elif self.touch.btn_down.collidepoint(mouse_pos):
                touch_dir = 1
            elif self.touch.btn_fire.collidepoint(mouse_pos):
                self.disparar_jogador()

        if teclas[pygame.K_SPACE]:
            self.disparar_jogador()

        self.jogador.mover(teclas, touch_dir)
        if config_atual["particulas"]:
            cor_rastro = VERDE if self.jogador.turbo_frames > 0 else CIANO
            self.efeitos.rastro(self.jogador.x + 5, self.jogador.y + self.jogador.altura // 2, cor=cor_rastro)

        for m in self.misseis[:]:
            m.mover()
            if m.fora_da_tela():
                self.misseis.remove(m)

        # Atualizar Power-ups
        for pu in self.powerups[:]:
            pu.mover()
            if pu.get_rect().colliderect(self.jogador.get_rect()):
                self.aplicar_powerup(pu)
                self.powerups.remove(pu)
            elif pu.fora_da_tela():
                self.powerups.remove(pu)

        # Spawn Vilões Médios
        if 15 <= self.hud.pontos < 30 and not self.viloes_medios and not self.viloes_derrotados:
            self.viloes_medios = [
                VilaoMedio(largura - 160, altura // 4, -1),
                VilaoMedio(largura - 160, 3 * altura // 4, 1),
            ]

        # Atualizar Vilões Médios
        for v in self.viloes_medios[:]:
            v.mover()
            for m in self.misseis[:]:
                if m.get_rect().colliderect(v.get_rect()):
                    v.vida -= 1
                    v.flash_frames = 5
                    self.misseis.remove(m)
                    if v.vida <= 0:
                        tocar_som("explosao", config_atual["vol_sfx"])
                        self.efeitos.explosao(*v.centro, escala=1.3, ativar_particulas=config_atual["particulas"], ativar_shake=config_atual["screen_shake"])
                        self.efeitos.adicionar_texto(*v.centro, "+5", AMARELO)
                        self.tentar_dropar_powerup(*v.centro, forcar=True)
                        self.hud.pontos += 5
                        self.viloes_medios.remove(v)
                        if not self.viloes_medios:
                            self.viloes_derrotados = True
                        break
            for t in v.tiros[:]:
                if t.get_rect().colliderect(self.jogador.get_rect()):
                    v.tiros.remove(t)
                    self.sofrer_dano()

        # Spawn Boss
        if self.hud.pontos >= 30 and not self.boss_ativo and self.viloes_derrotados:
            self.boss_ativo = True
            self.boss.iniciar(DIFICULDADES[config_atual["dificuldade"]]["vida_boss"])
            self.inimigos.clear()
            tocar_musica("boss", config_atual["vol_musica"])

        # Atualizar Boss ou Inimigos Comuns
        if self.boss_ativo:
            self.boss.mover()
            for m in self.misseis[:]:
                if m.get_rect().colliderect(self.boss.get_rect()):
                    self.boss.vida -= 1
                    self.boss.flash_frames = 4
                    self.misseis.remove(m)
                    if self.boss.vida <= 0:
                        tocar_som("explosao", config_atual["vol_sfx"])
                        self.efeitos.explosao(*self.boss.centro, escala=2.5, ativar_particulas=config_atual["particulas"], ativar_shake=config_atual["screen_shake"])
                        self.hud.pontos += 25
                        self.boss_ativo = False
                        self.finalizar_partida("vitoria")
                        break
            for t in self.boss.tiros[:]:
                if t.get_rect().colliderect(self.jogador.get_rect()):
                    self.boss.tiros.remove(t)
                    self.sofrer_dano()
        else:
            for ini in self.inimigos:
                ini.mover()
                for m in self.misseis[:]:
                    if m.get_rect().colliderect(ini.get_rect()):
                        tocar_som("explosao", config_atual["vol_sfx"])
                        self.efeitos.explosao(*ini.centro, escala=0.9, ativar_particulas=config_atual["particulas"], ativar_shake=config_atual["screen_shake"])
                        self.efeitos.adicionar_texto(*ini.centro, "+1", CIANO)
                        self.tentar_dropar_powerup(*ini.centro)
                        self.hud.pontos += 1
                        ini.reset()
                        self.misseis.remove(m)
                        break
                if ini.get_rect().colliderect(self.jogador.get_rect()):
                    ini.reset()
                    self.sofrer_dano()
                for t in ini.tiros[:]:
                    if t.get_rect().colliderect(self.jogador.get_rect()):
                        ini.tiros.remove(t)
                        self.sofrer_dano()

        self.efeitos.atualizar()

    def desenhar_jogo(self):
        self.fundo.desenhar(self.canvas)
        self.jogador.desenhar(self.canvas)
        for m in self.misseis:
            m.desenhar(self.canvas)
        for pu in self.powerups:
            pu.desenhar(self.canvas)
        if self.boss_ativo:
            self.boss.desenhar(self.canvas)
        else:
            for ini in self.inimigos:
                ini.desenhar(self.canvas)
        for v in self.viloes_medios:
            v.desenhar(self.canvas)

        self.efeitos.desenhar(self.canvas)
        self.hud.desenhar(self.canvas, self.jogador)

        if config_atual["controles_touch"]:
            self.touch.desenhar(self.canvas)

        if self.pausado:
            txt = fonte_game_over.render("PAUSADO", True, BRANCO)
            self.canvas.blit(txt, txt.get_rect(center=(largura // 2, altura // 2)))

        ox, oy = self.efeitos.get_offset_shake()
        self.screen.fill(PRETO)
        self.screen.blit(self.canvas, (ox, oy))
        pygame.display.update()

    def desenhar_recordes(self):
        self.fundo.desenhar(self.screen)
        titulo = fonte_titulo.render("TOP 5 RECORDES", True, AMARELO)
        self.screen.blit(titulo, titulo.get_rect(center=(largura // 2, 110)))

        recordes = carregar_recordes()
        if not recordes:
            vazio = fonte_padrao.render("Nenhum recorde registrado ainda!", True, BRANCO)
            self.screen.blit(vazio, vazio.get_rect(center=(largura // 2, 320)))
        else:
            y = 210
            for idx, r in enumerate(recordes, 1):
                cor = AMARELO if idx == 1 else BRANCO
                linha = fonte_padrao.render(f"{idx}º  -  {r['pontos']} pts   ({r['dificuldade']})", True, cor)
                self.screen.blit(linha, linha.get_rect(center=(largura // 2, y)))
                y += 62

        self.btn_voltar_rec.desenhar(self.screen)
        pygame.display.update()

    def executar(self):
        tocar_musica("tela_inicial", config_atual["vol_musica"])
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.sair_jogo()

                if self.estado == "menu":
                    self.btn_jogar.checar_clique(event)
                    self.btn_recordes.checar_clique(event)
                    self.btn_config.checar_clique(event)
                    self.btn_sair.checar_clique(event)
                elif self.estado == "config":
                    for b in self.botoes_config:
                        b.checar_clique(event)
                elif self.estado == "recordes":
                    self.btn_voltar_rec.checar_clique(event)
                elif self.estado in ("game_over", "vitoria"):
                    self.btn_reiniciar.checar_clique(event)
                    self.btn_menu.checar_clique(event)
                elif self.estado == "jogando":
                    if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                        self.pausado = not self.pausado
                    if event.type == pygame.MOUSEBUTTONDOWN and config_atual["controles_touch"]:
                        if self.touch.btn_pause.collidepoint(event.pos):
                            self.pausado = not self.pausado

            self.fundo.atualizar()

            if self.estado == "menu":
                self.fundo.desenhar(self.screen)
                titulo = fonte_titulo.render("BATTLE SPACE", True, CIANO)
                self.screen.blit(titulo, titulo.get_rect(center=(largura // 2, 165)))
                self.btn_jogar.desenhar(self.screen)
                self.btn_recordes.desenhar(self.screen)
                self.btn_config.desenhar(self.screen)
                self.btn_sair.desenhar(self.screen)
                pygame.display.update()

            elif self.estado == "config":
                self.fundo.desenhar(self.screen)
                titulo = fonte_titulo.render("CONFIGURAÇÕES", True, AMARELO)
                self.screen.blit(titulo, titulo.get_rect(center=(largura // 2, 95)))
                for b in self.botoes_config:
                    b.desenhar(self.screen)
                pygame.display.update()

            elif self.estado == "recordes":
                self.desenhar_recordes()

            elif self.estado == "jogando":
                if not self.pausado:
                    self.atualizar_jogo()
                self.desenhar_jogo()

            elif self.estado in ("vitoria", "game_over"):
                self.fundo.desenhar(self.screen)
                msg = "VOCÊ VENCEU!" if self.estado == "vitoria" else "GAME OVER"
                cor = CIANO if self.estado == "vitoria" else VERMELHO
                txt = fonte_game_over.render(msg, True, cor)
                self.screen.blit(txt, txt.get_rect(center=(largura // 2, 220)))
                pts = fonte_padrao.render(f"Pontuação Final: {self.hud.pontos}", True, BRANCO)
                self.screen.blit(pts, pts.get_rect(center=(largura // 2, 315)))
                if self.novo_recorde:
                    rec = fonte_padrao.render("★ NOVO RECORDE! ★", True, AMARELO)
                    self.screen.blit(rec, rec.get_rect(center=(largura // 2, 370)))
                self.btn_reiniciar.desenhar(self.screen)
                self.btn_menu.desenhar(self.screen)
                pygame.display.update()

            self.clock.tick(FPS)
