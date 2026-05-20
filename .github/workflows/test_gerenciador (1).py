"""
=============================================================
 TechFlow Solutions — Testes Unitários
 Arquivo: test_gerenciador.py
 Execute: pytest test_gerenciador.py -v
=============================================================
"""

import json
import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gerenciador_tarefas as g


# ══════════════════════════════════════════════════════════
#  FIXTURES
# ══════════════════════════════════════════════════════════

@pytest.fixture
def tarefas_exemplo():
    """Lista de tarefas fictícias reutilizável nos testes."""
    return [
        {
            "id": 1,
            "titulo": "Criar repositório GitHub",
            "descricao": "Criar repo público com README",
            "status": "Concluído",
            "prioridade": "Alta",
            "criada_em": "19/05/2025 09:00",
            "concluida_em": "19/05/2025 10:00",
        },
        {
            "id": 2,
            "titulo": "Configurar GitHub Actions",
            "descricao": "Pipeline de CI com pytest",
            "status": "Em Progresso",
            "prioridade": "Alta",
            "criada_em": "19/05/2025 10:00",
            "concluida_em": None,
        },
        {
            "id": 3,
            "titulo": "Escrever testes unitários",
            "descricao": "Cobrir todas as funções CRUD",
            "status": "A Fazer",
            "prioridade": "Média",
            "criada_em": "19/05/2025 11:00",
            "concluida_em": None,
        },
        {
            "id": 4,
            "titulo": "Documentar README",
            "descricao": "Escopo e metodologia",
            "status": "A Fazer",
            "prioridade": "Baixa",
            "criada_em": "19/05/2025 11:30",
            "concluida_em": None,
        },
    ]


@pytest.fixture
def arquivo_json(tmp_path, monkeypatch, tarefas_exemplo):
    """
    Cria um JSON temporário e redireciona ARQUIVO_DADOS para ele.
    Garante isolamento completo entre testes.
    """
    arquivo = tmp_path / "tarefas_teste.json"
    arquivo.write_text(
        json.dumps(tarefas_exemplo, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    monkeypatch.setattr(g, "ARQUIVO_DADOS", str(arquivo))
    return str(arquivo)


# ══════════════════════════════════════════════════════════
#  BLOCO 1 — gerar_id
# ══════════════════════════════════════════════════════════

class TestGerarId:
    def test_lista_vazia_retorna_1(self):
        assert g.gerar_id([]) == 1

    def test_incrementa_maior_id(self, tarefas_exemplo):
        assert g.gerar_id(tarefas_exemplo) == 5

    def test_lista_com_um_elemento(self):
        assert g.gerar_id([{"id": 7, "titulo": "x"}]) == 8

    def test_ids_fora_de_ordem(self):
        tarefas = [{"id": 3}, {"id": 1}, {"id": 5}, {"id": 2}]
        assert g.gerar_id(tarefas) == 6


# ══════════════════════════════════════════════════════════
#  BLOCO 2 — carregar_tarefas / salvar_tarefas
# ══════════════════════════════════════════════════════════

class TestPersistencia:
    def test_carregar_retorna_lista(self, arquivo_json):
        assert isinstance(g.carregar_tarefas(), list)

    def test_carregar_quantidade_correta(self, arquivo_json):
        assert len(g.carregar_tarefas()) == 4

    def test_carregar_arquivo_inexistente(self, monkeypatch, tmp_path):
        monkeypatch.setattr(g, "ARQUIVO_DADOS", str(tmp_path / "nao_existe.json"))
        assert g.carregar_tarefas() == []

    def test_salvar_e_recarregar(self, arquivo_json, tarefas_exemplo):
        nova = {
            "id": 99, "titulo": "Nova tarefa salva",
            "descricao": "Persistência", "status": "A Fazer",
            "prioridade": "Baixa", "criada_em": "01/01/2025 00:00",
            "concluida_em": None,
        }
        tarefas_exemplo.append(nova)
        g.salvar_tarefas(tarefas_exemplo)
        recarregadas = g.carregar_tarefas()
        assert len(recarregadas) == 5
        assert recarregadas[-1]["titulo"] == "Nova tarefa salva"

    def test_salvar_preserva_campos(self, arquivo_json, tarefas_exemplo):
        g.salvar_tarefas(tarefas_exemplo)
        primeira = g.carregar_tarefas()[0]
        assert primeira["titulo"] == "Criar repositório GitHub"
        assert primeira["status"] == "Concluído"
        assert primeira["prioridade"] == "Alta"

    def test_salvar_lista_vazia(self, arquivo_json):
        g.salvar_tarefas([])
        assert g.carregar_tarefas() == []


# ══════════════════════════════════════════════════════════
#  BLOCO 3 — Validação de campos (integridade dos dados)
# ══════════════════════════════════════════════════════════

class TestValidacaoCampos:
    def test_titulos_nao_vazios(self, tarefas_exemplo):
        for t in tarefas_exemplo:
            assert t["titulo"].strip() != "", f"Título vazio no ID {t['id']}"

    def test_status_validos(self, tarefas_exemplo):
        validos = set(g.STATUS.values())
        for t in tarefas_exemplo:
            assert t["status"] in validos

    def test_prioridades_validas(self, tarefas_exemplo):
        validos = set(g.PRIORIDADE.values())
        for t in tarefas_exemplo:
            assert t["prioridade"] in validos

    def test_ids_unicos(self, tarefas_exemplo):
        ids = [t["id"] for t in tarefas_exemplo]
        assert len(ids) == len(set(ids))

    def test_ids_positivos(self, tarefas_exemplo):
        for t in tarefas_exemplo:
            assert t["id"] > 0

    def test_campos_obrigatorios_presentes(self, tarefas_exemplo):
        obrigatorios = {"id", "titulo", "descricao", "status",
                        "prioridade", "criada_em", "concluida_em"}
        for t in tarefas_exemplo:
            assert obrigatorios.issubset(t.keys())


# ══════════════════════════════════════════════════════════
#  BLOCO 4 — Lógica de negócio (Kanban / datas)
# ══════════════════════════════════════════════════════════

class TestLogicaNegocio:
    def test_tarefa_concluida_tem_data(self, tarefas_exemplo):
        for t in tarefas_exemplo:
            if t["status"] == "Concluído":
                assert t["concluida_em"] is not None

    def test_tarefa_nao_concluida_sem_data(self, tarefas_exemplo):
        for t in tarefas_exemplo:
            if t["status"] != "Concluído":
                assert t["concluida_em"] is None

    def test_contagem_por_status(self, tarefas_exemplo):
        a_fazer = sum(1 for t in tarefas_exemplo if t["status"] == "A Fazer")
        em_prog  = sum(1 for t in tarefas_exemplo if t["status"] == "Em Progresso")
        concl    = sum(1 for t in tarefas_exemplo if t["status"] == "Concluído")
        assert a_fazer == 2
        assert em_prog == 1
        assert concl == 1

    def test_taxa_conclusao_25_porcento(self, tarefas_exemplo):
        total = len(tarefas_exemplo)
        concl = sum(1 for t in tarefas_exemplo if t["status"] == "Concluído")
        assert round((concl / total) * 100) == 25

    def test_taxa_conclusao_100_porcento(self):
        todas = [{"id": i, "status": "Concluído", "concluida_em": "19/05/2025"}
                 for i in range(1, 5)]
        concl = sum(1 for t in todas if t["status"] == "Concluído")
        assert round((concl / len(todas)) * 100) == 100

    def test_taxa_conclusao_zero_porcento(self, tarefas_exemplo):
        nenhuma = [dict(t, status="A Fazer", concluida_em=None)
                   for t in tarefas_exemplo]
        assert sum(1 for t in nenhuma if t["status"] == "Concluído") == 0

    def test_contagem_por_prioridade(self, tarefas_exemplo):
        alta  = sum(1 for t in tarefas_exemplo if t["prioridade"] == "Alta")
        media = sum(1 for t in tarefas_exemplo if t["prioridade"] == "Média")
        baixa = sum(1 for t in tarefas_exemplo if t["prioridade"] == "Baixa")
        assert alta == 2
        assert media == 1
        assert baixa == 1


# ══════════════════════════════════════════════════════════
#  BLOCO 5 — Busca e filtragem
# ══════════════════════════════════════════════════════════

class TestBusca:
    def test_busca_por_id_existente(self, tarefas_exemplo):
        resultado = next((t for t in tarefas_exemplo if t["id"] == 2), None)
        assert resultado is not None
        assert resultado["titulo"] == "Configurar GitHub Actions"

    def test_busca_por_id_inexistente(self, tarefas_exemplo):
        assert next((t for t in tarefas_exemplo if t["id"] == 999), None) is None

    def test_filtrar_por_status_a_fazer(self, tarefas_exemplo):
        assert len([t for t in tarefas_exemplo if t["status"] == "A Fazer"]) == 2

    def test_filtrar_por_prioridade_alta(self, tarefas_exemplo):
        assert len([t for t in tarefas_exemplo if t["prioridade"] == "Alta"]) == 2

    def test_filtrar_status_inexistente_retorna_vazio(self, tarefas_exemplo):
        assert [t for t in tarefas_exemplo if t["status"] == "Cancelado"] == []


# ══════════════════════════════════════════════════════════
#  BLOCO 6 — Constantes do módulo
# ══════════════════════════════════════════════════════════

class TestConstantes:
    def test_status_tem_tres_opcoes(self):
        assert len(g.STATUS) == 3

    def test_status_contem_colunas_kanban(self):
        valores = set(g.STATUS.values())
        assert {"A Fazer", "Em Progresso", "Concluído"}.issubset(valores)

    def test_prioridade_tem_tres_opcoes(self):
        assert len(g.PRIORIDADE) == 3

    def test_prioridade_contem_niveis_corretos(self):
        valores = set(g.PRIORIDADE.values())
        assert {"Baixa", "Média", "Alta"}.issubset(valores)

    def test_chaves_status_sao_numericas(self):
        for chave in g.STATUS:
            assert chave.isdigit()

    def test_chaves_prioridade_sao_numericas(self):
        for chave in g.PRIORIDADE:
            assert chave.isdigit()
