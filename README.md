# gerenciador-de-tarefas-py-faculdade
# 📌 TechFlow Solutions — Sistema de Gerenciamento de Tarefas

## 📖 Sobre o Projeto

Este projeto foi desenvolvido como atividade prática da disciplina de Engenharia de Software, com o objetivo de simular o desenvolvimento de um sistema de gerenciamento de tarefas baseado em metodologias ágeis.

A proposta consiste na criação de um sistema capaz de organizar tarefas utilizando o modelo Kanban, permitindo o acompanhamento do fluxo de trabalho, priorização de atividades e monitoramento do progresso do projeto.

O sistema foi desenvolvido em Python e possui uma interface interativa via terminal, permitindo ao usuário gerenciar tarefas de forma simples e organizada.

---

## 🎯 Objetivo do Sistema

O sistema tem como objetivo:

- Criar tarefas;
- Visualizar tarefas organizadas em um quadro Kanban;
- Atualizar informações das tarefas;
- Excluir tarefas;
- Monitorar desempenho do projeto;
- Persistir dados em arquivo JSON.

---

## 🧠 Metodologia Ágil Utilizada

Foi utilizada a metodologia **Kanban**, uma abordagem ágil voltada para gestão visual do fluxo de trabalho.

As tarefas são organizadas em três colunas principais:

- **A Fazer** → tarefas pendentes;
- **Em Progresso** → tarefas em desenvolvimento;
- **Concluído** → tarefas finalizadas.

Essa organização permite maior controle do andamento do projeto e melhor visualização das prioridades.

---

## ⚙️ Funcionalidades do Sistema

### ✅ CRUD de Tarefas

O sistema implementa as operações básicas de gerenciamento:

### Create (Criar)
Permite cadastrar uma nova tarefa com:

- título;
- descrição;
- prioridade;
- status.

### Read (Leitura)
Permite:

- listar tarefas em formato Kanban;
- visualizar detalhes completos de uma tarefa.

### Update (Atualizar)
Permite alterar:

- título;
- descrição;
- prioridade;
- status.

### Delete (Excluir)
Permite remover tarefas do sistema.

### 📊 Relatório de Desempenho
O sistema gera um relatório contendo:

- total de tarefas;
- taxa de conclusão;
- progresso do projeto;
- distribuição por status;
- distribuição por prioridade.

---

## 🛠️ Tecnologias Utilizadas

- Python 3
- JSON (persistência de dados)
- Git
- GitHub
- GitHub Projects (Kanban)
- GitHub Actions (Integração Contínua)

---

## 📂 Estrutura do Projeto

```txt
projeto/
│── gerenciador_tarefas.py
│── tarefas.json
│── README.md
│── tests/
│    └── test_gerenciador.py
│── .github/
│    └── workflows/
│         └── ci.yml
```

---

## ▶️ Como Executar o Projeto

### 1. Clonar o repositório

Abra o terminal e execute:

```bash
git clone https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git
```

Entre na pasta do projeto:

```bash
cd NOME-DO-REPOSITORIO
```

---

### 2. Executar o sistema

Certifique-se de possuir o Python instalado.

Verifique a versão:

```bash
python --version
```

Depois execute:

```bash
python gerenciador_tarefas.py
```

O sistema iniciará no terminal com um menu interativo.

---

## 💾 Persistência de Dados

As tarefas são armazenadas no arquivo:

```txt
tarefas.json
```

Isso permite que os dados permaneçam salvos mesmo após fechar o sistema.

---

## 🔄 Controle de Qualidade

O projeto utiliza testes automatizados e integração contínua através do **GitHub Actions**.

Os testes são executados automaticamente a cada alteração enviada ao repositório, garantindo maior confiabilidade do software.

Benefícios:

- validação automática do código;
- redução de erros;
- melhoria da qualidade do sistema;
- maior segurança na evolução do projeto.

---

## 🔀 Gestão de Mudanças (Mudança de Escopo)

Durante o desenvolvimento do sistema foi realizada uma mudança de escopo.

Inicialmente, o projeto previa apenas um CRUD simples de tarefas.

Posteriormente, foi adicionada a funcionalidade de **Relatório de Desempenho**, permitindo acompanhar métricas do projeto como:

- taxa de conclusão;
- progresso do Kanban;
- quantidade de tarefas por prioridade;
- desempenho geral.

Essa alteração foi implementada para melhorar o acompanhamento do fluxo de trabalho e atender melhor às necessidades da empresa fictícia **TechFlow Solutions**.

---

## 🚀 Como Subir o Projeto no GitHub

### 1. Criar repositório no GitHub

Acesse o GitHub e clique em:

```txt
New Repository
```

Defina:

- Nome do repositório;
- Público (Public);
- Clique em **Create Repository**.

---

### 2. Abrir terminal no VS Code

Dentro da pasta do projeto execute:

```bash
git init
```

---

### 3. Adicionar os arquivos

```bash
git add .
```

---

### 4. Criar o primeiro commit

```bash
git commit -m "feat: criação inicial do sistema de gerenciamento de tarefas"
```

---

### 5. Conectar ao repositório do GitHub

Substitua o link abaixo pelo do seu repositório:

```bash
git remote add origin https://github.com/SEU-USUARIO/NOME-REPOSITORIO.git
```

---

### 6. Enviar para o GitHub

```bash
git branch -M main
git push -u origin main
```

---

## 📝 Sugestão de Commits Semânticos

Para atender ao requisito do trabalho:

```txt
feat: criação da estrutura inicial do projeto
feat: implementação do menu principal
feat: criação da função de cadastro de tarefas
feat: implementação da listagem Kanban
feat: criação da atualização de tarefas
feat: implementação da exclusão de tarefas
feat: adição do relatório de desempenho
test: criação dos testes automatizados
ci: configuração do GitHub Actions
docs: atualização do README
```

---

## 👨‍💻 Autor

**Augusto Furin da Conceição**  
Disciplina: ciencias da computação
Projeto acadêmico desenvolvido para aplicação prática de conceitos de tecnologia, GitHub, Kanban e metodologias ágeis.
