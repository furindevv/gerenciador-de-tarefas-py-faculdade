"""
=============================================================
 TechFlow Solutions — Sistema de Gerenciamento de Tarefas
 Disciplina: Engenharia de Software
 Metodologia: Kanban (colunas: A Fazer, Em Progresso, Concluído)
=============================================================
"""

import json
import os
import sys
from datetime import datetime

# ─── Configuração do arquivo de dados ─────────────────────
ARQUIVO_DADOS = "tarefas.json"

# ─── Cores ANSI para o terminal ───────────────────────────
class Cor:
    RESET   = "\033[0m"
    NEGRITO = "\033[1m"
    VERDE   = "\033[92m"
    AMARELO = "\033[93m"
    AZUL    = "\033[94m"
    CIANO   = "\033[96m"
    VERMELHO= "\033[91m"
    CINZA   = "\033[90m"
    BRANCO  = "\033[97m"
    ROXO    = "\033[95m"

# ─── Status possíveis (Kanban) ────────────────────────────
STATUS = {
    "1": "A Fazer",
    "2": "Em Progresso",
    "3": "Concluído"
}

PRIORIDADE = {
    "1": "Baixa",
    "2": "Média",
    "3": "Alta"
}


# ══════════════════════════════════════════════════════════
#  FUNÇÕES DE PERSISTÊNCIA (leitura/escrita em JSON)
# ══════════════════════════════════════════════════════════

def carregar_tarefas():
    """Carrega as tarefas salvas no arquivo JSON."""
    if not os.path.exists(ARQUIVO_DADOS):
        return []
    with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_tarefas(tarefas):
    """Salva a lista de tarefas no arquivo JSON."""
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, ensure_ascii=False, indent=2)


def gerar_id(tarefas):
    """Gera um ID único incrementando o maior ID existente."""
    if not tarefas:
        return 1
    return max(t["id"] for t in tarefas) + 1


# ══════════════════════════════════════════════════════════
#  FUNÇÕES DE EXIBIÇÃO (interface do terminal)
# ══════════════════════════════════════════════════════════

def limpar_tela():
    """Limpa o terminal (funciona em Windows e Linux/Mac)."""
    os.system("cls" if os.name == "nt" else "clear")


def cabecalho():
    """Exibe o cabeçalho do sistema."""
    print(f"{Cor.CIANO}{Cor.NEGRITO}")
    print("╔══════════════════════════════════════════════════════╗")
    print("║      TechFlow Solutions — Gerenciador de Tarefas     ║")
    print("║          Metodologia Ágil: Kanban                    ║")
    print("╚══════════════════════════════════════════════════════╝")
    print(f"{Cor.RESET}")


def cor_status(status):
    """Retorna a cor ANSI correspondente ao status da tarefa."""
    cores = {
        "A Fazer":      Cor.AMARELO,
        "Em Progresso": Cor.AZUL,
        "Concluído":    Cor.VERDE,
    }
    return cores.get(status, Cor.RESET)


def cor_prioridade(prioridade):
    """Retorna a cor ANSI correspondente à prioridade."""
    cores = {
        "Baixa": Cor.CINZA,
        "Média": Cor.AMARELO,
        "Alta":  Cor.VERMELHO,
    }
    return cores.get(prioridade, Cor.RESET)


def exibir_tarefa(tarefa, resumido=False):
    """Exibe os dados de uma tarefa formatados."""
    cs = cor_status(tarefa["status"])
    cp = cor_prioridade(tarefa["prioridade"])

    if resumido:
        print(
            f"  {Cor.CINZA}[{tarefa['id']:02d}]{Cor.RESET} "
            f"{Cor.NEGRITO}{tarefa['titulo']:<30}{Cor.RESET} "
            f"{cs}■ {tarefa['status']:<15}{Cor.RESET} "
            f"{cp}▲ {tarefa['prioridade']}{Cor.RESET}"
        )
    else:
        print(f"  {Cor.CINZA}{'─'*52}{Cor.RESET}")
        print(f"  {Cor.NEGRITO}ID       :{Cor.RESET} {tarefa['id']}")
        print(f"  {Cor.NEGRITO}Título   :{Cor.RESET} {tarefa['titulo']}")
        print(f"  {Cor.NEGRITO}Descrição:{Cor.RESET} {tarefa['descricao'] or '—'}")
        print(f"  {Cor.NEGRITO}Status   :{Cor.RESET} {cs}{tarefa['status']}{Cor.RESET}")
        print(f"  {Cor.NEGRITO}Prioridade:{Cor.RESET} {cp}{tarefa['prioridade']}{Cor.RESET}")
        print(f"  {Cor.NEGRITO}Criada em:{Cor.RESET} {tarefa['criada_em']}")
        if tarefa.get("concluida_em"):
            print(f"  {Cor.NEGRITO}Concluída:{Cor.RESET} {tarefa['concluida_em']}")


def pausar():
    """Aguarda o usuário pressionar Enter."""
    print(f"\n{Cor.CINZA}Pressione Enter para continuar...{Cor.RESET}", end="")
    input()


# ══════════════════════════════════════════════════════════
#  OPERAÇÕES CRUD
# ══════════════════════════════════════════════════════════

def criar_tarefa():
    """(C) Cria uma nova tarefa e salva no JSON."""
    limpar_tela()
    cabecalho()
    print(f"{Cor.VERDE}{Cor.NEGRITO}  ── Nova Tarefa ──{Cor.RESET}\n")

    tarefas = carregar_tarefas()

    titulo = input("  Título da tarefa: ").strip()
    if not titulo:
        print(f"\n{Cor.VERMELHO}  Título não pode ser vazio.{Cor.RESET}")
        pausar()
        return

    descricao = input("  Descrição (opcional): ").strip()

    print("\n  Prioridade:")
    for k, v in PRIORIDADE.items():
        cp = cor_prioridade(v)
        print(f"    {k}. {cp}{v}{Cor.RESET}")
    escolha_p = input("  Escolha [1-3]: ").strip()
    prioridade = PRIORIDADE.get(escolha_p, "Média")

    print("\n  Status inicial:")
    for k, v in STATUS.items():
        cs = cor_status(v)
        print(f"    {k}. {cs}{v}{Cor.RESET}")
    escolha_s = input("  Escolha [1-3]: ").strip()
    status = STATUS.get(escolha_s, "A Fazer")

    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    nova = {
        "id":          gerar_id(tarefas),
        "titulo":      titulo,
        "descricao":   descricao,
        "status":      status,
        "prioridade":  prioridade,
        "criada_em":   agora,
        "concluida_em": agora if status == "Concluído" else None
    }

    tarefas.append(nova)
    salvar_tarefas(tarefas)

    print(f"\n{Cor.VERDE}  ✔ Tarefa '{titulo}' criada com ID {nova['id']}!{Cor.RESET}")
    pausar()


def listar_tarefas():
    """(R) Lista todas as tarefas agrupadas por coluna Kanban."""
    limpar_tela()
    cabecalho()
    print(f"{Cor.AZUL}{Cor.NEGRITO}  ── Quadro Kanban ──{Cor.RESET}\n")

    tarefas = carregar_tarefas()

    if not tarefas:
        print(f"  {Cor.CINZA}Nenhuma tarefa cadastrada ainda.{Cor.RESET}")
        pausar()
        return

    # Agrupa por status (colunas do Kanban)
    for s in STATUS.values():
        cs = cor_status(s)
        grupo = [t for t in tarefas if t["status"] == s]
        print(f"  {cs}{Cor.NEGRITO}{'█'} {s} ({len(grupo)}){Cor.RESET}")
        if grupo:
            for t in grupo:
                exibir_tarefa(t, resumido=True)
        else:
            print(f"  {Cor.CINZA}    (vazio){Cor.RESET}")
        print()

    pausar()


def ver_tarefa():
    """(R) Exibe os detalhes completos de uma tarefa pelo ID."""
    limpar_tela()
    cabecalho()
    print(f"{Cor.CIANO}{Cor.NEGRITO}  ── Detalhes da Tarefa ──{Cor.RESET}\n")

    tarefas = carregar_tarefas()
    if not tarefas:
        print(f"  {Cor.CINZA}Nenhuma tarefa cadastrada.{Cor.RESET}")
        pausar()
        return

    try:
        id_busca = int(input("  ID da tarefa: ").strip())
    except ValueError:
        print(f"\n{Cor.VERMELHO}  ID inválido.{Cor.RESET}")
        pausar()
        return

    tarefa = next((t for t in tarefas if t["id"] == id_busca), None)
    if not tarefa:
        print(f"\n{Cor.VERMELHO}  Tarefa com ID {id_busca} não encontrada.{Cor.RESET}")
    else:
        exibir_tarefa(tarefa)

    pausar()


def atualizar_tarefa():
    """(U) Atualiza os dados de uma tarefa existente."""
    limpar_tela()
    cabecalho()
    print(f"{Cor.AMARELO}{Cor.NEGRITO}  ── Atualizar Tarefa ──{Cor.RESET}\n")

    tarefas = carregar_tarefas()
    if not tarefas:
        print(f"  {Cor.CINZA}Nenhuma tarefa cadastrada.{Cor.RESET}")
        pausar()
        return

    # Mostra resumo para facilitar a escolha
    for t in tarefas:
        exibir_tarefa(t, resumido=True)
    print()

    try:
        id_busca = int(input("  ID da tarefa a atualizar: ").strip())
    except ValueError:
        print(f"\n{Cor.VERMELHO}  ID inválido.{Cor.RESET}")
        pausar()
        return

    tarefa = next((t for t in tarefas if t["id"] == id_busca), None)
    if not tarefa:
        print(f"\n{Cor.VERMELHO}  Tarefa não encontrada.{Cor.RESET}")
        pausar()
        return

    print(f"\n  {Cor.CINZA}(deixe em branco para manter o valor atual){Cor.RESET}\n")

    # Título
    novo_titulo = input(f"  Título [{tarefa['titulo']}]: ").strip()
    if novo_titulo:
        tarefa["titulo"] = novo_titulo

    # Descrição
    nova_desc = input(f"  Descrição [{tarefa['descricao'] or '—'}]: ").strip()
    if nova_desc:
        tarefa["descricao"] = nova_desc

    # Prioridade
    print("\n  Prioridade:")
    for k, v in PRIORIDADE.items():
        cp = cor_prioridade(v)
        print(f"    {k}. {cp}{v}{Cor.RESET}")
    escolha_p = input(f"  Escolha [atual: {tarefa['prioridade']}]: ").strip()
    if escolha_p in PRIORIDADE:
        tarefa["prioridade"] = PRIORIDADE[escolha_p]

    # Status
    print("\n  Status (coluna Kanban):")
    for k, v in STATUS.items():
        cs = cor_status(v)
        print(f"    {k}. {cs}{v}{Cor.RESET}")
    escolha_s = input(f"  Escolha [atual: {tarefa['status']}]: ").strip()
    if escolha_s in STATUS:
        novo_status = STATUS[escolha_s]
        # Registra data de conclusão ao mover para "Concluído"
        if novo_status == "Concluído" and tarefa["status"] != "Concluído":
            tarefa["concluida_em"] = datetime.now().strftime("%d/%m/%Y %H:%M")
        elif novo_status != "Concluído":
            tarefa["concluida_em"] = None
        tarefa["status"] = novo_status

    salvar_tarefas(tarefas)
    print(f"\n{Cor.VERDE}  ✔ Tarefa atualizada com sucesso!{Cor.RESET}")
    pausar()


def deletar_tarefa():
    """(D) Remove uma tarefa pelo ID."""
    limpar_tela()
    cabecalho()
    print(f"{Cor.VERMELHO}{Cor.NEGRITO}  ── Excluir Tarefa ──{Cor.RESET}\n")

    tarefas = carregar_tarefas()
    if not tarefas:
        print(f"  {Cor.CINZA}Nenhuma tarefa cadastrada.{Cor.RESET}")
        pausar()
        return

    for t in tarefas:
        exibir_tarefa(t, resumido=True)
    print()

    try:
        id_busca = int(input("  ID da tarefa a excluir: ").strip())
    except ValueError:
        print(f"\n{Cor.VERMELHO}  ID inválido.{Cor.RESET}")
        pausar()
        return

    tarefa = next((t for t in tarefas if t["id"] == id_busca), None)
    if not tarefa:
        print(f"\n{Cor.VERMELHO}  Tarefa não encontrada.{Cor.RESET}")
        pausar()
        return

    confirmacao = input(
        f"\n  Excluir '{tarefa['titulo']}'? {Cor.VERMELHO}(s/N){Cor.RESET}: "
    ).strip().lower()

    if confirmacao == "s":
        tarefas.remove(tarefa)
        salvar_tarefas(tarefas)
        print(f"\n{Cor.VERDE}  ✔ Tarefa excluída.{Cor.RESET}")
    else:
        print(f"\n{Cor.CINZA}  Operação cancelada.{Cor.RESET}")

    pausar()


def relatorio_desempenho():
    """Gera um relatório de desempenho da equipe/projeto."""
    limpar_tela()
    cabecalho()
    print(f"{Cor.ROXO}{Cor.NEGRITO}  ── Relatório de Desempenho ──{Cor.RESET}\n")

    tarefas = carregar_tarefas()
    total = len(tarefas)

    if total == 0:
        print(f"  {Cor.CINZA}Sem dados para gerar relatório.{Cor.RESET}")
        pausar()
        return

    # Contagem por status
    por_status = {s: 0 for s in STATUS.values()}
    por_prioridade = {p: 0 for p in PRIORIDADE.values()}
    for t in tarefas:
        por_status[t["status"]] += 1
        por_prioridade[t["prioridade"]] += 1

    concluidas = por_status["Concluído"]
    pct = round((concluidas / total) * 100) if total else 0

    print(f"  {Cor.NEGRITO}Total de tarefas:{Cor.RESET} {total}")
    print(f"  {Cor.NEGRITO}Taxa de conclusão:{Cor.RESET} {Cor.VERDE}{pct}%{Cor.RESET}\n")

    # Barra de progresso
    barra = int(pct / 5)
    print(f"  Progresso: [{Cor.VERDE}{'█' * barra}{Cor.CINZA}{'░' * (20 - barra)}{Cor.RESET}] {pct}%\n")

    # Por status
    print(f"  {Cor.NEGRITO}Por coluna Kanban:{Cor.RESET}")
    for s, qtd in por_status.items():
        cs = cor_status(s)
        pct_s = round((qtd / total) * 100) if total else 0
        print(f"    {cs}{s:<15}{Cor.RESET} {qtd:>3} tarefa(s)  ({pct_s}%)")

    # Por prioridade
    print(f"\n  {Cor.NEGRITO}Por prioridade:{Cor.RESET}")
    for p, qtd in por_prioridade.items():
        cp = cor_prioridade(p)
        print(f"    {cp}{p:<8}{Cor.RESET} {qtd:>3} tarefa(s)")

    pausar()


# ══════════════════════════════════════════════════════════
#  MENU PRINCIPAL
# ══════════════════════════════════════════════════════════

def menu():
    """Exibe o menu principal e processa a escolha do usuário."""
    while True:
        limpar_tela()
        cabecalho()

        print(f"  {Cor.NEGRITO}MENU PRINCIPAL{Cor.RESET}\n")
        print(f"  {Cor.VERDE}1.{Cor.RESET} Criar nova tarefa")
        print(f"  {Cor.AZUL}2.{Cor.RESET} Listar tarefas (Quadro Kanban)")
        print(f"  {Cor.CIANO}3.{Cor.RESET} Ver detalhes de uma tarefa")
        print(f"  {Cor.AMARELO}4.{Cor.RESET} Atualizar tarefa")
        print(f"  {Cor.VERMELHO}5.{Cor.RESET} Excluir tarefa")
        print(f"  {Cor.ROXO}6.{Cor.RESET} Relatório de desempenho")
        print(f"  {Cor.CINZA}0.{Cor.RESET} Sair\n")

        escolha = input("  Escolha uma opção: ").strip()

        acoes = {
            "1": criar_tarefa,
            "2": listar_tarefas,
            "3": ver_tarefa,
            "4": atualizar_tarefa,
            "5": deletar_tarefa,
            "6": relatorio_desempenho,
        }

        if escolha == "0":
            limpar_tela()
            print(f"\n{Cor.CIANO}  Até logo! — TechFlow Solutions{Cor.RESET}\n")
            sys.exit(0)
        elif escolha in acoes:
            acoes[escolha]()
        else:
            print(f"\n{Cor.VERMELHO}  Opção inválida.{Cor.RESET}")
            pausar()


# ══════════════════════════════════════════════════════════
#  PONTO DE ENTRADA
# ══════════════════════════════════════════════════════════

if __name__ == "__main__":
    menu()
