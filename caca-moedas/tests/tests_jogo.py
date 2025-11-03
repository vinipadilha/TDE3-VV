import unittest
from app.jogo_core import Jogo

class TestCacaMoedas(unittest.TestCase):

    def setUp(self):
        self.jogo = Jogo(largura=800, altura=600, tempo_ms=30000, meta=7, seed=1)

    # CT1 — Movimentação dentro dos limites
    def test_movimentacao_dentro_limites(self):
        for dx, dy in [(-2000,0),(2000,0),(0,-2000),(0,2000)]:
            self.jogo.mover(dx, dy)
            self.assertGreaterEqual(self.jogo.player_x, 0)
            self.assertLessEqual(self.jogo.player_x, self.jogo.largura)
            self.assertGreaterEqual(self.jogo.player_y, 0)
            self.assertLessEqual(self.jogo.player_y, self.jogo.altura)
        self.assertEqual(self.jogo.estado, "RUNNING")

    # CT2 — Coletar moeda incrementa pontuação
    def test_coletar_moeda_incrementa_score(self):
        # coloca o jogador sobre a moeda, movendo até colidir
        self.jogo.player_x = self.jogo.moeda.x
        self.jogo.player_y = self.jogo.moeda.y
        antes = self.jogo.score
        self.jogo.coletar_moeda()
        self.assertEqual(self.jogo.score, antes + 1)
        self.assertIn(self.jogo.estado, ("RUNNING", "WON"))

    # CT3 — Colisão com obstáculo => derrota
    def test_colisao_resulta_derrota(self):
        self.jogo.colisao_obstaculo()
        self.assertEqual(self.jogo.estado, "LOST")

    # CT4 — Tempo chega a zero => derrota (se não venceu)
    def test_tempo_em_zero_derrota(self):
        j = Jogo(tempo_ms=1000, meta=7, seed=2)
        self.assertEqual(j.estado, "RUNNING")
        j.tick(1000)  # esgota
        self.assertEqual(j.tempo, 0)
        self.assertEqual(j.estado, "LOST")

    # CT5 — Vitória ao atingir meta
    def test_vitoria_ao_atingir_meta(self):
        j = Jogo(meta=3, seed=3)
        for _ in range(2):
            j.player_x, j.player_y = j.moeda.x, j.moeda.y
            j.coletar_moeda()
            self.assertEqual(j.estado, "RUNNING")
        # 3ª moeda
        j.player_x, j.player_y = j.moeda.x, j.moeda.y
        j.coletar_moeda()
        self.assertEqual(j.score, 3)
        self.assertEqual(j.estado, "WON")
        # não passa da meta após vitória
        j.player_x, j.player_y = j.moeda.x, j.moeda.y
        j.coletar_moeda()
        self.assertEqual(j.score, 3)

    # CT6 — Reiniciar após estado terminal
    def test_reiniciar_pos_estado_terminal(self):
        self.jogo.colisao_obstaculo()
        self.assertEqual(self.jogo.estado, "LOST")
        self.jogo.reiniciar()
        self.assertEqual(self.jogo.estado, "RUNNING")
        self.assertEqual(self.jogo.score, 0)
        self.assertGreater(self.jogo.tempo, 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
