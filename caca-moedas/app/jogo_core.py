import random
from dataclasses import dataclass

@dataclass
class Rect:
    x: int; y: int; w: int; h: int
    def colliderect(self, other: "Rect") -> bool:
        return not (self.x + self.w < other.x or other.x + other.w < self.x or
                    self.y + self.h < other.y or other.y + other.h < self.y)

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
        self.obstaculos: list[Rect] = []
        for _ in range(5):
            while True:
                r = Rect(random.randint(0, largura - 20), random.randint(0, altura - 20), 20, 20)
                if not self._player_rect().colliderect(r):
                    self.obstaculos.append(r); break

    def _player_rect(self) -> Rect:
        return Rect(self.player_x, self.player_y, self.player_w, self.player_h)

    def _clamp_player(self):
        self.player_x = max(0, min(self.player_x, self.largura))
        self.player_y = max(0, min(self.player_y, self.altura))

    def _check_win(self):
        if self.score >= self.meta:
            self.estado = "WON"

    def _check_timeout(self):
        if self.tempo <= 0 and self.estado == "RUNNING" and self.score < self.meta:
            self.estado = "LOST"

    # ---------- API compatível com os testes ----------
    def mover(self, dx, dy):
        if self.estado != "RUNNING": return
        self.player_x += dx; self.player_y += dy
        self._clamp_player()

    def coletar_moeda(self):
        """Imita: se colidir com moeda e não venceu, score++ e moeda realoca."""
        if self.estado != "RUNNING": return
        if self._player_rect().colliderect(self.moeda):
            if self.score < self.meta:
                self.score += 1
            # moeda reposiciona (como no jogo)
            self.moeda.x = random.randint(0, self.largura - self.moeda.w)
            self.moeda.y = random.randint(0, self.altura - self.moeda.h)
            self._check_win()

    def colisao_obstaculo(self):
        """Atalho para forçar derrota (equivalente a encostar num obstáculo)."""
        if self.estado == "RUNNING":
            self.estado = "LOST"

    def checar_colisao_obstaculos(self):
        if self.estado != "RUNNING": return
        pr = self._player_rect()
        for o in self.obstaculos:
            if pr.colliderect(o):
                self.estado = "LOST"; break

    def tick(self, ms):
        """Avança o relógio em milissegundos; realoca obstáculos a cada 3s."""
        if self.estado != "RUNNING": return
        if ms < 0: raise ValueError("ms deve ser >= 0")
        self.tempo -= int(ms)
        if self.tempo < 0: self.tempo = 0
        self._elapsed += ms / 1000.0

        # shuffle obstáculos a cada intervalo_mudanca
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
        self.__init__(self.largura, self.altura, self._tempo_inicial, self.meta, self.intervalo_mudanca, seed=42)


