import random
from dataclasses import dataclass

# Classe Rect: representa uma área retangular no jogo (jogador, moedas, obstáculos)
@dataclass
class Rect:
    x: int
    y: int 
    w: int  
    h: int  
    
    def colliderect(self, other: "Rect") -> bool:
        # Verifica se este retângulo colide com outro retângulo
        return not (self.x + self.w < other.x or other.x + other.w < self.x or
                    self.y + self.h < other.y or other.y + other.h < self.y)


# Classe Jogo: implementa a lógica principal do jogo 
class Jogo:
    def __init__(self, largura=800, altura=600, tempo_ms=30000, meta=7,
                 intervalo_mudanca=3, seed: int | None = 42):
        if seed is not None:
            random.seed(seed)
        
        
        self.largura = largura
        self.altura = altura 
        self.meta = meta  
        
        self.player_w, self.player_h = 40, 30
        self.player_x, self.player_y = largura // 2, altura // 2 
        
        self.score = 0 
        self.estado = "RUNNING"

        self._tempo_inicial = int(tempo_ms) 
        self.tempo = int(tempo_ms)  
        self.intervalo_mudanca = intervalo_mudanca 
        self._elapsed = 0  
        self._ultimo_shuffle = 0  
        self.speed = 20 

        self.moeda = Rect(random.randint(0, largura - 15), random.randint(0, altura - 15), 15, 15)
        
        # Cria 5 obstáculos em posições aleatórias
        self.obstaculos: list[Rect] = []
        for _ in range(5):
            while True:
                r = Rect(random.randint(0, largura - 20), random.randint(0, altura - 20), 20, 20)
                if not self._player_rect().colliderect(r): 
                    self.obstaculos.append(r); break

    def _player_rect(self) -> Rect:
        return Rect(self.player_x, self.player_y, self.player_w, self.player_h)  # Retorna um objeto Rect representando a posição atual do jogador

    def _clamp_player(self):
        # Limita a posição do jogador dentro dos limites da tela
        self.player_x = max(0, min(self.player_x, self.largura))
        self.player_y = max(0, min(self.player_y, self.altura))

    def _check_win(self):
        # Verifica se o jogador atingiu a meta (número de moedas necessárias) e muda o estado para "WON" se sim
        if self.score >= self.meta:
            self.estado = "WON"

    def _check_timeout(self):
        # Verifica se o tempo acabou sem o jogador ter vencido (se o tempo chegou a zero e o jogador não atingiu a meta, perde o jogo)
        if self.tempo <= 0 and self.estado == "RUNNING" and self.score < self.meta:
            self.estado = "LOST"

    def mover(self, dx, dy):
        # Move o jogador na direção especificada (dx: deslocamento horizontal, dy: deslocamento vertical)
        if self.estado != "RUNNING": return
        self.player_x += dx; self.player_y += dy
        self._clamp_player()

    def coletar_moeda(self):
        # Verifica se o jogador está colidindo com a moeda e, se sim: incrementa o score (se ainda não venceu), reposiciona a moeda e verifica se o jogador venceu
        # Só funciona se o jogo estiver em estado "RUNNING"
        if self.estado != "RUNNING": return
        if self._player_rect().colliderect(self.moeda):
            if self.score < self.meta:
                self.score += 1
            self.moeda.x = random.randint(0, self.largura - self.moeda.w)
            self.moeda.y = random.randint(0, self.altura - self.moeda.h)
            self._check_win()

    def colisao_obstaculo(self):
        # Força uma derrota imediata (equivalente a colidir com um obstáculo). Usado principalmente nos testes para simular colisões
        if self.estado == "RUNNING":
            self.estado = "LOST"

    def checar_colisao_obstaculos(self):
        # Verifica se o jogador está colidindo com algum obstáculo. Se houver colisão, muda o estado para "LOST"
        if self.estado != "RUNNING": return
        pr = self._player_rect()
        for o in self.obstaculos:
            if pr.colliderect(o):
                self.estado = "LOST"; break

    def tick(self, ms):
        # Avança o relógio do jogo em milissegundos. Decrementa o tempo restante, atualiza o tempo decorrido,
        if self.estado != "RUNNING": return
        if ms < 0: raise ValueError("ms deve ser >= 0")
        self.tempo -= int(ms)
        if self.tempo < 0: self.tempo = 0
        self._elapsed += ms / 1000.0 

        if (self._elapsed - self._ultimo_shuffle) > self.intervalo_mudanca:
            for i in range(len(self.obstaculos)):
                while True:
                    r = Rect(random.randint(0, self.largura - 20), 
                             random.randint(0, self.altura - 20), 20, 20)
                    if not self._player_rect().colliderect(r):  
                        self.obstaculos[i] = r; break
            self._ultimo_shuffle = self._elapsed


        self._check_timeout()
        self._check_win()

    def reiniciar(self):
        # Reinicia o jogo para o estado inicial 
        self.__init__(self.largura, self.altura, self._tempo_inicial, self.meta, self.intervalo_mudanca, seed=42)

