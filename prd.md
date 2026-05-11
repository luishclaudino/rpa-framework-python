# 📋 PRD — RPA Framework Coop (rpa_3003)

**Versão:** 1.0.0  
**Data:** 2026-05-10  
**Status:** Draft

---

## 1. Visão Geral

### 1.1 Objetivo

Criar um **Framework Python modular e extensível** para automação RPA com suporte a múltiplos navegadores e engines de automação web (Selenium e Playwright).

### 1.2 Público-Alvo

| Persona | Descrição | Necessidade Principal |
|---------|-----------|----------------------|
| **Dev RPA Júnior** | Pouca experiência com automação, conhece Python básico | Templates prontos e estrutura clara para seguir |
| **Dev RPA Sênior** | Experiente, mantém múltiplos projetos simultâneos | Padronização, extensibilidade e troca de engine sem retrabalho |
| **Tech Lead** | Responsável pela qualidade e manutenibilidade | Logs centralizados, separação dev/prd e testes automatizados |

### 1.3 Problema

Equipes de automação que trabalham com RPA enfrentam desafios recorrentes:

- **Falta de padronização** entre projetos — cada bot tem sua própria estrutura, convenções e dependências.
- **Acoplamento de engine** — mudar de Selenium para Playwright exige reescrever o código de automação.
- **Logs inconsistentes** — dificulta o monitoramento, auditoria e debugging em produção.
- **Ausência de separação de ambientes** — código de desenvolvimento/testes misturado com workflows de produção.
- **Onboarding lento** — novos membros perdem tempo recriando boilerplate ao iniciar projetos.

### 1.4 Solução

Um framework Python unificado que resolve esses problemas com:

- **Estrutura padronizada**: Templates pré-definidos para organização automática de projetos.
- **API unificada com dual-engine**: Mesmos métodos para Selenium e Playwright — basta trocar a engine na configuração.
- **Sistema de logging corporativo**: Logs auditáveis com formato consistente, rotação automática e integração ao Splunk.
- **Separação clara de ambientes**: Diretórios distintos para `dev` e `prd` com configuração isolada.
- **Utilitários compartilhados**: Funções prontas para manipulação de arquivos, JSON, CSV, masking de dados e integrações diversas.
- **CLI integrada**: Comandos para criação de projetos, execução de bots, gerenciamento de logs e configuração.
- **Versionamento e controle**: Estrutura que facilita o versionamento e gerenciamento de dependências.

O framework elimina o retrabalho, garante consistência entre projetos, acelera o onboarding e fornece a rastreabilidade necessária para automações em produção.

---

## 2. Requisitos Funcionais

### 2.1 Estrutura do Framework

```
coop-framework/
├── rpa_3003/                   # Pacote principal
│   ├── __init__.py
│   ├── cli.py                  # Interface de linha de comando
│   ├── core/
│   │   ├── __init__.py
│   │   ├── logger.py           # Sistema de logging centralizado
│   │   ├── config.py           # Gerenciamento de configurações
│   │   └── exceptions.py       # Exceções customizadas
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── file_utils.py
│   │   ├── json_utils.py
│   │   └── csv_utils.py
│   ├── bots/
│   │   ├── __init__.py
│   │   ├── base.py             # Classe base abstrata
│   │   ├── selenium/
│   │   │   ├── __init__.py
│   │   │   ├── browser.py
│   │   │   └── actions.py
│   │   └── playwright/
│   │       ├── __init__.py
│   │       ├── browser.py
│   │       └── actions.py
│   └── templates/
│       ├── __init__.py
│       ├── default/
│       │   ├── main.py.tpl
│       │   ├── global_vars.py.tpl
│       │   └── step_01_initialize.py.tpl
│       └── template_manager.py
├── projects/
├── tests/
├── requirements.txt
├── setup.py
└── README.md
```

### 2.2 Estrutura de Projetos RPA

```
projects/
└── meu_projeto/
    ├── workflows/
    │   ├── __init__.py
    │   ├── dev/
    │   │   ├── __init__.py
    │   │   └── step_01_initialize.py
    │   └── prd/
    │       ├── __init__.py
    │       └── step_01_initialize.py
    ├── logs/
    ├── data/
    ├── main.py
    └── global_vars.py
```

### 2.3 Sistema de Logging

#### Formato

```
[YYYY-MM-DD HH:MM:SS] [LEVEL] [nome_script] [linha] [user] mensagem
```

| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| `YYYY-MM-DD HH:MM:SS` | Timestamp | `2026-05-10 14:30:45` |
| `LEVEL` | Nível do log | `INFO`, `WARNING`, `ERROR`, `DEBUG`, `CRITICAL` |
| `nome_script` | Arquivo `.py` em execução | `step_01_initialize.py` |
| `linha` | Linha no script | `42` |
| `user` | Usuário executando o processo | `joao.silva` |
| `mensagem` | Descrição do evento | `Navegador Chrome iniciado` |

#### Requisitos

- **RF-LOG-01**: Aceitar parâmetro `user` ao criar instância (default: `os.getlogin()` / `getpass.getuser()`)
- **RF-LOG-02**: Rotação automática por tamanho (10MB) e quantidade (5 backups)
- **RF-LOG-03**: Output simultâneo em arquivo e console
- **RF-LOG-04**: `nome_script` e `linha` extraídos automaticamente via `inspect` na stack de chamadas
- **RF-LOG-05**: Logs armazenados em `logs/` do projeto com nome `{projeto}_{YYYY-MM-DD}.log`

#### Exemplo de Saída

```
[2026-05-10 14:30:45] [INFO] [step_01_initialize.py] [23] [joao.silva] Iniciando workflow
[2026-05-10 14:30:46] [INFO] [step_01_initialize.py] [35] [joao.silva] Chrome iniciado
[2026-05-10 14:31:02] [ERROR] [step_01_initialize.py] [58] [joao.silva] Elemento não encontrado: #btn-login
```

### 2.4 Suporte Multi-Browser

| Navegador | Selenium | Playwright |
|-----------|----------|------------|
| Chrome    | ✅       | ✅ (Chromium) |
| Firefox   | ✅       | ✅         |
| Edge      | ✅       | ✅         |

#### Classe Base Abstrata (`BotBase`)

Todos os métodos abaixo são `@abstractmethod`:

- `open_browser(browser="chrome", headless=False) -> None`
- `close_browser() -> None`
- `navigate(url: str) -> None`
- `find_element(selector: str, by="css", timeout=10) -> Any`
- `click(selector: str, by="css", timeout=10) -> None`
- `type_text(selector: str, text: str, by="css", timeout=10) -> None`
- `get_text(selector: str, by="css", timeout=10) -> str`
- `wait_for_element(selector: str, by="css", timeout=10) -> Any`
- `take_screenshot(path: str) -> None`
- `execute_script(script: str) -> Any`

#### Requisitos dos Bots

- **RF-BOT-01**: Engine configurável por projeto (Selenium ou Playwright)
- **RF-BOT-02**: API consistente entre engines (mesmos métodos/parâmetros)
- **RF-BOT-03**: Modo headless para ambos
- **RF-BOT-04**: Gerenciamento automático de WebDrivers via `webdriver-manager`
- **RF-BOT-05**: Suporte a proxy e diretório de download configurável
- **RF-BOT-06**: Captura automática de screenshot em caso de erro
- **RF-BOT-07**: Timeout padrão configurável (default: 10 segundos)

### 2.5 Utilitários

#### File Utils

| Função | Descrição |
|--------|-----------|
| `create_directory(path)` | Cria diretório recursivamente |
| `delete_file(path)` | Remove arquivo |
| `copy_file(src, dst)` | Copia arquivo |
| `move_file(src, dst)` | Move arquivo |
| `list_files(directory, extension)` | Lista arquivos por extensão |
| `file_exists(path)` | Verifica existência |
| `read_file(path, encoding)` | Lê conteúdo texto |
| `write_file(path, content, encoding)` | Escreve conteúdo texto |

#### JSON Utils

| Função | Descrição |
|--------|-----------|
| `read_json(path)` | Lê arquivo JSON |
| `write_json(path, data, indent)` | Escreve arquivo JSON |
| `merge_json(file1, file2, output)` | Merge de dois JSONs |
| `json_to_dict(json_string)` | String JSON → dict |
| `dict_to_json(data)` | Dict → string JSON |
| `validate_json(path_or_string)` | Valida JSON |

#### CSV Utils

| Função | Descrição |
|--------|-----------|
| `read_csv(path, delimiter, encoding)` | Lê CSV → lista de dicts |
| `write_csv(path, data, headers, delimiter)` | Escreve CSV |
| `append_to_csv(path, row)` | Adiciona linha ao CSV |
| `filter_csv(path, column, value)` | Filtra linhas por coluna/valor |

### 2.6 Interface CLI

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `rpa3003 new <nome>` | Cria novo projeto | `rpa3003 new meu_projeto` |
| `rpa3003 run <nome> [--env]` | Executa projeto | `rpa3003 run meu_projeto --env prd` |
| `rpa3003 list` | Lista projetos | `rpa3003 list` |
| `rpa3003 info <nome>` | Info do projeto | `rpa3003 info meu_projeto` |
| `rpa3003 version` | Versão do framework | `rpa3003 version` |

**Opções de `new`:** `--engine` (selenium/playwright), `--browser` (chrome/firefox/edge), `--template` (default)

**Opções de `run`:** `--env` (dev/prd), `--headless`, `--user`

### 2.7 Templates

- **RF-TPL-01**: Template `default` cria estrutura completa de pastas e arquivos
- **RF-TPL-02**: `main.py` gerado com código funcional que importa e executa os steps
- **RF-TPL-03**: `global_vars.py` com variáveis padrão (browser, engine, headless, timeout)
- **RF-TPL-04**: `step_01_initialize.py` com código de exemplo que abre navegador
- **RF-TPL-05**: Logger configurado automaticamente para o projeto

---

## 3. Requisitos Não-Funcionais

| Categoria | Requisito |
|-----------|-----------|
| Python | >= 3.9 |
| SO | Windows 10/11 (principal), Linux (compatível) |
| Selenium | >= 4.0 |
| Playwright | >= 1.40 |
| Testes | Cobertura >= 70% |
| Código | PEP 8, docstrings, type hints obrigatórios |
| Performance | Criação de projeto < 3s, import < 1s |
| Extensibilidade | Open/Closed Principle para novos engines e templates |

---

## 4. Dependências

**Produção:**
```
selenium>=4.0.0
playwright>=1.40.0
webdriver-manager>=4.0.0
click>=8.0.0
```

**Desenvolvimento:**
```
pytest>=7.0.0
pytest-cov>=4.0.0
flake8>=6.0.0
black>=23.0.0
```

---

## 5. Ambiente de Desenvolvimento

### 5.1 Pré-requisitos

- Python >= 3.9 instalado e disponível no PATH
- Git

### 5.2 Configuração do Ambiente Virtual

```bash
# 1. Clonar o repositório
git clone <url-do-repositorio>
cd coop-framework

# 2. Criar o ambiente virtual
python -m venv venv

# 3. Ativar o ambiente virtual
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Windows (CMD)
.\venv\Scripts\activate.bat

# Linux / macOS
source venv/bin/activate

# 4. Instalar o framework em modo editável (com todas as dependências)
pip install -e .

# 5. (Playwright) Instalar os browsers necessários
playwright install
```

### 5.3 Verificação

```bash
# Confirmar versão do framework
rpa3003 version

# Rodar a suite de testes
pytest --cov=rpa_3003 tests/
```

### 5.4 Desativar o Ambiente Virtual

```bash
deactivate
```

> **Nota:** O diretório `venv/` deve ser incluído no `.gitignore` e não versionado.

---

## 6. Riscos e Mitigações

| Risco | Mitigação |
|-------|-----------|
| Incompatibilidade browser/WebDriver | `webdriver-manager` automático |
| Diferenças API Selenium/Playwright | Classe base abstrata garantindo interface consistente |
| Performance com logging excessivo | Nível de log configurável + rotação |
| Playwright requer install de browsers | Documentar + comando de setup |

---

## 7. Critérios de Aceite

- [ ] Instalável via `pip install -e .`
- [ ] CLI com todos os comandos funcionais
- [ ] Novo projeto gera estrutura completa
- [ ] Bots Selenium e Playwright abrem Chrome, Firefox e Edge
- [ ] Logger no formato especificado com script, linha e user
- [ ] Rotação de logs funcional
- [ ] Utilitários testados
- [ ] Testes >= 80% cobertura
- [ ] README completo

---

## 8. Cronograma Sugerido

| Fase | Descrição | Duração |
|------|-----------|---------|
| 1 | Core (logger, config, exceptions) + Estrutura | 2 dias |
| 2 | Utilitários (file, json, csv) | 1 dia |
| 3 | Bots (base + Selenium) | 2 dias |
| 4 | Bots (Playwright) | 1 dia |
| 5 | CLI + Templates | 2 dias |
| 6 | Testes + Documentação | 2 dias |
| **Total** | | **~10 dias** |

---

## 9. Glossário

| Termo | Definição |
|-------|-----------|
| **RPA** | Robotic Process Automation |
| **Workflow** | Sequência de passos automatizados |
| **Step** | Unidade de execução dentro de um workflow |
| **Engine** | Motor de automação web (Selenium ou Playwright) |
| **Headless** | Execução do browser sem interface gráfica |
| **WebDriver** | Driver para controle programático do navegador |
