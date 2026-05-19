"""
=============================================================
 TechFlow Solutions — Testes Unitários (pytest)
 Valida as funções principais do gerenciador de tarefas.
 Execute com:  pytest test_gerenciador.py -v
=============================================================
"""

import json
import os
import pytest
import tempfile

# ─── Importa o módulo principal ───────────────────────────
import gerenciador_tarefas as g


# ══════════════════════════════════════════════════════════
#  FIXTURES — dados de teste isolados
# ══════════════════════════════════════════════════════════

@pytest.fixture
def tarefas_exemplo():
    """Retorna uma lista de tarefas para uso nos testes."""
    return [
        {
            "id": 1,
            "titulo": "Criar repositório",
            "descricao": "Repo público no GitHub",
            "status": "Concluído",
            "prioridade": "Alta",
            "criada_em": "19/05/2025 10:00",
            "concluida_em": "19/05/2025 11:00"
        },
        {
            "id": 2,
            "titulo": "Configurar CI",
            "descricao": "GitHub Actions com pytest",
            "status": "Em Progresso",
            "prioridade": "Alta",
            "criada_em": "19/05/2025 11:00",
            "concluida_em": None
        },
        {
            "id": 3,
            "titulo": "Escrever testes",
            "descricao": "Cobertura das funções CRUD",
            "status": "A Fazer",
            "prioridade": "Média",
            "criada_em": "19/05/2025 12:00",
            "concluida_em": None
        }
    ]


@pytest.fixture
def arquivo_temporario(tmp_path, monkeypatch, tarefas_exemplo):
    """
    Cria um arquivo JSON temporário e redireciona o módulo
    para usá-lo, garantindo isolamento entre os testes.
    """
    arquivo = tmp_path / "tarefas_teste.json"
    arquivo.write_text(
        json.dumps(tarefas_exemplo, ensure_ascii=False),
        encoding="utf-8"
    )
    monkeypatch.setattr(g, "ARQUIVO_DADOS", str(arquivo))
    return str(arquivo)


# ══════════════════════════════════════════════════════════
#  TESTES: gerar_id
# ══════════════════════════════════════════════════════════

def test_gerar_id_lista_vazia():
    """Deve retornar 1 quando não há tarefas."""
    assert g.gerar_id([]) == 1


def test_gerar_id_incrementa(tarefas_exemplo):
    """Deve retornar o maior ID + 1."""
    assert g.gerar_id(tarefas_exemplo) == 4


def test_gerar_id_com_uma_tarefa():
    """Deve retornar 2 para lista com um único elemento."""
    tarefas = [{"id": 1, "titulo": "x"}]
    assert g.gerar_id(tarefas) == 2


# ══════════════════════════════════════════════════════════
#  TESTES: carregar_tarefas / salvar_tarefas
# ══════════════════════════════════════════════════════════

def test_carregar_tarefas_retorna_lista(arquivo_temporario):
    """Deve carregar corretamente as tarefas do arquivo JSON."""
    tarefas = g.carregar_tarefas()
    assert isinstance(tarefas, list)
    assert len(tarefas) == 3


def test_carregar_tarefas_arquivo_inexistente(monkeypatch, tmp_path):
    """Deve retornar lista vazia se o arquivo não existir."""
    monkeypatch.setattr(g, "ARQUIVO_DADOS", str(tmp_path / "nao_existe.json"))
    assert g.carregar_tarefas() == []


def test_salvar_e_recarregar(arquivo_temporario, tarefas_exemplo):
    """Deve salvar e recuperar os dados sem perda."""
    nova_tarefa = {
        "id": 99,
        "titulo": "Tarefa salva",
        "descricao": "Teste de persistência",
        "status": "A Fazer",
        "prioridade": "Baixa",
        "criada_em": "01/01/2025 00:00",
        "concluida_em": None
    }
    tarefas_exemplo.append(nova_tarefa)
    g.salvar_tarefas(tarefas_exemplo)

    recarregadas = g.carregar_tarefas()
    assert len(recarregadas) == 4
    assert recarregadas[-1]["titulo"] == "Tarefa salva"


# ══════════════════════════════════════════════════════════
#  TESTES: validação de campos obrigatórios
# ══════════════════════════════════════════════════════════

def test_titulo_nao_vazio(tarefas_exemplo):
    """Toda tarefa deve ter um título não vazio."""
    for t in tarefas_exemplo:
        assert t["titulo"].strip() != ""


def test_status_valido(tarefas_exemplo):
    """O status de cada tarefa deve ser um dos valores permitidos."""
    valores_validos = set(g.STATUS.values())
    for t in tarefas_exemplo:
        assert t["status"] in valores_validos, (
            f"Status inválido: '{t['status']}'"
        )


def test_prioridade_valida(tarefas_exemplo):
    """A prioridade deve ser um dos valores permitidos."""
    valores_validos = set(g.PRIORIDADE.values())
    for t in tarefas_exemplo:
        assert t["prioridade"] in valores_validos, (
            f"Prioridade inválida: '{t['prioridade']}'"
        )


def test_id_unico(tarefas_exemplo):
    """Todos os IDs da lista devem ser únicos."""
    ids = [t["id"] for t in tarefas_exemplo]
    assert len(ids) == len(set(ids)), "Há IDs duplicados na lista"


# ══════════════════════════════════════════════════════════
#  TESTES: lógica de negócio
# ══════════════════════════════════════════════════════════

def test_contagem_por_status(tarefas_exemplo):
    """Deve contar corretamente as tarefas por status."""
    concluidas = sum(1 for t in tarefas_exemplo if t["status"] == "Concluído")
    em_progresso = sum(1 for t in tarefas_exemplo if t["status"] == "Em Progresso")
    a_fazer = sum(1 for t in tarefas_exemplo if t["status"] == "A Fazer")

    assert concluidas == 1
    assert em_progresso == 1
    assert a_fazer == 1


def test_taxa_conclusao(tarefas_exemplo):
    """Taxa de conclusão deve ser calculada corretamente."""
    total = len(tarefas_exemplo)
    concluidas = sum(1 for t in tarefas_exemplo if t["status"] == "Concluído")
    taxa = round((concluidas / total) * 100)
    assert taxa == 33


def test_tarefa_concluida_tem_data(tarefas_exemplo):
    """Toda tarefa com status 'Concluído' deve ter data de conclusão."""
    for t in tarefas_exemplo:
        if t["status"] == "Concluído":
            assert t["concluida_em"] is not None, (
                f"Tarefa ID {t['id']} concluída sem data de conclusão"
            )


def test_tarefa_nao_concluida_sem_data(tarefas_exemplo):
    """Tarefas não concluídas não devem ter data de conclusão."""
    for t in tarefas_exemplo:
        if t["status"] != "Concluído":
            assert t["concluida_em"] is None, (
                f"Tarefa ID {t['id']} não concluída mas tem data de conclusão"
            )


def test_busca_por_id(tarefas_exemplo):
    """Deve encontrar tarefa pelo ID corretamente."""
    resultado = next((t for t in tarefas_exemplo if t["id"] == 2), None)
    assert resultado is not None
    assert resultado["titulo"] == "Configurar CI"


def test_busca_id_inexistente(tarefas_exemplo):
    """Deve retornar None para ID que não existe."""
    resultado = next((t for t in tarefas_exemplo if t["id"] == 999), None)
    assert resultado is None
