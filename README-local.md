# Battle Space - Edição Turbinada (PC & Android APK)

## Novidades incluídas
- **Gráficos Neon HD & Animações:** Sprites procedurais, estrelas em parallax, partículas, ondas de choque, flash de dano e tremor de tela (*screen shake*).
- **Power-ups:**
  - `E` (**Escudo**): absorve 1 impacto.
  - `3X` (**Tiro Triplo**): dispara 3 projéteis simultâneos por 8 segundos.
  - `V` (**Turbo**): aumenta velocidade e cadência de tiro por 8 segundos.
  - `+` (**Vida Extra**): recupera 1 ponto de vida.
- **Ranking de Recordes (Top 5):** Salvo automaticamente em `highscores.json`.
- **Menu de Configurações:** Volume de música/SFX, Dificuldade (*Fácil*, *Normal*, *Difícil*), Partículas e Controles Touch.

## Como gerar o APK automaticamente pelo GitHub
1. Crie um repositório novo no [GitHub](https://github.com/new) (ex: `battle-space-apk`).
2. Extraia este ZIP e envie **todos os arquivos** (incluindo a pasta oculta `.github/workflows/build_apk.yml` e a sua pasta `sounds/` com os áudios originais) para o repositório.
3. No GitHub, clique na aba **Actions** -> clique em **Build Android APK (Battle Space)** -> aguarde a compilação terminar (leva ~10 a 15 minutos na primeira vez).
4. Ao finalizar, desça até **Artifacts** e clique em **Battle-Space-APK** para baixar o arquivo `.apk` pronto para instalar no Android!
