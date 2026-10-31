"""
CAPTURE E BATALHE - versão melhorada

Sprites próprios:
  Crie uma pasta "sprites" ao lado deste arquivo e coloque PNGs com o nome
  do Pokémon em minúsculas (ex.: sprites/pikachu.png, sprites/onix.png).
  Se o PNG existir, ele é usado automaticamente; se não, o jogo desenha uma
  criatura genérica por código, com visual baseado no tipo.
"""
import math
import os
import random

import pygame

pygame.init()

LARGURA, ALTURA = 1000, 720
HORIZONTE = 470
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Capture e Batalhe")
relogio = pygame.time.Clock()

try:
    PASTA_SPRITES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sprites")
except NameError:
    PASTA_SPRITES = "sprites"

FONTE_MINI = pygame.font.SysFont("arial", 13, bold=True)
FONTE_PEQUENA = pygame.font.SysFont("arial", 16, bold=True)
FONTE = pygame.font.SysFont("arial", 22)
FONTE_NEGRITO = pygame.font.SysFont("arial", 22, bold=True)
FONTE_SUB = pygame.font.SysFont("arial", 30, bold=True)
FONTE_TITULO = pygame.font.SysFont("arial", 54, bold=True)

BRANCO = (255, 255, 255)
PRETO = (25, 25, 30)
BORDA = (45, 45, 60)
AZUL = (70, 130, 210)
VERDE = (65, 170, 90)
VERMELHO = (210, 65, 65)
AMARELO = (240, 190, 50)
ROXO = (140, 90, 190)
OURO = (255, 205, 60)

TIPO_COR = {
    "Normal": (168, 168, 120), "Fogo": (240, 128, 48), "Água": (104, 144, 240),
    "Planta": (120, 200, 80), "Elétrico": (248, 208, 48), "Pedra": (184, 160, 56),
    "Voador": (168, 144, 240), "Terra": (224, 192, 104), "Gelo": (152, 216, 216),
    "Inseto": (168, 184, 32), "Lutador": (192, 48, 40), "Fantasma": (112, 88, 152),
}

# Nome, preço, força, chance de captura e cor
POKEBOLAS = [
    ("Master Ball", 500, 12, 1.00, (150, 70, 200)),
    ("Beast Ball", 350, 10, 0.85, (80, 90, 210)),
    ("Dream Ball", 300, 9, 0.80, (220, 130, 190)),
    ("Cherish Ball", 280, 9, 0.78, (230, 80, 100)),
    ("Safari Ball", 250, 8, 0.75, (150, 190, 90)),
    ("Sport Ball", 230, 8, 0.72, (220, 130, 50)),
    ("Heavy Ball", 210, 7, 0.70, (100, 100, 120)),
    ("Love Ball", 200, 7, 0.68, (240, 120, 160)),
    ("Moon Ball", 190, 7, 0.67, (80, 100, 170)),
    ("Fast Ball", 180, 6, 0.65, (240, 190, 60)),
    ("Level Ball", 170, 6, 0.64, (220, 110, 60)),
    ("Lure Ball", 160, 6, 0.62, (70, 150, 210)),
    ("Friend Ball", 150, 5, 0.60, (90, 180, 100)),
    ("Net Ball", 140, 5, 0.58, (60, 150, 170)),
    ("Dive Ball", 130, 5, 0.57, (70, 130, 220)),
    ("Dusk Ball", 120, 4, 0.55, (70, 70, 100)),
    ("Timer Ball", 110, 4, 0.53, (180, 100, 70)),
    ("Repeat Ball", 100, 4, 0.52, (220, 90, 90)),
    ("Luxury Ball", 90, 4, 0.50, (40, 40, 40)),
    ("Quick Ball", 80, 3, 0.48, (70, 170, 220)),
    ("Nest Ball", 70, 3, 0.46, (100, 180, 90)),
    ("Heal Ball", 60, 3, 0.44, (230, 130, 170)),
    ("Premier Ball", 50, 2, 0.42, (230, 230, 230)),
    ("Great Ball", 40, 2, 0.40, (60, 110, 220)),
    ("Pokébola", 30, 2, 0.35, (220, 70, 70)),
    ("Strange Ball", 20, 1, 0.30, (170, 100, 190)),
    ("Bola Básica", 10, 1, 0.25, (200, 200, 200)),
]
NOMES_BOLAS = [b[0] for b in POKEBOLAS]
BOLAS = {b[0]: b for b in POKEBOLAS}

# ---------------------------------------------------------------- Pokémon
ATAQUES_TIPO = {
    "Fogo": [("Brasas", 18), ("Roda de Fogo", 24)],
    "Água": [("Jato d'Água", 20), ("Bolhas", 18)],
    "Planta": [("Chicote de Vinha", 20), ("Folha Navalha", 24)],
    "Elétrico": [("Choque do Trovão", 22), ("Faísca", 20)],
    "Pedra": [("Arremesso de Pedra", 20), ("Rolar", 18)],
    "Voador": [("Rajada", 18), ("Ataque de Asa", 22)],
    "Terra": [("Tapa de Lama", 18), ("Terremoto", 24)],
    "Gelo": [("Raio de Gelo", 22), ("Vento Gelado", 18)],
    "Inseto": [("Picada", 18), ("Zumbido", 22)],
    "Lutador": [("Soco Karatê", 20), ("Golpe Baixo", 24)],
    "Fantasma": [("Lambida", 16), ("Bola Sombria", 24)],
}


def ataques_padrao(tipo):
    if tipo == "Normal":
        return [("Arranhão", "Normal", 14), ("Investida", "Normal", 12),
                ("Ataque Rápido", "Normal", 16), ("Cabeçada", "Normal", 18)]
    a, b = ATAQUES_TIPO[tipo]
    return [(a[0], tipo, a[1]), ("Investida", "Normal", 12),
            (b[0], tipo, b[1]), ("Cabeçada", "Normal", 16)]


def mk(tipo, cor, facil=1.0):
    return {"tipo": tipo, "cor": cor, "ataques": ataques_padrao(tipo), "facil": facil}


POKEMON = {
    "Charmander": {
        "tipo": "Fogo", "cor": (240, 120, 60), "facil": 0.9,
        "ataques": [("Brasas", "Fogo", 18), ("Arranhão", "Normal", 12),
                    ("Roda de Fogo", "Fogo", 24), ("Investida", "Normal", 15)],
    },
    "Bulbasaur": {
        "tipo": "Planta", "cor": (80, 170, 90), "facil": 0.9,
        "ataques": [("Chicote de Vinha", "Planta", 20), ("Investida", "Normal", 12),
                    ("Folha Navalha", "Planta", 24), ("Pó de Sono", "Planta", 16)],
    },
    "Squirtle": {
        "tipo": "Água", "cor": (80, 160, 230), "facil": 0.9,
        "ataques": [("Jato d'Água", "Água", 20), ("Investida", "Normal", 12),
                    ("Bolhas", "Água", 18), ("Cabeçada", "Normal", 16)],
    },
    "Pikachu": {
        "tipo": "Elétrico", "cor": (245, 210, 60), "facil": 0.75,
        "ataques": [("Choque do Trovão", "Elétrico", 22), ("Investida", "Normal", 12),
                    ("Ataque Rápido", "Normal", 16), ("Faísca", "Elétrico", 20)],
    },
    "Geodude": {
        "tipo": "Pedra", "cor": (140, 130, 120), "facil": 1.0,
        "ataques": [("Arremesso de Pedra", "Pedra", 20), ("Investida", "Normal", 12),
                    ("Rolar", "Pedra", 18), ("Cabeçada", "Normal", 16)],
    },
    "Pidgey": {
        "tipo": "Voador", "cor": (180, 140, 90), "facil": 1.0,
        "ataques": [("Rajada", "Voador", 18), ("Investida", "Normal", 12),
                    ("Ataque de Asa", "Voador", 22), ("Bicada", "Voador", 16)],
    },
    "Rattata": mk("Normal", (150, 110, 170), 1.1),
    "Meowth": mk("Normal", (235, 215, 170), 1.0),
    "Caterpie": mk("Inseto", (130, 200, 90), 1.1),
    "Oddish": mk("Planta", (90, 120, 190), 1.0),
    "Sandshrew": mk("Terra", (225, 195, 110), 1.0),
    "Diglett": mk("Terra", (160, 110, 70), 1.0),
    "Vulpix": mk("Fogo", (200, 90, 60), 0.85),
    "Growlithe": mk("Fogo", (235, 150, 60), 0.85),
    "Onix": mk("Pedra", (150, 150, 160), 0.7),
    "Machop": mk("Lutador", (150, 165, 200), 0.9),
    "Zubat": mk("Voador", (110, 120, 210), 1.0),
    "Psyduck": mk("Água", (240, 210, 90), 0.9),
    "Magikarp": mk("Água", (225, 100, 80), 1.2),
    "Gastly": mk("Fantasma", (90, 70, 140), 0.8),
    "Swinub": mk("Gelo", (170, 140, 110), 0.95),
    "Snorunt": mk("Gelo", (190, 205, 225), 0.9),
}
NOMES_POKEMON = list(POKEMON.keys())

VANTAGENS = {
    "Fogo": ["Planta", "Gelo", "Inseto"],
    "Água": ["Fogo", "Pedra", "Terra"],
    "Planta": ["Água", "Pedra", "Terra"],
    "Elétrico": ["Água", "Voador"],
    "Pedra": ["Fogo", "Voador", "Gelo", "Inseto"],
    "Voador": ["Planta", "Inseto", "Lutador"],
    "Terra": ["Fogo", "Elétrico", "Pedra"],
    "Gelo": ["Planta", "Terra", "Voador"],
    "Inseto": ["Planta"],
    "Lutador": ["Normal", "Pedra", "Gelo"],
    "Fantasma": ["Fantasma"],
}
RESISTENCIAS = {
    "Fogo": ["Fogo", "Água", "Pedra"],
    "Água": ["Água", "Planta"],
    "Planta": ["Planta", "Fogo", "Voador"],
    "Elétrico": ["Elétrico", "Planta", "Terra"],
    "Pedra": ["Lutador", "Terra"],
    "Voador": ["Elétrico", "Pedra"],
    "Terra": ["Voador", "Planta"],
    "Gelo": ["Fogo", "Água", "Gelo"],
    "Inseto": ["Fogo", "Voador", "Lutador"],
    "Lutador": ["Voador", "Fantasma"],
    "Fantasma": ["Normal", "Lutador"],
}

LIDERES = [
    {"nome": "Líder Rocha", "pokemon": "Onix", "hp": 100, "recompensa": 50},
    {"nome": "Líder Água", "pokemon": "Squirtle", "hp": 105, "recompensa": 60},
    {"nome": "Líder Planta", "pokemon": "Bulbasaur", "hp": 110, "recompensa": 70},
    {"nome": "Líder Elétrico", "pokemon": "Pikachu", "hp": 115, "recompensa": 80},
    {"nome": "Líder Fogo", "pokemon": "Growlithe", "hp": 120, "recompensa": 90},
    {"nome": "Líder Gelo", "pokemon": "Swinub", "hp": 125, "recompensa": 100},
    {"nome": "Líder Sombra", "pokemon": "Gastly", "hp": 130, "recompensa": 120},
    {"nome": "Líder Luta", "pokemon": "Machop", "hp": 140, "recompensa": 150},
]
for _l in LIDERES:
    _l["tipo"] = POKEMON[_l["pokemon"]]["tipo"]

MAPAS = [
    {"nome": "Campo Verde", "decor": "campo", "ceu": ((120, 195, 245), (205, 235, 250)),
     "chao": (110, 190, 100), "chao2": (100, 178, 92),
     "pool": ["Rattata", "Pidgey", "Caterpie", "Oddish", "Meowth", "Pikachu"]},
    {"nome": "Deserto", "decor": "deserto", "ceu": ((250, 190, 110), (255, 235, 180)),
     "chao": (232, 200, 130), "chao2": (222, 188, 118),
     "pool": ["Sandshrew", "Diglett", "Geodude", "Vulpix", "Growlithe", "Meowth"]},
    {"nome": "Floresta", "decor": "floresta", "ceu": ((90, 150, 120), (170, 215, 170)),
     "chao": (70, 140, 80), "chao2": (62, 128, 72),
     "pool": ["Bulbasaur", "Caterpie", "Oddish", "Pikachu", "Pidgey", "Zubat"]},
    {"nome": "Montanhas", "decor": "montanha", "ceu": ((130, 170, 215), (215, 230, 245)),
     "chao": (150, 160, 150), "chao2": (140, 150, 140),
     "pool": ["Geodude", "Onix", "Machop", "Zubat", "Pidgey", "Rattata"]},
    {"nome": "Praia", "decor": "praia", "ceu": ((100, 200, 250), (230, 245, 250)),
     "chao": (240, 225, 165), "chao2": (232, 214, 152),
     "pool": ["Squirtle", "Psyduck", "Magikarp", "Pidgey", "Diglett", "Rattata"]},
    {"nome": "Caverna", "decor": "caverna", "ceu": ((25, 20, 45), (60, 50, 90)),
     "chao": (90, 80, 105), "chao2": (82, 72, 96),
     "pool": ["Zubat", "Geodude", "Gastly", "Onix", "Machop", "Diglett"]},
    {"nome": "Montanha Gelada", "decor": "neve", "ceu": ((170, 205, 235), (235, 245, 255)),
     "chao": (232, 242, 250), "chao2": (220, 232, 245),
     "pool": ["Swinub", "Snorunt", "Pikachu", "Machop", "Zubat", "Meowth"]},
    {"nome": "Vulcão", "decor": "vulcao", "ceu": ((90, 25, 25), (230, 120, 60)),
     "chao": (95, 70, 65), "chao2": (86, 62, 58),
     "pool": ["Charmander", "Growlithe", "Vulpix", "Geodude", "Onix", "Gastly"]},
]

# ---------------------------------------------------------------- estado
moedas = 150
inventario_bolas = {"Pokébola": 5}
pokemon_capturados = []
ativo = None
lideres_vencidos = set()

mapa_atual = 0
construcoes = []
pokemon_no_mapa = None
pokemon_rect = pygame.Rect(750, 390, 70, 70)
bola_voando = None
bola_selecionada = "Pokébola"

mensagem = "Bem-vindo! Escolha uma opção no lobby."
tela_atual = "lobby"
tempo = 0

lider_idx = 0
lider_batalha = None
jogador_batalha = None
hp_jogador = hp_jogador_max = 100
hp_lider = hp_lider_max = 100
hp_exib_jogador = hp_exib_lider = 100.0
fase = "escolha"
timer_fase = 0
msg_batalha = ["", ""]
tremer_j = tremer_l = 0
resultado = ""
resultado_sub = ""
venceu = False

particulas = []
_cache_fundos = {}
_cache_sprites = {}
_cache_mapas = {}

# ---------------------------------------------------------------- utilidades


def R(x, y, w, h):
    return pygame.Rect(int(x), int(y), int(w), int(h))


def clamp(v, a, b):
    return max(a, min(b, v))


def misturar(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def clarear(c, t=0.3):
    return misturar(c, (255, 255, 255), t)


def escurecer(c, t=0.3):
    return misturar(c, (0, 0, 0), t)


def gradiente(w, h, topo, base):
    surf = pygame.Surface((w, h))
    for y in range(h):
        pygame.draw.line(surf, misturar(topo, base, y / max(1, h - 1)), (0, y), (w, y))
    return surf


def fundo_gradiente(chave, topo, base):
    if chave not in _cache_fundos:
        _cache_fundos[chave] = gradiente(LARGURA, ALTURA, topo, base)
    return _cache_fundos[chave]


def texto(msg, x, y, cor=PRETO, fonte=FONTE, centro=False, sombra=False):
    img = fonte.render(str(msg), True, cor)
    rect = img.get_rect()
    if centro:
        rect.midtop = (x, y)
    else:
        rect.topleft = (x, y)
    if sombra:
        s = fonte.render(str(msg), True, (0, 0, 0))
        s.set_alpha(90)
        tela.blit(s, rect.move(2, 3))
    tela.blit(img, rect)


def sombra_chao(x, y, w, h, alpha=70):
    s = pygame.Surface((int(w), int(h)), pygame.SRCALPHA)
    pygame.draw.ellipse(s, (0, 0, 0, alpha), s.get_rect())
    tela.blit(s, (int(x - w / 2), int(y - h / 2)))


def painel(rect, cor=BRANCO, alpha=225, borda=BORDA):
    s = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(s, (*cor, alpha), s.get_rect(), border_radius=14)
    tela.blit(s, rect.topleft)
    pygame.draw.rect(tela, borda, rect, 2, border_radius=14)


def botao(rect, rotulo, cor=AZUL, ativo_=True, fonte=FONTE_PEQUENA):
    sobre = ativo_ and rect.collidepoint(pygame.mouse.get_pos())
    base = cor if ativo_ else (150, 150, 155)
    if sobre:
        base = clarear(base, 0.18)
    pygame.draw.rect(tela, escurecer(base, 0.45), rect.move(0, 4), border_radius=10)
    pygame.draw.rect(tela, base, rect, border_radius=10)
    pygame.draw.rect(tela, clarear(base, 0.25),
                     R(rect.x + 5, rect.y + 4, rect.w - 10, rect.h // 3), border_radius=8)
    pygame.draw.rect(tela, BORDA, rect, 2, border_radius=10)
    img = fonte.render(rotulo, True, BRANCO)
    tela.blit(img, img.get_rect(center=rect.center))


def chip_tipo(x, y, tipo):
    img = FONTE_MINI.render(tipo.upper(), True, BRANCO)
    r = pygame.Rect(int(x), int(y), img.get_width() + 14, 18)
    pygame.draw.rect(tela, TIPO_COR[tipo], r, border_radius=9)
    pygame.draw.rect(tela, escurecer(TIPO_COR[tipo], 0.4), r, 1, border_radius=9)
    tela.blit(img, img.get_rect(center=r.center))
    return r.width


def desenhar_bola(surf, centro, raio, cor):
    pygame.draw.circle(surf, escurecer(cor, 0.35), (centro[0], centro[1] + 2), raio)
    pygame.draw.circle(surf, cor, centro, raio)
    pygame.draw.circle(surf, clarear(cor, 0.55),
                       (centro[0] - raio // 3, centro[1] - raio // 3), max(2, raio // 4))
    pygame.draw.circle(surf, PRETO, centro, raio, 2)


def barra_hp(x, y, w, atual, maximo):
    pct = clamp(atual / maximo, 0, 1)
    cor = VERDE if pct > 0.5 else (AMARELO if pct > 0.25 else VERMELHO)
    pygame.draw.rect(tela, (60, 60, 75), R(x, y, w, 14), border_radius=7)
    if pct > 0:
        pygame.draw.rect(tela, cor, R(x + 2, y + 2, max(6, (w - 4) * pct), 10), border_radius=5)


def multiplicador(tipo_ataque, tipo_defesa):
    if tipo_defesa in VANTAGENS.get(tipo_ataque, []):
        return 1.5
    if tipo_defesa in RESISTENCIAS.get(tipo_ataque, []):
        return 0.75
    return 1.0


# ---------------------------------------------------------------- partículas


def criar_particulas(x, y, cor, n=16):
    for _ in range(n):
        ang = random.uniform(0, 2 * math.pi)
        vel = random.uniform(1.5, 6)
        particulas.append({"x": x, "y": y, "vx": math.cos(ang) * vel,
                           "vy": math.sin(ang) * vel - 1.5, "vida": random.randint(22, 42),
                           "cor": cor, "r": random.uniform(2, 5)})


def atualizar_particulas():
    for p in particulas[:]:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["vy"] += 0.18
        p["vida"] -= 1
        if p["vida"] <= 0:
            particulas.remove(p)


def desenhar_particulas():
    for p in particulas:
        pygame.draw.circle(tela, p["cor"], (int(p["x"]), int(p["y"])), max(1, int(p["r"] * p["vida"] / 30)))


# ---------------------------------------------------------------- sprites


def criar_criatura(nome, t):
    """Criatura genérica desenhada por código, baseada no tipo."""
    dados = POKEMON[nome]
    cor, tipo = dados["cor"], dados["tipo"]
    rng = random.Random(nome)
    T = t * 2
    s = pygame.Surface((T, T), pygame.SRCALPHA)
    contorno = escurecer(cor, 0.6)
    claro = clarear(cor, 0.5)
    escuro = escurecer(cor, 0.2)
    esp = max(3, T // 60)

    larg = int(T * rng.uniform(0.56, 0.72))
    alt = int(T * rng.uniform(0.5, 0.62))
    corpo = pygame.Rect(0, 0, larg, alt)
    corpo.midbottom = (T // 2, int(T * 0.9))
    cx, topo, cy = corpo.centerx, corpo.top, corpo.centery

    def P(dx, dy, bx=None, by=None):
        bx = cx if bx is None else bx
        by = topo if by is None else by
        return (int(bx + T * dx), int(by + T * dy))

    def forma(pontos, cor_f, cor_b=contorno):
        pygame.draw.polygon(s, cor_f, pontos)
        pygame.draw.polygon(s, cor_b, pontos, esp)

    def elipse(rect, cor_f, cor_b=contorno):
        pygame.draw.ellipse(s, cor_f, rect)
        pygame.draw.ellipse(s, cor_b, rect, esp)

    # ---- atrás do corpo
    if tipo == "Voador":
        for lado in (-1, 1):
            w = pygame.Rect(0, 0, int(T * 0.24), int(T * 0.38))
            w.center = (cx + lado * (larg // 2 + int(T * 0.03)), cy - int(T * 0.05))
            elipse(w, escuro)
    if tipo == "Fantasma":
        for k in range(-2, 3):
            pos = (cx + int(k * larg * 0.2), corpo.bottom - int(T * 0.02))
            r = int(T * 0.07)
            pygame.draw.circle(s, cor, pos, r)
            pygame.draw.circle(s, contorno, pos, r, esp)
    else:
        for lado in (-1, 1):
            f = pygame.Rect(0, 0, int(T * 0.18), int(T * 0.11))
            f.center = (cx + lado * int(larg * 0.25), corpo.bottom - int(T * 0.01))
            elipse(f, escuro)
    if tipo == "Normal":
        for lado in (-1, 1):
            pos = (cx + int(lado * larg * 0.32), topo + int(T * 0.02))
            pygame.draw.circle(s, cor, pos, int(T * 0.08))
            pygame.draw.circle(s, contorno, pos, int(T * 0.08), esp)
    if tipo in ("Pedra", "Terra"):
        cor_esp = escurecer(cor, 0.35) if tipo == "Pedra" else (150, 110, 70)
        for k in range(-2, 3):
            x = cx + int(k * larg * 0.17)
            forma([(x - int(T * 0.05), topo + int(T * 0.04)),
                   (x, topo - int(T * 0.1) + int(abs(k) * T * 0.015)),
                   (x + int(T * 0.05), topo + int(T * 0.04))], cor_esp)

    # ---- corpo
    elipse(corpo, cor)
    barriga = pygame.Rect(0, 0, int(larg * 0.55), int(alt * 0.5))
    barriga.center = (cx, cy + int(alt * 0.2))
    pygame.draw.ellipse(s, claro, barriga)

    # ---- adornos da cabeça
    if tipo == "Fogo":
        forma([P(-.08, .03), P(-.07, -.1), P(-.02, -.07), P(0, -.22), P(.05, -.09),
               P(.09, -.12), P(.08, .03)], (250, 140, 40))
        forma([P(-.04, .02), P(-.03, -.05), P(0, -.1), P(.04, -.04), P(.04, .02)],
              (255, 220, 90), (255, 220, 90))
    elif tipo == "Água":
        pygame.draw.circle(s, (130, 200, 255), P(0, -.03), int(T * .06))
        pygame.draw.circle(s, contorno, P(0, -.03), int(T * .06), esp)
        forma([P(-.055, -.05), P(0, -.19), P(.055, -.05)], (130, 200, 255))
    elif tipo == "Planta":
        forma([P(0, .03), P(-.07, -.08), P(-.19, -.15), P(-.15, -.01), P(-.06, .03)], (90, 200, 100))
        forma([P(0, .03), P(.07, -.08), P(.19, -.15), P(.15, -.01), P(.06, .03)], (90, 200, 100))
    elif tipo == "Elétrico":
        forma([P(-.07, .03), P(-.05, -.1), P(-.01, -.03), P(.02, -.15), P(.04, -.04),
               P(.08, -.09), P(.07, .03)], (255, 230, 80))
        for lado in (-1, 1):
            sx, sy = cx + int(lado * larg * 0.55), cy - int(T * 0.1)
            forma([(sx, sy - int(T * .05)), (sx + int(T * .03), sy),
                   (sx, sy + int(T * .05)), (sx - int(T * .03), sy)], (255, 240, 120))
    elif tipo == "Gelo":
        forma([P(-.1, .03), P(-.06, -.12), P(-.02, .03)], (190, 235, 255))
        forma([P(0, .03), P(.05, -.17), P(.1, .03)], (220, 245, 255))
    elif tipo == "Inseto":
        for lado in (-1, 1):
            a = P(lado * .06, .02)
            b = P(lado * .14, -.16)
            pygame.draw.line(s, contorno, a, b, esp)
            pygame.draw.circle(s, claro, b, int(T * .03))
            pygame.draw.circle(s, contorno, b, int(T * .03), esp)
    elif tipo == "Lutador":
        y = topo + int(alt * 0.22)
        pygame.draw.rect(s, (200, 50, 50), R(cx - larg * 0.33, y, larg * 0.66, T * .05))
        pygame.draw.rect(s, contorno, R(cx - larg * 0.33, y, larg * 0.66, T * .05), esp)

    # ---- rosto
    olho_y = topo + int(alt * 0.4)
    r_olho = int(T * rng.uniform(0.045, 0.065))
    if tipo == "Fantasma":
        r_olho = int(r_olho * 1.3)
    for lado in (-1, 1):
        pos = (cx + lado * int(larg * 0.2), olho_y)
        pygame.draw.circle(s, BRANCO, pos, r_olho)
        pygame.draw.circle(s, contorno, pos, r_olho, max(2, esp - 1))
        pygame.draw.circle(s, PRETO, (pos[0] + 2, pos[1] + 1), int(r_olho * 0.6))
        pygame.draw.circle(s, BRANCO, (pos[0] + 4, pos[1] - 2), max(2, int(r_olho * 0.22)))
    if tipo == "Voador":
        forma([(cx - int(T * .04), olho_y + int(T * .04)), (cx + int(T * .04), olho_y + int(T * .04)),
               (cx, olho_y + int(T * .1))], (250, 170, 60))
    elif tipo == "Fantasma":
        rect_boca = pygame.Rect(cx - int(T * .08), olho_y + int(T * .03), int(T * .16), int(T * .1))
        pygame.draw.ellipse(s, (60, 20, 70), rect_boca)
        pygame.draw.ellipse(s, contorno, rect_boca, esp)
    else:
        rect_boca = pygame.Rect(cx - int(T * .05), olho_y + int(T * .02), int(T * .1), int(T * .07))
        pygame.draw.arc(s, contorno, rect_boca, 3.4, 6.0, esp)

    return pygame.transform.smoothscale(s, (t, t))


def sprite_pokemon(nome, tamanho):
    chave = (nome, tamanho)
    if chave in _cache_sprites:
        return _cache_sprites[chave]
    img = None
    caminho = os.path.join(PASTA_SPRITES, nome.lower() + ".png")
    if os.path.exists(caminho):
        try:
            img = pygame.image.load(caminho).convert_alpha()
            w, h = img.get_size()
            esc = tamanho / max(w, h)
            img = pygame.transform.smoothscale(img, (max(1, int(w * esc)), max(1, int(h * esc))))
        except pygame.error:
            img = None
    if img is None:
        img = criar_criatura(nome, tamanho)
    _cache_sprites[chave] = img
    return img


def silhueta(nome, tamanho):
    chave = ("sil", nome, tamanho)
    if chave not in _cache_sprites:
        img = sprite_pokemon(nome, tamanho).copy()
        img.fill((35, 35, 50, 255), special_flags=pygame.BLEND_RGBA_MULT)
        img.fill((35, 35, 50, 0), special_flags=pygame.BLEND_RGBA_ADD)
        _cache_sprites[chave] = img
    return _cache_sprites[chave]


def desenhar_treinador(x, y, mira=None):
    """(x, y) = pés do treinador."""
    sombra_chao(x, y + 2, 60, 16)
    pygame.draw.rect(tela, (55, 60, 95), R(x - 13, y - 30, 11, 30), border_radius=4)
    pygame.draw.rect(tela, (55, 60, 95), R(x + 2, y - 30, 11, 30), border_radius=4)
    pygame.draw.rect(tela, (35, 35, 50), R(x - 15, y - 6, 14, 7), border_radius=3)
    pygame.draw.rect(tela, (35, 35, 50), R(x + 1, y - 6, 14, 7), border_radius=3)
    pygame.draw.rect(tela, (60, 120, 190), R(x - 18, y - 66, 36, 40), border_radius=10)
    pygame.draw.rect(tela, BORDA, R(x - 18, y - 66, 36, 40), 2, border_radius=10)
    pygame.draw.line(tela, (245, 205, 170), (x + 10, y - 60), (x + 32, y - 58), 8)
    pygame.draw.circle(tela, (245, 205, 170), (x + 34, y - 58), 6)
    pygame.draw.circle(tela, (245, 205, 170), (x, y - 82), 17)
    pygame.draw.circle(tela, BORDA, (x, y - 82), 17, 2)
    pygame.draw.circle(tela, PRETO, (x + 6, y - 83), 2)
    pygame.draw.circle(tela, PRETO, (x - 5, y - 83), 2)
    pygame.draw.arc(tela, (230, 90, 60), R(x - 18, y - 102, 36, 32), 0, math.pi, 17)
    pygame.draw.rect(tela, (230, 90, 60), R(x - 2, y - 92, 28, 7), border_radius=3)


# ---------------------------------------------------------------- mapas


def desenhar_nuvem(s, x, y, e=1.0, cor=(255, 255, 255)):
    for dx, dy, r in ((0, 0, 26), (28, -8, 32), (60, 0, 26), (30, 10, 26)):
        pygame.draw.circle(s, cor, (int(x + dx * e), int(y + dy * e)), int(r * e))


def desenhar_arvore(s, x, y, e, folha, tronco=(110, 75, 45)):
    pygame.draw.rect(s, tronco, R(x - 7 * e, y - 45 * e, 14 * e, 45 * e))
    copas = ((0, -70, 30), (-22, -52, 24), (22, -52, 24))
    for dx, dy, r in copas:
        pygame.draw.circle(s, escurecer(folha, 0.25), (int(x + dx * e), int(y + dy * e + 4 * e)), int(r * e))
    for dx, dy, r in copas:
        pygame.draw.circle(s, folha, (int(x + dx * e - 2 * e), int(y + dy * e)), int(r * e) - 2)


def desenhar_pinheiro(s, x, y, e, cor, neve=False):
    pygame.draw.rect(s, (100, 70, 45), R(x - 5 * e, y - 20 * e, 10 * e, 20 * e))
    for k in range(3):
        base = y - 15 * e - k * 30 * e
        larg = (44 - k * 10) * e
        pygame.draw.polygon(s, cor, [(x - larg, base), (x + larg, base), (x, base - 50 * e)])
        if neve:
            pygame.draw.polygon(s, (245, 250, 255), [(x - larg * 0.45, base - 27 * e),
                                                    (x + larg * 0.45, base - 27 * e), (x, base - 50 * e)])


def desenhar_cacto(s, x, y, e):
    cor = (70, 150, 80)
    borda = escurecer(cor, 0.35)
    partes = [R(x - 9 * e, y - 70 * e, 18 * e, 70 * e),
              R(x - 28 * e, y - 48 * e, 22 * e, 9 * e), R(x - 28 * e, y - 62 * e, 9 * e, 23 * e),
              R(x + 6 * e, y - 40 * e, 22 * e, 9 * e), R(x + 19 * e, y - 54 * e, 9 * e, 23 * e)]
    for p in partes:
        pygame.draw.rect(s, cor, p, border_radius=max(2, int(4 * e)))
        pygame.draw.rect(s, borda, p, 2, border_radius=max(2, int(4 * e)))


def desenhar_palmeira(s, x, y, e):
    topo = (x, y)
    for k in range(10):
        px = x + math.sin(k / 10 * 1.2) * 18 * e
        py = y - k * 9 * e
        pygame.draw.circle(s, (130, 90, 55), (int(px), int(py)), max(3, int(6 * e)))
        topo = (px, py)
    for ang in (200, 235, 270, 305, 340):
        a = math.radians(ang)
        fim = (topo[0] + math.cos(a) * 55 * e, topo[1] + math.sin(a) * 30 * e + 18 * e)
        pygame.draw.line(s, (50, 140, 70), topo, fim, max(3, int(7 * e)))
        pygame.draw.line(s, (90, 190, 100), topo, fim, max(1, int(3 * e)))


def desenhar_pico(s, x, base, w, h, cor, neve=True):
    pygame.draw.polygon(s, cor, [(x - w / 2, base), (x, base - h), (x + w / 2, base)])
    pygame.draw.polygon(s, escurecer(cor, 0.15), [(x, base - h), (x + w / 2, base), (x + w * 0.1, base)])
    if neve:
        pygame.draw.polygon(s, (245, 248, 255), [(x - w * 0.14, base - h * 0.72), (x, base - h),
                                                (x + w * 0.14, base - h * 0.72), (x + w * 0.05, base - h * 0.66),
                                                (x - w * 0.03, base - h * 0.7)])


def brilho(s, x, y, r, cor):
    g = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
    for k in range(r, 0, -3):
        pygame.draw.circle(g, (*cor, int(90 * (1 - k / r)) + 10), (r, r), k)
    s.blit(g, (int(x - r), int(y - r)))


def construir_mapa(i):
    m = MAPAS[i]
    s = pygame.Surface((LARGURA, ALTURA))
    h = HORIZONTE
    s.blit(gradiente(LARGURA, h, *m["ceu"]), (0, 0))
    rng = random.Random(100 + i)
    d = m["decor"]

    # ---- fundo distante
    if d == "campo":
        for x in (80, 300, 520, 760, 950):
            pygame.draw.ellipse(s, (130, 190, 110), R(x - 230, h - 110, 460, 220))
        for _ in range(4):
            desenhar_nuvem(s, rng.randint(50, 900), rng.randint(40, 200), rng.uniform(0.8, 1.3))
    elif d == "deserto":
        pygame.draw.circle(s, (255, 240, 170), (800, 110), 55)
        for x, w in ((120, 520), (560, 600), (950, 480)):
            pygame.draw.ellipse(s, (232, 190, 120), R(x - w / 2, h - 70, w, 150))
    elif d == "floresta":
        for x in range(-20, LARGURA + 40, 60):
            desenhar_arvore(s, x, h - 5, rng.uniform(1.0, 1.5), (40, 100, 70))
        for _ in range(3):
            desenhar_nuvem(s, rng.randint(50, 900), rng.randint(30, 120), 0.9, (190, 225, 200))
    elif d == "montanha":
        for x, w, hh in ((120, 380, 260), (420, 460, 330), (760, 420, 280), (980, 360, 220)):
            desenhar_pico(s, x, h, w, hh, (120, 130, 150))
        for _ in range(3):
            desenhar_nuvem(s, rng.randint(50, 900), rng.randint(30, 140), 1.0)
    elif d == "praia":
        pygame.draw.circle(s, (255, 245, 190), (820, 100), 50)
        s.blit(gradiente(LARGURA, 150, (90, 190, 230), (40, 130, 200)), (0, 320))
        for k in range(26):
            wx, wy = rng.randint(0, LARGURA), rng.randint(335, 455)
            pygame.draw.arc(s, (210, 240, 255), R(wx, wy, 40, 12), 0.3, 2.8, 2)
        for _ in range(3):
            desenhar_nuvem(s, rng.randint(50, 900), rng.randint(30, 150), 1.0)
    elif d == "caverna":
        for _ in range(26):
            x = rng.randint(0, LARGURA)
            hh = rng.randint(30, 150)
            ww = rng.randint(18, 40)
            pygame.draw.polygon(s, (50, 42, 72), [(x - ww, 0), (x + ww, 0), (x, hh)])
            pygame.draw.polygon(s, (72, 62, 100), [(x, 0), (x + ww, 0), (x, hh)])
        for _ in range(7):
            x, y = rng.randint(40, 960), rng.randint(200, 420)
            brilho(s, x, y, 40, (120, 220, 255))
            pygame.draw.polygon(s, (150, 230, 255), [(x - 7, y + 14), (x, y - 20), (x + 7, y + 14)])
    elif d == "neve":
        for x, w, hh in ((140, 420, 240), (480, 480, 300), (850, 440, 250)):
            desenhar_pico(s, x, h, w, hh, (150, 170, 200))
        for _ in range(3):
            desenhar_nuvem(s, rng.randint(50, 900), rng.randint(30, 130), 1.0, (250, 252, 255))
    elif d == "vulcao":
        pygame.draw.polygon(s, (55, 35, 40), [(260, h), (480, 140), (520, 140), (740, h)])
        pygame.draw.polygon(s, (255, 120, 40), [(480, 140), (520, 140), (505, 175), (495, 175)])
        brilho(s, 500, 150, 70, (255, 150, 60))
        for k in range(5):
            pygame.draw.circle(s, (80, 60, 65), (500 + k * 12, 100 - k * 22), 22 + k * 7)
        for x, w, hh in ((60, 300, 150), (950, 340, 170)):
            desenhar_pico(s, x, h, w, hh, (70, 45, 50), False)

    # ---- chão
    s.fill(m["chao"], R(0, h, LARGURA, ALTURA - h))
    for k in range(0, 5, 2):
        s.fill(m["chao2"], R(0, h + k * 50, LARGURA, 50))
    pygame.draw.line(s, escurecer(m["chao"], 0.3), (0, h), (LARGURA, h), 3)

    # ---- props
    if d == "campo":
        for x in range(30, LARGURA, 90):
            desenhar_arvore(s, x + rng.randint(-15, 15), h - 2, rng.uniform(0.45, 0.6), (70, 160, 80))
        for _ in range(60):
            fx, fy = rng.randint(0, LARGURA), rng.randint(h + 20, ALTURA - 10)
            pygame.draw.circle(s, rng.choice([(255, 240, 120), (255, 255, 255), (250, 150, 180)]), (fx, fy), 3)
        desenhar_arvore(s, 40, h + 70, 1.4, (60, 150, 75))
        desenhar_arvore(s, 960, h + 70, 1.4, (60, 150, 75))
    elif d == "deserto":
        for x in range(40, LARGURA, 110):
            desenhar_cacto(s, x + rng.randint(-20, 20), h - 2, rng.uniform(0.4, 0.55))
        desenhar_cacto(s, 45, h + 90, 1.3)
        desenhar_cacto(s, 955, h + 80, 1.1)
        for _ in range(10):
            rx, ry = rng.randint(0, LARGURA), rng.randint(h + 80, ALTURA - 20)
            pygame.draw.ellipse(s, (170, 140, 100), R(rx, ry, 26, 12))
    elif d == "floresta":
        for x in range(10, LARGURA, 75):
            desenhar_arvore(s, x + rng.randint(-10, 10), h + 4, rng.uniform(0.7, 0.9), (50, 130, 70))
        desenhar_arvore(s, 40, h + 110, 1.6, (40, 120, 65))
        desenhar_arvore(s, 965, h + 110, 1.6, (40, 120, 65))
        for _ in range(8):
            mx, my = rng.randint(0, LARGURA), rng.randint(h + 90, ALTURA - 20)
            pygame.draw.rect(s, (240, 235, 225), R(mx - 3, my, 6, 10))
            pygame.draw.ellipse(s, (220, 70, 70), R(mx - 10, my - 8, 20, 12))
    elif d == "montanha":
        for _ in range(14):
            rx, ry = rng.randint(0, LARGURA), rng.randint(h + 10, ALTURA - 20)
            pygame.draw.ellipse(s, (120, 125, 120), R(rx, ry, rng.randint(24, 50), rng.randint(14, 24)))
        desenhar_pico(s, 40, h + 150, 150, 160, (110, 120, 135))
        desenhar_pico(s, 960, h + 150, 170, 170, (110, 120, 135))
    elif d == "praia":
        for x in (30, 150, 880, 970):
            desenhar_palmeira(s, x, h + 10 + (0 if x in (150, 880) else 80), 0.8 if x in (150, 880) else 1.2)
        for _ in range(16):
            cx, cy = rng.randint(0, LARGURA), rng.randint(h + 40, ALTURA - 20)
            pygame.draw.ellipse(s, (250, 190, 190), R(cx, cy, 14, 9))
    elif d == "caverna":
        for x in range(10, LARGURA, 55):
            hh = rng.randint(20, 55)
            pygame.draw.polygon(s, (60, 50, 82), [(x - 14, h + 4), (x + 14, h + 4), (x, h + 4 - hh)])
        for _ in range(5):
            x, y = rng.choice([rng.randint(20, 100), rng.randint(900, 980)]), rng.randint(h + 60, ALTURA - 60)
            brilho(s, x, y, 45, (120, 220, 255))
            pygame.draw.polygon(s, (150, 230, 255), [(x - 9, y + 18), (x, y - 26), (x + 9, y + 18)])
    elif d == "neve":
        for x in range(20, LARGURA, 80):
            desenhar_pinheiro(s, x + rng.randint(-10, 10), h + 2, rng.uniform(0.45, 0.6), (40, 110, 90), True)
        desenhar_pinheiro(s, 45, h + 110, 1.4, (35, 100, 85), True)
        desenhar_pinheiro(s, 960, h + 110, 1.4, (35, 100, 85), True)
        for _ in range(90):
            pygame.draw.circle(s, BRANCO, (rng.randint(0, LARGURA), rng.randint(0, ALTURA)), rng.randint(1, 3))
    elif d == "vulcao":
        for _ in range(12):
            x, y = rng.randint(0, LARGURA), rng.randint(h + 20, ALTURA - 20)
            pygame.draw.line(s, (255, 120, 40), (x, y), (x + rng.randint(30, 80), y + rng.randint(-8, 8)), 3)
            pygame.draw.line(s, (255, 200, 90), (x, y), (x + 20, y), 1)
        for _ in range(12):
            rx, ry = rng.randint(0, LARGURA), rng.randint(h + 10, ALTURA - 20)
            pygame.draw.ellipse(s, (60, 45, 48), R(rx, ry, rng.randint(24, 46), rng.randint(14, 22)))

    return s


def fundo_mapa(i):
    if i not in _cache_mapas:
        _cache_mapas[i] = construir_mapa(i)
    return _cache_mapas[i]


# ---------------------------------------------------------------- captura


def bolas_disponiveis():
    return [n for n in NOMES_BOLAS if inventario_bolas.get(n, 0) > 0]


def trocar_bola(delta):
    global bola_selecionada, mensagem
    lista = bolas_disponiveis()
    if not lista:
        mensagem = "Você está sem Pokébolas. Compre mais na loja."
        return
    if bola_selecionada in lista:
        idx = (lista.index(bola_selecionada) + delta) % len(lista)
    else:
        idx = 0
    bola_selecionada = lista[idx]


def chance_atual():
    if not pokemon_no_mapa:
        return 0
    chance = BOLAS[bola_selecionada][3]
    if chance >= 1.0:
        return 1.0
    return min(1.0, chance * POKEMON[pokemon_no_mapa]["facil"])


def criar_construcoes():
    global construcoes, pokemon_no_mapa, bola_voando, mensagem
    construcoes = []
    bola_voando = None
    for i in range(4):
        construcoes.append({"rect": pygame.Rect(430 + i * 55, 360, 45, 100), "vida": 3})
    pokemon_no_mapa = random.choice(MAPAS[mapa_atual]["pool"])
    mensagem = f"Um {pokemon_no_mapa} selvagem apareceu!"


def mudar_mapa(delta):
    global mapa_atual
    mapa_atual = (mapa_atual + delta) % len(MAPAS)
    criar_construcoes()


def lancar_bola(pos):
    global mensagem, bola_voando
    if bola_voando is not None:
        mensagem = "Espere a Pokébola terminar o arremesso."
        return
    if not pokemon_no_mapa:
        mensagem = "Não há Pokémon por perto. Procure outro!"
        return
    if inventario_bolas.get(bola_selecionada, 0) <= 0:
        trocar_bola(1)
        if inventario_bolas.get(bola_selecionada, 0) <= 0:
            return
    inventario_bolas[bola_selecionada] -= 1
    bola_voando = {"x": 172.0, "y": 445.0, "destino_x": float(pos[0]),
                   "destino_y": float(pos[1]), "nome": bola_selecionada, "rastro": []}


def atualizar_bola():
    global bola_voando, mensagem, pokemon_no_mapa, moedas
    if bola_voando is None:
        return
    b = bola_voando
    dx, dy = b["destino_x"] - b["x"], b["destino_y"] - b["y"]
    distancia = math.hypot(dx, dy)
    velocidade = 12
    b["rastro"].append((b["x"], b["y"]))
    b["rastro"] = b["rastro"][-8:]
    if distancia <= velocidade:
        b["x"], b["y"] = b["destino_x"], b["destino_y"]
    else:
        b["x"] += dx / distancia * velocidade
        b["y"] += dy / distancia * velocidade

    bola_rect = pygame.Rect(int(b["x"] - 10), int(b["y"] - 10), 20, 20)

    for c in construcoes[:]:
        if bola_rect.colliderect(c["rect"]):
            c["vida"] -= 1
            mensagem = "A Pokébola bateu na parede!"
            criar_particulas(b["x"], b["y"], (170, 120, 70), 14)
            if c["vida"] <= 0:
                criar_particulas(c["rect"].centerx, c["rect"].centery, (150, 105, 60), 30)
                construcoes.remove(c)
                mensagem = "A parede foi destruída!"
            bola_voando = None
            return

    if pokemon_no_mapa and bola_rect.colliderect(pokemon_rect):
        nome = pokemon_no_mapa
        chance = chance_atual()
        if random.random() <= chance:
            pokemon_capturados.append(nome)
            moedas += 20
            mensagem = f"Você capturou {nome}! +20 moedas"
            criar_particulas(pokemon_rect.centerx, pokemon_rect.centery, POKEMON[nome]["cor"], 40)
            criar_particulas(pokemon_rect.centerx, pokemon_rect.centery, OURO, 20)
            pokemon_no_mapa = None
        else:
            mensagem = f"{nome} escapou da Pokébola!"
            criar_particulas(b["x"], b["y"], BRANCO, 18)
        bola_voando = None
        return

    if distancia <= velocidade:
        mensagem = "A Pokébola não acertou o Pokémon."
        bola_voando = None


def desenhar_captura():
    m = MAPAS[mapa_atual]
    tela.blit(fundo_mapa(mapa_atual), (0, 0))
    mouse = pygame.mouse.get_pos()

    desenhar_treinador(140, 505)

    # Pokémon selvagem
    if pokemon_no_mapa:
        cx = pokemon_rect.centerx
        bob = math.sin(tempo * 0.004) * 4
        sombra_chao(cx, pokemon_rect.bottom + 4, 90, 20)
        spr = sprite_pokemon(pokemon_no_mapa, 120)
        tela.blit(spr, spr.get_rect(midbottom=(cx, pokemon_rect.bottom + 8 + bob)))
        tipo = POKEMON[pokemon_no_mapa]["tipo"]
        nome_img = FONTE_PEQUENA.render(pokemon_no_mapa, True, PRETO)
        larg = nome_img.get_width() + 70
        caixa = pygame.Rect(0, 0, larg, 26)
        caixa.midtop = (cx, pokemon_rect.bottom + 16)
        painel(caixa, alpha=210)
        tela.blit(nome_img, (caixa.x + 8, caixa.y + 4))
        chip_tipo(caixa.x + 14 + nome_img.get_width(), caixa.y + 4, tipo)

    # Paredes
    for c in construcoes:
        r = c["rect"]
        pygame.draw.rect(tela, (150, 100, 60), r, border_radius=4)
        for yy in (r.y + 33, r.y + 66):
            pygame.draw.line(tela, (110, 72, 40), (r.x, yy), (r.right, yy), 2)
        pygame.draw.line(tela, (110, 72, 40), (r.centerx, r.y), (r.centerx, r.y + 33), 2)
        pygame.draw.line(tela, (110, 72, 40), (r.x + 12, r.y + 33), (r.x + 12, r.y + 66), 2)
        pygame.draw.line(tela, (110, 72, 40), (r.right - 12, r.y + 66), (r.right - 12, r.bottom), 2)
        if c["vida"] < 3:
            pygame.draw.line(tela, PRETO, (r.x + 8, r.y + 10), (r.centerx, r.y + 40), 2)
            pygame.draw.line(tela, PRETO, (r.centerx, r.y + 40), (r.x + 14, r.y + 62), 2)
        if c["vida"] < 2:
            pygame.draw.line(tela, PRETO, (r.right - 8, r.y + 20), (r.centerx + 4, r.y + 55), 2)
        pygame.draw.rect(tela, PRETO, r, 2, border_radius=4)
        for k in range(3):
            pygame.draw.circle(tela, VERMELHO if k < c["vida"] else (90, 90, 90),
                               (r.x + 8 + k * 14, r.y - 10), 5)

    # Linha de mira
    if bola_voando is None and pokemon_no_mapa and mouse[1] < 630:
        ox, oy = 172, 445
        dist = math.hypot(mouse[0] - ox, mouse[1] - oy)
        if dist > 30:
            for k in range(1, int(dist // 16)):
                px = ox + (mouse[0] - ox) * (k * 16 / dist)
                py = oy + (mouse[1] - oy) * (k * 16 / dist)
                pygame.draw.circle(tela, BRANCO, (int(px), int(py)), 3)
                pygame.draw.circle(tela, BORDA, (int(px), int(py)), 3, 1)

    # Pokébola
    if bola_voando:
        cor = BOLAS[bola_voando["nome"]][4]
        for k, (rx, ry) in enumerate(bola_voando["rastro"]):
            pygame.draw.circle(tela, clarear(cor, 0.4), (int(rx), int(ry)), 2 + k)
        desenhar_bola(tela, (int(bola_voando["x"]), int(bola_voando["y"])), 12, cor)

    desenhar_particulas()

    # HUD
    painel(R(15, 12, 470, 98))
    texto(f"Mapa: {m['nome']}", 28, 18, PRETO, FONTE_NEGRITO)
    _, preco, forca, chance_b, cor_b = BOLAS[bola_selecionada]
    desenhar_bola(tela, (40, 66), 11, cor_b)
    texto(f"{bola_selecionada}  (x{inventario_bolas.get(bola_selecionada, 0)})", 60, 52, PRETO, FONTE)
    if pokemon_no_mapa:
        texto(f"Chance de captura: {int(chance_atual() * 100)}%", 28, 80, VERDE, FONTE_PEQUENA)
    texto("Clique no cenário para arremessar. Paredes bloqueiam!", 215, 82, (90, 90, 100), FONTE_MINI)

    painel(R(790, 12, 195, 66))
    texto(f"Moedas: {moedas}", 805, 18, (170, 120, 10), FONTE_NEGRITO)
    texto(f"Capturados: {len(pokemon_capturados)}", 805, 46, PRETO, FONTE_PEQUENA)

    painel(R(15, 590, 970, 40), alpha=215)
    texto(mensagem, 30, 598, PRETO, FONTE_PEQUENA)

    # Barra inferior
    pygame.draw.rect(tela, (35, 40, 60), R(0, 640, LARGURA, 80))
    botao(pygame.Rect(15, 652, 150, 46), "Voltar ao lobby", (120, 120, 140))
    botao(pygame.Rect(175, 652, 100, 46), "< Mapa", ROXO)
    botao(pygame.Rect(285, 652, 100, 46), "Mapa >", ROXO)
    botao(pygame.Rect(395, 652, 170, 46), "Outro Pokémon", VERDE)
    botao(pygame.Rect(590, 652, 40, 46), "<", AZUL)
    botao(pygame.Rect(945, 652, 40, 46), ">", AZUL)
    painel(R(636, 652, 303, 46), alpha=235)
    desenhar_bola(tela, (660, 675), 12, cor_b)
    texto(f"{bola_selecionada}", 682, 658, PRETO, FONTE_PEQUENA)
    texto(f"x{inventario_bolas.get(bola_selecionada, 0)}   força {forca}   chance {int(chance_b * 100)}%",
          682, 677, (90, 90, 100), FONTE_MINI)


# ---------------------------------------------------------------- lobby

bolinhas_lobby = [{"x": random.randint(0, LARGURA), "y": random.randint(0, ALTURA),
                   "r": random.randint(10, 24), "cor": random.choice(POKEBOLAS)[4],
                   "v": random.uniform(0.2, 0.7), "f": random.uniform(0, 6)} for _ in range(14)]


def rects_lobby():
    return [pygame.Rect(350, 160 + i * 72, 300, 58) for i in range(5)]


def pokemon_ativo():
    if ativo in pokemon_capturados:
        return ativo
    if pokemon_capturados:
        return pokemon_capturados[0]
    return None


def desenhar_lobby():
    tela.blit(fundo_gradiente("lobby", (110, 185, 245), (230, 245, 255)), (0, 0))
    for b in bolinhas_lobby:
        b["y"] -= b["v"]
        if b["y"] < -30:
            b["y"] = ALTURA + 30
            b["x"] = random.randint(0, LARGURA)
        x = b["x"] + math.sin(tempo * 0.001 + b["f"]) * 18
        s = pygame.Surface((b["r"] * 2 + 6, b["r"] * 2 + 6), pygame.SRCALPHA)
        desenhar_bola(s, (b["r"] + 3, b["r"] + 3), b["r"], b["cor"])
        s.set_alpha(110)
        tela.blit(s, (int(x), int(b["y"])))

    texto("CAPTURE E BATALHE", LARGURA // 2, 40, AZUL, FONTE_TITULO, centro=True, sombra=True)

    painel(R(25, 160, 305, 200))
    texto("Treinador", 45, 172, (80, 80, 110), FONTE_NEGRITO)
    texto(f"Moedas: {moedas}", 45, 208, (170, 120, 10), FONTE)
    texto(f"Pokémon capturados: {len(pokemon_capturados)}", 45, 238, PRETO, FONTE_PEQUENA)
    texto(f"Espécies: {len(set(pokemon_capturados))}/{len(POKEMON)}", 45, 262, PRETO, FONTE_PEQUENA)
    texto(f"Pokébolas: {sum(inventario_bolas.values())}", 45, 286, PRETO, FONTE_PEQUENA)
    texto(f"Líderes vencidos: {len(lideres_vencidos)}/{len(LIDERES)}", 45, 310, PRETO, FONTE_PEQUENA)

    painel(R(675, 160, 300, 260))
    texto("Pokémon ativo", 825, 172, (80, 80, 110), FONTE_NEGRITO, centro=True)
    p = pokemon_ativo()
    if p:
        bob = math.sin(tempo * 0.004) * 4
        sombra_chao(825, 330, 100, 20)
        spr = sprite_pokemon(p, 150)
        tela.blit(spr, spr.get_rect(midbottom=(825, 336 + bob)))
        texto(p, 825, 345, PRETO, FONTE_NEGRITO, centro=True)
        chip_tipo(825 - 30, 375, POKEMON[p]["tipo"])
    else:
        texto("Nenhum ainda.", 825, 255, (110, 110, 130), FONTE, centro=True)
        texto("Capture um Pokémon!", 825, 285, (110, 110, 130), FONTE_PEQUENA, centro=True)

    r = rects_lobby()
    botao(r[0], "Jogar captura", AZUL, fonte=FONTE_NEGRITO)
    botao(r[1], "Loja de Pokébolas", VERDE, fonte=FONTE_NEGRITO)
    botao(r[2], "Meus Pokémon", (230, 150, 50), fonte=FONTE_NEGRITO)
    botao(r[3], "Batalhar contra líderes", (170, 100, 200), fonte=FONTE_NEGRITO)
    botao(r[4], "Sair", (150, 70, 70), fonte=FONTE_NEGRITO)

    painel(R(25, 640, 950, 50), alpha=215)
    texto(mensagem, 40, 654, PRETO, FONTE_PEQUENA)


# ---------------------------------------------------------------- loja


def pos_card(i):
    return 25 + (i % 3) * 325, 85 + (i // 3) * 58


def rect_compra(i):
    x, y = pos_card(i)
    return pygame.Rect(x + 212, y + 10, 80, 28)


def desenhar_loja():
    tela.blit(fundo_gradiente("loja", (225, 235, 255), (250, 245, 235)), (0, 0))
    texto("LOJA DE POKÉBOLAS", 330, 15, AZUL, FONTE_TITULO if False else FONTE_SUB, sombra=True)
    painel(R(760, 12, 215, 40))
    texto(f"Moedas: {moedas}", 775, 20, (170, 120, 10), FONTE_NEGRITO)

    for i, (nome, preco, forca, chance, cor) in enumerate(POKEBOLAS):
        x, y = pos_card(i)
        painel(R(x, y, 300, 48), alpha=240)
        desenhar_bola(tela, (x + 24, y + 24), 13, cor)
        texto(nome, x + 46, y + 4, PRETO, FONTE_PEQUENA)
        texto(f"{int(chance * 100)}% · força {forca} · tem {inventario_bolas.get(nome, 0)}",
              x + 46, y + 27, (100, 100, 115), FONTE_MINI)
        pode = moedas >= preco
        botao(rect_compra(i), f"{preco} $", VERDE if pode else (150, 150, 155), pode, FONTE_PEQUENA)

    painel(R(230, 652, 745, 44), alpha=220)
    texto(mensagem, 245, 662, PRETO, FONTE_PEQUENA)
    botao(pygame.Rect(25, 652, 190, 44), "Voltar ao lobby", (120, 120, 140))


def comprar_pokebola(indice):
    global moedas, mensagem
    nome, preco, _, _, _ = POKEBOLAS[indice]
    if moedas >= preco:
        moedas -= preco
        inventario_bolas[nome] = inventario_bolas.get(nome, 0) + 1
        mensagem = f"Você comprou: {nome}!"
    else:
        mensagem = "Você não tem moedas suficientes."


# ---------------------------------------------------------------- coleção


def rect_celula(i):
    return pygame.Rect(50 + (i % 6) * 150, 85 + (i // 6) * 135, 140, 125)


def desenhar_colecao():
    tela.blit(fundo_gradiente("colecao", (255, 238, 205), (255, 250, 235)), (0, 0))
    texto("MEUS POKÉMON", LARGURA // 2, 18, (190, 110, 20), FONTE_SUB, centro=True, sombra=True)
    texto("Clique em um Pokémon capturado para usá-lo nas batalhas", LARGURA // 2, 54,
          (110, 90, 60), FONTE_PEQUENA, centro=True)
    atual = pokemon_ativo()
    for i, nome in enumerate(NOMES_POKEMON):
        r = rect_celula(i)
        qtd = pokemon_capturados.count(nome)
        selecionado = nome == atual
        painel(r, (255, 248, 220) if selecionado else BRANCO, 240,
               OURO if selecionado else BORDA)
        if selecionado:
            pygame.draw.rect(tela, OURO, r, 4, border_radius=14)
        if qtd:
            spr = sprite_pokemon(nome, 78)
            tela.blit(spr, spr.get_rect(midtop=(r.centerx, r.y + 6)))
            texto(nome, r.centerx, r.y + 86, PRETO, FONTE_PEQUENA, centro=True)
            texto(f"x{qtd}", r.right - 10 - FONTE_MINI.size(f"x{qtd}")[0], r.y + 6, (110, 110, 130), FONTE_MINI)
            chip_tipo(r.centerx - 25, r.y + 104, POKEMON[nome]["tipo"])
        else:
            spr = silhueta(nome, 78)
            tela.blit(spr, spr.get_rect(midtop=(r.centerx, r.y + 6)))
            texto("???", r.centerx, r.y + 86, (130, 130, 145), FONTE_PEQUENA, centro=True)
    botao(pygame.Rect(25, 652, 190, 44), "Voltar ao lobby", (120, 120, 140))
    painel(R(230, 652, 745, 44), alpha=220)
    texto(f"Espécies descobertas: {len(set(pokemon_capturados))}/{len(POKEMON)}   |   Ativo: {atual or '-'}",
          245, 662, PRETO, FONTE_PEQUENA)


# ---------------------------------------------------------------- líderes


def rect_lider(i):
    return pygame.Rect(60 + (i % 2) * 450, 105 + (i // 2) * 130, 430, 110)


def desenhar_selecao_lider():
    tela.blit(fundo_gradiente("lideres", (215, 205, 245), (245, 240, 255)), (0, 0))
    texto("ESCOLHA UM LÍDER", LARGURA // 2, 25, (110, 60, 160), FONTE_SUB, centro=True, sombra=True)
    p = pokemon_ativo() or "Pikachu"
    texto(f"Seu Pokémon: {p}", LARGURA // 2, 65, (90, 70, 120), FONTE_PEQUENA, centro=True)
    for i, lider in enumerate(LIDERES):
        r = rect_lider(i)
        sobre = r.collidepoint(pygame.mouse.get_pos())
        painel(r, (250, 245, 255) if sobre else BRANCO, 245, ROXO)
        spr = sprite_pokemon(lider["pokemon"], 86)
        tela.blit(spr, spr.get_rect(midleft=(r.x + 10, r.centery)))
        texto(lider["nome"], r.x + 110, r.y + 12, PRETO, FONTE_NEGRITO)
        texto(f"Pokémon: {lider['pokemon']}", r.x + 110, r.y + 44, (90, 90, 110), FONTE_PEQUENA)
        chip_tipo(r.x + 110, r.y + 70, lider["tipo"])
        texto(f"+{lider['recompensa']} moedas", r.x + 110 + 80, r.y + 72, (170, 120, 10), FONTE_MINI)
        if i in lideres_vencidos:
            pygame.draw.circle(tela, OURO, (r.right - 30, r.y + 30), 16)
            pygame.draw.circle(tela, (180, 130, 20), (r.right - 30, r.y + 30), 16, 3)
            texto("✓", r.right - 36, r.y + 20, (150, 100, 10), FONTE_NEGRITO)
    botao(pygame.Rect(25, 652, 190, 44), "Voltar ao lobby", (120, 120, 140))


# ---------------------------------------------------------------- batalha


def iniciar_batalha(indice):
    global lider_idx, lider_batalha, jogador_batalha, hp_jogador, hp_lider
    global hp_lider_max, hp_exib_jogador, hp_exib_lider, fase, timer_fase
    global msg_batalha, tela_atual, tremer_j, tremer_l
    lider_idx = indice
    lider_batalha = LIDERES[indice]
    jogador_batalha = pokemon_ativo() or "Pikachu"
    hp_jogador = hp_jogador_max
    hp_lider_max = lider_batalha["hp"]
    hp_lider = hp_lider_max
    hp_exib_jogador, hp_exib_lider = float(hp_jogador), float(hp_lider)
    fase, timer_fase = "escolha", 0
    tremer_j = tremer_l = 0
    msg_batalha = [f"{lider_batalha['nome']} quer batalhar!", "Escolha um ataque."]
    tela_atual = "batalha"


def atacar_ginasio(indice_ataque):
    global hp_lider, fase, timer_fase, msg_batalha, tremer_l
    if fase != "escolha":
        return
    nome, tipo, base = POKEMON[jogador_batalha]["ataques"][indice_ataque]
    mult = multiplicador(tipo, lider_batalha["tipo"])
    dano = int(base * mult) + random.randint(0, 4)
    hp_lider = max(0, hp_lider - dano)
    efeito = "Foi super efetivo!" if mult > 1 else ("Não foi muito efetivo..." if mult < 1 else "")
    msg_batalha = [f"{jogador_batalha} usou {nome}! (-{dano} HP)", efeito]
    tremer_l = 18
    criar_particulas(730, 190, TIPO_COR[tipo], 24)
    if hp_lider <= 0:
        fase, timer_fase = "vitoria", 70
    else:
        fase, timer_fase = "inimigo", 55


def contra_ataque():
    global hp_jogador, fase, msg_batalha, tremer_j
    nome, tipo, base = random.choice(POKEMON[lider_batalha["pokemon"]]["ataques"])
    mult = multiplicador(tipo, POKEMON[jogador_batalha]["tipo"])
    dano = int(base * 0.7 * mult) + random.randint(0, 3) + lider_idx
    hp_jogador = max(0, hp_jogador - dano)
    efeito = "Foi super efetivo!" if mult > 1 else ("Não foi muito efetivo..." if mult < 1 else "")
    msg_batalha = [f"{lider_batalha['pokemon']} usou {nome}! (-{dano} HP)", efeito]
    tremer_j = 18
    criar_particulas(270, 360, TIPO_COR[tipo], 24)
    if hp_jogador <= 0:
        fase = "derrota"
        return True
    fase = "escolha"
    return False


def atualizar_batalha():
    global timer_fase, tela_atual, resultado, resultado_sub, moedas, venceu
    global hp_exib_jogador, hp_exib_lider, tremer_j, tremer_l, fase
    hp_exib_jogador += clamp(hp_jogador - hp_exib_jogador, -0.8, 0.8)
    hp_exib_lider += clamp(hp_lider - hp_exib_lider, -0.8, 0.8)
    tremer_j = max(0, tremer_j - 1)
    tremer_l = max(0, tremer_l - 1)
    if timer_fase > 0:
        timer_fase -= 1
        if timer_fase == 0:
            if fase == "inimigo":
                if contra_ataque():
                    timer_fase = 70
            elif fase == "vitoria":
                venceu = True
                resultado = f"Vitória! Você venceu {lider_batalha['nome']}!"
                resultado_sub = f"+{lider_batalha['recompensa']} moedas"
                moedas += lider_batalha["recompensa"]
                lideres_vencidos.add(lider_idx)
                tela_atual = "resultado"
            elif fase == "derrota":
                venceu = False
                resultado = "Você perdeu a batalha."
                resultado_sub = "Capture Pokémon mais fortes e tente de novo!"
                tela_atual = "resultado"


def caixa_info(x, y, nome, tipo, atual, exib, maximo, numeros):
    painel(R(x, y, 330, 82), alpha=235)
    texto(nome, x + 14, y + 8, PRETO, FONTE_NEGRITO)
    chip_tipo(x + 24 + FONTE_NEGRITO.size(nome)[0], y + 12, tipo)
    texto("HP", x + 14, y + 40, (110, 110, 125), FONTE_MINI)
    barra_hp(x + 40, y + 40, 270, exib, maximo)
    if numeros:
        texto(f"{int(atual)}/{maximo}", x + 14, y + 60, PRETO, FONTE_MINI)


def desenhar_batalha():
    tela.blit(fundo_gradiente("arena", (130, 200, 245), (190, 230, 190)), (0, 0))
    pygame.draw.rect(tela, (120, 190, 110), R(0, 300, LARGURA, 260))
    pygame.draw.rect(tela, (108, 176, 100), R(0, 380, LARGURA, 180))
    pygame.draw.line(tela, (80, 140, 80), (0, 300), (LARGURA, 300), 3)
    texto(f"Batalha contra {lider_batalha['nome']}", LARGURA // 2, 12, PRETO, FONTE_SUB, centro=True, sombra=True)

    # plataformas
    for cx, cy, w, h in ((730, 305, 260, 60), (270, 470, 320, 70)):
        pygame.draw.ellipse(tela, (90, 150, 85), R(cx - w / 2, cy - h / 2 + 8, w, h))
        pygame.draw.ellipse(tela, (150, 210, 130), R(cx - w / 2, cy - h / 2, w, h))
        pygame.draw.ellipse(tela, (70, 120, 70), R(cx - w / 2, cy - h / 2, w, h), 3)

    ox = random.randint(-6, 6) if tremer_l else 0
    oj = random.randint(-6, 6) if tremer_j else 0
    bob = math.sin(tempo * 0.004) * 4
    s_l = sprite_pokemon(lider_batalha["pokemon"], 190)
    tela.blit(s_l, s_l.get_rect(midbottom=(730 + ox, 305 + bob)))
    s_j = sprite_pokemon(jogador_batalha, 230)
    tela.blit(s_j, s_j.get_rect(midbottom=(270 + oj, 480 - bob)))

    desenhar_particulas()

    caixa_info(40, 50, lider_batalha["pokemon"], lider_batalha["tipo"], hp_lider, hp_exib_lider, hp_lider_max, False)
    caixa_info(620, 345, jogador_batalha, POKEMON[jogador_batalha]["tipo"], hp_jogador, hp_exib_jogador, hp_jogador_max, True)

    pygame.draw.rect(tela, (35, 40, 60), R(0, 548, LARGURA, 172))
    painel(R(25, 562, 450, 130), (250, 250, 255), 250)
    texto(msg_batalha[0], 42, 585, PRETO, FONTE)
    texto(msg_batalha[1], 42, 620, (170, 60, 60), FONTE_NEGRITO)
    if fase == "escolha":
        texto("Sua vez!", 42, 660, (90, 90, 110), FONTE_MINI)

    for i, (nome, tipo, dano) in enumerate(POKEMON[jogador_batalha]["ataques"]):
        r = pygame.Rect(500 + (i % 2) * 240, 562 + (i // 2) * 66, 230, 58)
        botao(r, nome, TIPO_COR[tipo], fase == "escolha", FONTE_PEQUENA)
        texto(f"{tipo} · dano {dano}", r.centerx, r.bottom - 22, BRANCO, FONTE_MINI, centro=True)


def desenhar_resultado():
    tela.blit(fundo_gradiente("resultado", (200, 225, 255) if venceu else (235, 205, 205),
                              (245, 250, 255) if venceu else (255, 240, 240)), (0, 0))
    painel(R(180, 150, 640, 270), alpha=240)
    texto(resultado, LARGURA // 2, 200, VERDE if venceu else VERMELHO, FONTE_SUB, centro=True)
    texto(resultado_sub, LARGURA // 2, 260, (170, 120, 10) if venceu else PRETO, FONTE_NEGRITO, centro=True)
    if venceu:
        for k in range(3):
            pygame.draw.circle(tela, OURO, (LARGURA // 2 - 60 + k * 60, 330), 20)
            pygame.draw.circle(tela, (180, 130, 20), (LARGURA // 2 - 60 + k * 60, 330), 20, 3)
    botao(pygame.Rect(350, 450, 300, 55), "Voltar ao lobby", AZUL, fonte=FONTE_NEGRITO)


def voltar_lobby():
    global tela_atual
    tela_atual = "lobby"


# ---------------------------------------------------------------- loop principal

rodando = True

while rodando:
    tempo = pygame.time.get_ticks()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE and tela_atual != "lobby":
            voltar_lobby()

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            pos = evento.pos

            if tela_atual == "lobby":
                r = rects_lobby()
                if r[0].collidepoint(pos):
                    tela_atual = "captura"
                    criar_construcoes()
                elif r[1].collidepoint(pos):
                    tela_atual = "loja"
                    mensagem = "Compre Pokébolas com suas moedas."
                elif r[2].collidepoint(pos):
                    tela_atual = "colecao"
                elif r[3].collidepoint(pos):
                    tela_atual = "lideres"
                elif r[4].collidepoint(pos):
                    rodando = False

            elif tela_atual == "loja":
                if pygame.Rect(25, 652, 190, 44).collidepoint(pos):
                    voltar_lobby()
                else:
                    for i in range(len(POKEBOLAS)):
                        if rect_compra(i).collidepoint(pos):
                            comprar_pokebola(i)
                            break

            elif tela_atual == "colecao":
                if pygame.Rect(25, 652, 190, 44).collidepoint(pos):
                    voltar_lobby()
                else:
                    for i, nome in enumerate(NOMES_POKEMON):
                        if rect_celula(i).collidepoint(pos) and nome in pokemon_capturados:
                            ativo = nome
                            mensagem = f"{nome} agora é seu Pokémon ativo!"
                            break

            elif tela_atual == "captura":
                if pygame.Rect(15, 652, 150, 46).collidepoint(pos):
                    voltar_lobby()
                elif pygame.Rect(175, 652, 100, 46).collidepoint(pos):
                    mudar_mapa(-1)
                elif pygame.Rect(285, 652, 100, 46).collidepoint(pos):
                    mudar_mapa(1)
                elif pygame.Rect(395, 652, 170, 46).collidepoint(pos):
                    criar_construcoes()
                elif pygame.Rect(590, 652, 40, 46).collidepoint(pos):
                    trocar_bola(-1)
                elif pygame.Rect(945, 652, 40, 46).collidepoint(pos):
                    trocar_bola(1)
                elif pos[1] < 630:
                    lancar_bola(pos)

            elif tela_atual == "lideres":
                if pygame.Rect(25, 652, 190, 44).collidepoint(pos):
                    voltar_lobby()
                else:
                    for i in range(len(LIDERES)):
                        if rect_lider(i).collidepoint(pos):
                            iniciar_batalha(i)
                            break

            elif tela_atual == "batalha":
                for i in range(4):
                    if pygame.Rect(500 + (i % 2) * 240, 562 + (i // 2) * 66, 230, 58).collidepoint(pos):
                        atacar_ginasio(i)
                        break

            elif tela_atual == "resultado":
                if pygame.Rect(350, 450, 300, 55).collidepoint(pos):
                    voltar_lobby()

    if tela_atual == "captura":
        atualizar_bola()
    if tela_atual == "batalha":
        atualizar_batalha()
    atualizar_particulas()

    if tela_atual == "lobby":
        desenhar_lobby()
    elif tela_atual == "loja":
        desenhar_loja()
    elif tela_atual == "colecao":
        desenhar_colecao()
    elif tela_atual == "captura":
        desenhar_captura()
    elif tela_atual == "lideres":
        desenhar_selecao_lider()
    elif tela_atual == "batalha":
        desenhar_batalha()
    elif tela_atual == "resultado":
        desenhar_resultado()

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
