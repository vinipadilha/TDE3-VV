import unittest
from app.jogo_core import Jogo

class TestCacaMoedas(unittest.TestCase):
    def setUp(self):
        # Executa antes de cada teste, com paramétros padrão
        self.jogo = Jogo(largura=800, altura=600, tempo_ms=30000, meta=7, seed=1)

    # CT1 - Movimentação dentro dos limites da tela
    def test_movimentacao_dentro_limites(self):
        # move o jogador nas 4 direções extremas e verifica se ele permanece dentro dos limites da tela
        for dx, dy in [(-2000,0),(2000,0),(0,-2000),(0,2000)]:
            self.jogo.mover(dx, dy)
            self.assertGreaterEqual(self.jogo.player_x, 0) 
            self.assertLessEqual(self.jogo.player_x, self.jogo.largura)
            self.assertGreaterEqual(self.jogo.player_y, 0) 
            self.assertLessEqual(self.jogo.player_y, self.jogo.altura)
        self.assertEqual(self.jogo.estado, "RUNNING")


    # CT2 - Coletar moeda incrementa pontuação
    def test_coletar_moeda_incrementa_score(self):
        # teste se colocar uma moeda aumenta o score pra 1
        self.jogo.player_x = self.jogo.moeda.x 
        self.jogo.player_y = self.jogo.moeda.y
        antes = self.jogo.score
        self.jogo.coletar_moeda() 
        self.assertEqual(self.jogo.score, antes + 1) 
        self.assertIn(self.jogo.estado, ("RUNNING", "WON")) 


    # CT3 - Colisão com obstáculo resulta em derrota
    def test_colisao_resulta_derrota(self):
        # simula uma colisão e e verifica se muda o estado para LOST
        self.jogo.colisao_obstaculo() 
        self.assertEqual(self.jogo.estado, "LOST")  


    # CT4 — Tempo chegando a zero resulta em derrota
    def test_tempo_em_zero_derrota(self):
        # Cria um jogo muito curto, e adianta o tempo para zero, verificando se o estado muda para LOST
        j = Jogo(tempo_ms=1000, meta=7, seed=2) 
        self.assertEqual(j.estado, "RUNNING")  
        j.tick(1000)  
        self.assertEqual(j.tempo, 0)  
        self.assertEqual(j.estado, "LOST")


    # CT5 - Vitória ao atingir a meta de moedas
    def test_vitoria_ao_atingir_meta(self):
        # Testa se ao atingir a meta de moedas, o jogo termina em vitória. Também verifica que após vencer, coletar mais moedas não aumenta o score.
        j = Jogo(meta=3, seed=3) 
        for _ in range(2):  
            j.player_x, j.player_y = j.moeda.x, j.moeda.y  
            j.coletar_moeda()
            self.assertEqual(j.estado, "RUNNING")  
        j.player_x, j.player_y = j.moeda.x, j.moeda.y
        j.coletar_moeda()
        self.assertEqual(j.score, 3) 
        self.assertEqual(j.estado, "WON")  

        # adicional: verifica que após vencer, coletar mais moedas não aumenta o score além da meta 
        j.player_x, j.player_y = j.moeda.x, j.moeda.y
        j.coletar_moeda()
        self.assertEqual(j.score, 3)  # O score deve permanecer em 3, não aumentar para 4


    # CT6 - Reiniciar após estado terminal 
    def test_reiniciar_pos_estado_terminal(self):
        # Testa se reiniciar o jogo após uma derrota (ou vitória) reseta corretamente todas as variáveis para o estado inicial.
        self.jogo.colisao_obstaculo()  
        self.assertEqual(self.jogo.estado, "LOST") 
        self.jogo.reiniciar()  
        self.assertEqual(self.jogo.estado, "RUNNING")  
        self.assertEqual(self.jogo.score, 0) 
        self.assertGreater(self.jogo.tempo, 0)  


# Quando este arquivo é executado diretamente (não importado como módulo), executa todos os testes definidos nesta classe.
# verbosity=2 significa que os testes mostrarão informações detalhadas sobre cada teste executado (nome do teste, resultado, etc.)
if __name__ == "__main__":
    unittest.main(verbosity=2)
