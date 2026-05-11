# 🗺️ Plano de Implementação — RPA Framework Coop (rpa_3003)

**Versão:** 1.0.0  
**Data:** 2026-05-10  
**Referência:** [prd.md](file:///d:/Projetos/rpa-framework-coop/prd.md)

---

## Fase 1 — Estrutura Base + Core (Dias 1-2)

### 1.1 Scaffold do Projeto ✅

Criar toda a árvore de diretórios e arquivos `__init__.py`:

```
coop-framework/
├── rpa_3003/
│   ├── __init__.py          # __version__ = "1.0.0"
│   ├── core/
│   │   └── __init__.py
│   ├── utils/
│   │   └── __init__.py
│   ├── bots/
│   │   ├── __init__.py
│   │   ├── selenium/
│   │   │   └── __init__.py
│   │   └── playwright/
│   │       └── __init__.py
│   └── templates/
│       ├── __init__.py
│       └── default/
├── projects/
├── tests/
│   └── __init__.py
├── requirements.txt
└── setup.py
```

**Ações:**
- Criar `setup.py` com `entry_points` para o CLI (`rpa3003 = rpa_3003.cli:main`)
- Criar `requirements.txt` com todas as dependências
- Criar `rpa_3003/__init__.py` exportando versão e componentes principais

---

### 1.2 Core — Logger (`rpa_3003/core/logger.py`)

Componente mais crítico do framework. Implementação detalhada:

#### Classe `RPALogger`

```python
class RPALogger:
    def __init__(
        self,
        project_name: str,
        log_dir: str,
        user: str | None = None,        # default: getpass.getuser()
        level: str = "INFO",
        max_bytes: int = 100_000_000,     # 100MB
        backup_count: int = 5,
        console_output: bool = True
    ):
```

#### Formato Customizado

Criar um `logging.Formatter` customizado que sobrescreve `format()`:

```python
class RPAFormatter(logging.Formatter):
    def __init__(self, user: str):
        self.user = user
        super().__init__()

    def format(self, record: logging.LogRecord) -> str:
        # Usar inspect.stack() para obter o caller real
        # Percorrer a stack até encontrar o primeiro frame fora do logger
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        caller_file = os.path.basename(record.pathname)
        caller_line = record.lineno
        return (
            f"[{timestamp}] [{record.levelname}] "
            f"[{caller_file}] [{caller_line}] "
            f"[{self.user}] {record.getMessage()}"
        )
```

> **Nota Técnica:** Para que `record.pathname` e `record.lineno` apontem para o arquivo correto (e não para `logger.py` em si), os métodos `info()`, `debug()`, etc. do `RPALogger` devem usar `self.logger._log(level, msg, args, stacklevel=N)` com o `stacklevel` adequado para subir frames na stack até o chamador real. Alternativamente, usar `logging.Logger.findCaller()` com `stacklevel` configurado.

#### Handlers

- **RotatingFileHandler**: arquivo `{project}_{YYYY-MM-DD}.log` em `logs/`, max 100MB, 5 backups
- **StreamHandler**: console com mesmo formato

#### Métodos Públicos

```python
def debug(self, message: str) -> None
def info(self, message: str) -> None
def warning(self, message: str) -> None
def error(self, message: str) -> None
def critical(self, message: str) -> None
```

---

### 1.3 Core — Config (`rpa_3003/core/config.py`)

Classe para gerenciar configurações do framework e dos projetos:

```python
class Config:
    DEFAULT_CONFIG = {
        "engine": "selenium",
        "browser": "chrome",
        "headless": False,
        "timeout": 10,
        "log_level": "INFO",
        "log_max_bytes": 10_485_760,
        "log_backup_count": 5,
    }

    def __init__(self, config_path: str | None = None):
        # Carrega config de arquivo JSON ou usa defaults

    def get(self, key: str, default=None) -> Any: ...
    def set(self, key: str, value: Any) -> None: ...
    def save(self, path: str) -> None: ...
    def load(self, path: str) -> None: ...
```

---

### 1.4 Core — Exceptions (`rpa_3003/core/exceptions.py`)

```python
class RPAFrameworkError(Exception):
    """Exceção base do framework."""

class BrowserNotFoundError(RPAFrameworkError):
    """Navegador não encontrado ou não suportado."""

class ElementNotFoundError(RPAFrameworkError):
    """Elemento web não encontrado no timeout."""

class EngineNotSupportedError(RPAFrameworkError):
    """Engine de automação não suportado."""

class ProjectExistsError(RPAFrameworkError):
    """Projeto já existe."""

class ProjectNotFoundError(RPAFrameworkError):
    """Projeto não encontrado."""

class ConfigError(RPAFrameworkError):
    """Erro na configuração."""

class FileOperationError(RPAFrameworkError):
    """Erro em operação de arquivo."""
```

---

## Fase 2 — Utilitários (Dia 3)

### 2.1 File Utils (`rpa_3003/utils/file_utils.py`)

Implementação direta usando `os`, `shutil`, `pathlib`:

```python
def create_directory(path: str) -> str:
    """Cria diretório e pais. Retorna o path criado."""
    os.makedirs(path, exist_ok=True)
    return path

def delete_file(path: str) -> bool:
    """Remove arquivo. Retorna True se removido."""

def copy_file(src: str, dst: str) -> str:
    """Copia arquivo. Retorna path destino."""

def move_file(src: str, dst: str) -> str:
    """Move arquivo. Retorna path destino."""

def list_files(directory: str, extension: str = "*") -> list[str]:
    """Lista arquivos. Filtra por extensão se informada."""

def file_exists(path: str) -> bool:
    """Verifica se arquivo existe."""

def get_file_size(path: str) -> int:
    """Retorna tamanho em bytes."""

def read_file(path: str, encoding: str = "utf-8") -> str:
    """Lê conteúdo de arquivo texto."""

def write_file(path: str, content: str, encoding: str = "utf-8") -> None:
    """Escreve conteúdo em arquivo texto."""
```

---

### 2.2 JSON Utils (`rpa_3003/utils/json_utils.py`)

```python
def read_json(path: str, encoding: str = "utf-8") -> dict | list:
    """Lê e retorna conteúdo de arquivo JSON."""

def write_json(path: str, data: dict | list, indent: int = 4, encoding: str = "utf-8") -> None:
    """Escreve dados em arquivo JSON."""

def merge_json(file1: str, file2: str, output: str | None = None) -> dict:
    """Faz merge (deep merge) de dois arquivos JSON. Retorna resultado."""

def json_to_dict(json_string: str) -> dict | list:
    """Converte string JSON para dict/list."""

def dict_to_json(data: dict | list, indent: int = 4) -> str:
    """Converte dict/list para string JSON."""

def validate_json(path_or_string: str) -> bool:
    """Valida se é JSON válido (aceita path de arquivo ou string)."""
```

---

### 2.3 CSV Utils (`rpa_3003/utils/csv_utils.py`)

```python
def read_csv(path: str, delimiter: str = ",", encoding: str = "utf-8") -> list[dict]:
    """Lê CSV e retorna lista de dicionários (usando DictReader)."""

def write_csv(
    path: str,
    data: list[dict],
    headers: list[str] | None = None,
    delimiter: str = ",",
    encoding: str = "utf-8"
) -> None:
    """Escreve lista de dicionários em arquivo CSV."""

def append_to_csv(path: str, row: dict, encoding: str = "utf-8") -> None:
    """Adiciona uma linha ao final do CSV."""

def filter_csv(path: str, column: str, value: str) -> list[dict]:
    """Filtra linhas do CSV onde column == value."""
```

---

## Fase 3 — Bots Selenium (Dias 4-5)

### 3.1 Base Abstrata (`rpa_3003/bots/base.py`)

```python
from abc import ABC, abstractmethod
from typing import Any

class BotBase(ABC):
    """Classe base abstrata para bots de automação web."""

    def __init__(self, logger=None, config=None):
        self.logger = logger
        self.config = config
        self.driver = None  # ou page para Playwright

    @abstractmethod
    def open_browser(self, browser: str = "chrome", headless: bool = False, **kwargs) -> None:
        """Abre o navegador especificado."""

    @abstractmethod
    def close_browser(self) -> None:
        """Fecha o navegador."""

    @abstractmethod
    def navigate(self, url: str) -> None:
        """Navega para a URL."""

    @abstractmethod
    def find_element(self, selector: str, by: str = "css", timeout: int = 10) -> Any:
        """Encontra elemento na página."""

    @abstractmethod
    def click(self, selector: str, by: str = "css", timeout: int = 10) -> None:
        """Clica em um elemento."""

    @abstractmethod
    def type_text(self, selector: str, text: str, by: str = "css", timeout: int = 10) -> None:
        """Digita texto em um elemento."""

    @abstractmethod
    def get_text(self, selector: str, by: str = "css", timeout: int = 10) -> str:
        """Retorna o texto de um elemento."""

    @abstractmethod
    def wait_for_element(self, selector: str, by: str = "css", timeout: int = 10) -> Any:
        """Aguarda elemento estar presente/visível."""

    @abstractmethod
    def take_screenshot(self, path: str) -> None:
        """Captura screenshot."""

    @abstractmethod
    def execute_script(self, script: str) -> Any:
        """Executa JavaScript na página."""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type and self.logger:
            self.logger.error(f"Erro durante execução: {exc_val}")
            try:
                self.take_screenshot(f"error_{datetime.now():%Y%m%d_%H%M%S}.png")
            except Exception:
                pass
        self.close_browser()
        return False
```

---

### 3.2 Selenium Browser (`rpa_3003/bots/selenium/browser.py`)

```python
class SeleniumBot(BotBase):
    """Implementação do bot usando Selenium WebDriver."""

    BROWSER_MAP = {
        "chrome": (webdriver.Chrome, ChromeDriverManager),
        "firefox": (webdriver.Firefox, GeckoDriverManager),
        "edge": (webdriver.Edge, EdgeChromiumDriverManager),
    }

    BY_MAP = {
        "css": By.CSS_SELECTOR,
        "xpath": By.XPATH,
        "id": By.ID,
        "name": By.NAME,
        "class": By.CLASS_NAME,
        "tag": By.TAG_NAME,
        "link_text": By.LINK_TEXT,
        "partial_link_text": By.PARTIAL_LINK_TEXT,
    }

    def open_browser(self, browser="chrome", headless=False, **kwargs):
        # Usa webdriver-manager para instalar driver automaticamente
        # Configura options (headless, proxy, download_dir)
        # Cria instância do webdriver

    def close_browser(self):
        if self.driver:
            self.driver.quit()

    def navigate(self, url):
        self.driver.get(url)

    def find_element(self, selector, by="css", timeout=10):
        by_type = self.BY_MAP.get(by, By.CSS_SELECTOR)
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by_type, selector))
        )

    def click(self, selector, by="css", timeout=10):
        element = self.find_element(selector, by, timeout)
        element.click()

    def type_text(self, selector, text, by="css", timeout=10):
        element = self.find_element(selector, by, timeout)
        element.clear()
        element.send_keys(text)

    # ... demais métodos
```

### 3.3 Selenium Actions (`rpa_3003/bots/selenium/actions.py`)

Ações auxiliares comuns do Selenium:

```python
class SeleniumActions:
    """Ações avançadas para Selenium."""

    def __init__(self, bot: SeleniumBot):
        self.bot = bot

    def select_dropdown(self, selector, value, by="css") -> None:
        """Seleciona opção em dropdown."""

    def switch_to_frame(self, frame_reference) -> None:
        """Troca para iframe."""

    def switch_to_default(self) -> None:
        """Volta ao conteúdo principal."""

    def switch_to_window(self, index: int) -> None:
        """Troca para aba/janela por índice."""

    def accept_alert(self) -> str:
        """Aceita alert e retorna texto."""

    def dismiss_alert(self) -> str:
        """Dismisses alert e retorna texto."""

    def scroll_to_element(self, selector, by="css") -> None:
        """Faz scroll até elemento."""

    def hover(self, selector, by="css") -> None:
        """Move mouse sobre elemento."""

    def drag_and_drop(self, source_sel, target_sel, by="css") -> None:
        """Drag and drop entre elementos."""

    def wait_page_load(self, timeout=30) -> None:
        """Aguarda carregamento completo da página."""
```

---

## Fase 4 — Bots Playwright (Dia 6)

### 4.1 Playwright Browser (`rpa_3003/bots/playwright/browser.py`)

```python
class PlaywrightBot(BotBase):
    """Implementação do bot usando Playwright."""

    BROWSER_MAP = {
        "chrome": "chromium",
        "chromium": "chromium",
        "firefox": "firefox",
        "edge": "chromium",  # Edge usa Chromium channel
    }

    def __init__(self, logger=None, config=None):
        super().__init__(logger, config)
        self._playwright = None
        self._browser = None
        self._context = None
        self._page = None

    def open_browser(self, browser="chrome", headless=False, **kwargs):
        self._playwright = sync_playwright().start()
        browser_type = self.BROWSER_MAP.get(browser, "chromium")
        launcher = getattr(self._playwright, browser_type)

        launch_kwargs = {"headless": headless}
        if browser == "edge":
            launch_kwargs["channel"] = "msedge"
        elif browser == "chrome":
            launch_kwargs["channel"] = "chrome"

        self._browser = launcher.launch(**launch_kwargs)
        self._context = self._browser.new_context(**kwargs)
        self._page = self._context.new_page()

    def find_element(self, selector, by="css", timeout=10):
        locator = self._resolve_locator(selector, by)
        locator.wait_for(timeout=timeout * 1000)
        return locator

    def _resolve_locator(self, selector, by):
        if by == "xpath":
            return self._page.locator(f"xpath={selector}")
        elif by == "id":
            return self._page.locator(f"#{selector}")
        elif by == "text":
            return self._page.get_by_text(selector)
        else:
            return self._page.locator(selector)

    # ... demais métodos seguindo mesma interface
```

### 4.2 Playwright Actions (`rpa_3003/bots/playwright/actions.py`)

Mesma interface que `SeleniumActions`, mas usando API do Playwright.

---

## Fase 5 — CLI + Templates (Dias 7-8)

### 5.1 CLI (`rpa_3003/cli.py`)

Usar `click` como framework de CLI:

```python
import click

@click.group()
@click.version_option(version=__version__, prog_name="rpa3003")
def main():
    """RPA Framework Coop - CLI para gerenciamento de projetos RPA."""
    pass

@main.command()
@click.argument("name")
@click.option("--engine", default="selenium", type=click.Choice(["selenium", "playwright"]))
@click.option("--browser", default="chrome", type=click.Choice(["chrome", "firefox", "edge"]))
@click.option("--template", default="default")
def new(name, engine, browser, template):
    """Cria um novo projeto RPA."""
    # Valida nome do projeto
    # Verifica se já existe
    # Chama TemplateManager para criar estrutura
    # Configura global_vars com engine e browser
    # Exibe mensagem de sucesso

@main.command()
@click.argument("name")
@click.option("--env", default="dev", type=click.Choice(["dev", "prd"]))
@click.option("--headless", is_flag=True, default=False)
@click.option("--user", default=None)
def run(name, env, headless, user):
    """Executa um projeto RPA existente."""
    # Localiza o projeto
    # Configura logger com user
    # Executa main.py do projeto

@main.command(name="list")
def list_projects():
    """Lista todos os projetos RPA."""

@main.command()
@click.argument("name")
def info(name):
    """Mostra informações de um projeto."""
```

---

### 5.2 Template Manager (`rpa_3003/templates/template_manager.py`)

```python
class TemplateManager:
    """Gerencia a criação de projetos a partir de templates."""

    def __init__(self, templates_dir: str | None = None):
        self.templates_dir = templates_dir or os.path.join(
            os.path.dirname(__file__), "default"
        )

    def create_project(
        self,
        project_name: str,
        target_dir: str,
        engine: str = "selenium",
        browser: str = "chrome",
        template: str = "default"
    ) -> str:
        """Cria projeto completo a partir do template."""
        project_path = os.path.join(target_dir, project_name)

        # 1. Criar árvore de diretórios
        self._create_directories(project_path)

        # 2. Gerar arquivos a partir dos templates
        context = {
            "project_name": project_name,
            "engine": engine,
            "browser": browser,
        }
        self._render_templates(project_path, context)

        return project_path

    def _create_directories(self, project_path):
        dirs = [
            "workflows/dev",
            "workflows/prd",
            "logs",
            "data",
        ]
        for d in dirs:
            os.makedirs(os.path.join(project_path, d), exist_ok=True)

    def _render_templates(self, project_path, context):
        # Lê cada .tpl, substitui variáveis, grava como .py
```

---

### 5.3 Templates de Arquivo

#### `templates/default/main.py.tpl`

```python
"""
Projeto: {{project_name}}
Ponto de entrada principal do projeto RPA.
"""
import sys
import os

# Adiciona o diretório raiz do framework ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from rpa_3003.core.logger import RPALogger
from global_vars import *

def main(env: str = "dev", user: str = None):
    logger = RPALogger(
        project_name="{{project_name}}",
        log_dir=os.path.join(os.path.dirname(__file__), "logs"),
        user=user,
    )

    logger.info(f"Iniciando projeto {{project_name}} no ambiente {env}")

    try:
        if env == "dev":
            from workflows.dev.step_01_initialize import run
        else:
            from workflows.prd.step_01_initialize import run

        run(logger=logger)
        logger.info("Projeto finalizado com sucesso")

    except Exception as e:
        logger.critical(f"Erro fatal: {e}")
        raise

if __name__ == "__main__":
    env = sys.argv[1] if len(sys.argv) > 1 else "dev"
    user = sys.argv[2] if len(sys.argv) > 2 else None
    main(env=env, user=user)
```

#### `templates/default/global_vars.py.tpl`

```python
"""
Variáveis globais do projeto {{project_name}}.
"""

# Configurações do bot
ENGINE = "{{engine}}"           # "selenium" ou "playwright"
BROWSER = "{{browser}}"         # "chrome", "firefox" ou "edge"
HEADLESS = False
TIMEOUT = 10

# URLs e credenciais (configurar conforme necessidade)
BASE_URL = ""
```

#### `templates/default/step_01_initialize.py.tpl`

```python
"""
Step 01 - Inicialização
Abre o navegador e navega para a URL base.
"""
from global_vars import *

def run(logger=None):
    logger.info("Executando Step 01 - Inicialização")

    if ENGINE == "selenium":
        from rpa_3003.bots.selenium.browser import SeleniumBot as Bot
    else:
        from rpa_3003.bots.playwright.browser import PlaywrightBot as Bot

    bot = Bot(logger=logger)

    try:
        logger.info(f"Abrindo navegador {BROWSER} (headless={HEADLESS})")
        bot.open_browser(browser=BROWSER, headless=HEADLESS)

        if BASE_URL:
            logger.info(f"Navegando para {BASE_URL}")
            bot.navigate(BASE_URL)

        logger.info("Step 01 concluído com sucesso")

    except Exception as e:
        logger.error(f"Erro no Step 01: {e}")
        raise

    finally:
        bot.close_browser()
        logger.info("Navegador fechado")
```

---

## Fase 6 — Testes + Documentação (Dias 9-10)

### 6.1 Testes Unitários

| Arquivo de Teste | O que testa | Estratégia |
|------------------|-------------|------------|
| `test_logger.py` | RPALogger, RPAFormatter, rotação | Criar arquivo de log temporário, verificar formato |
| `test_file_utils.py` | Todas as funções de file_utils | Usar `tmp_path` do pytest |
| `test_json_utils.py` | Leitura, escrita, merge, validação | Arquivos JSON temporários |
| `test_csv_utils.py` | Leitura, escrita, append, filtro | Arquivos CSV temporários |
| `test_config.py` | Config load, save, get, set | Config temporário |
| `test_exceptions.py` | Hierarquia de exceções | Verificar herança |
| `test_cli.py` | Todos os comandos CLI | `click.testing.CliRunner` |
| `test_template_manager.py` | Criação de projetos | Diretório temporário |
| `test_selenium_browser.py` | SeleniumBot (mock) | Mock do webdriver |
| `test_playwright_browser.py` | PlaywrightBot (mock) | Mock do playwright |

#### Convenções de Teste

- Usar `pytest` como framework
- Usar fixtures para setup/teardown
- Usar `tmp_path` para arquivos temporários
- Usar `unittest.mock` para mockar WebDrivers e Playwright
- Meta: **cobertura >= 70%**

### 6.2 README.md

Documentar:
- Instalação (`pip install -e .`)
- Configuração de ambiente (install browsers para Playwright)
- Guia de início rápido (criar e rodar primeiro projeto)
- Referência da API (logger, utils, bots)
- Exemplos de uso
- Estrutura de diretórios
- Contribuição

### 6.3 `setup.py`

```python
from setuptools import setup, find_packages

setup(
    name="rpa-3003",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "selenium>=4.0.0",
        "playwright>=1.40.0",
        "webdriver-manager>=4.0.0",
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "rpa3003=rpa_3003.cli:main",
        ],
    },
    python_requires=">=3.9",
)
```

---

## Decisões Técnicas

### Por que `click` para CLI?

- API declarativa e limpa
- Suporte nativo a grupos de comandos, opções e argumentos
- `CliRunner` facilita testes
- Mensagens de ajuda automáticas

### Por que `RotatingFileHandler` ao invés de `TimedRotatingFileHandler`?

- Controle por tamanho é mais previsível para auditorias
- O nome do arquivo já contém a data (rotação "visual" por dia)
- Evita logs de tamanho descontrolado em dias com muita atividade

### Por que Classe Base Abstrata para Bots?

- Garante interface consistente entre Selenium e Playwright
- Permite trocar engine sem alterar código do projeto
- Facilita testes com mocks
- Segue Open/Closed Principle

### Por que `inspect` para obter caller no Logger?

- Python `logging` já expõe `pathname` e `lineno` via `LogRecord`
- Ajustando `stacklevel` nos métodos wrapper, o `logging` nativo captura corretamente
- Evita overhead de chamar `inspect.stack()` manualmente (mais lento)
- Solução recomendada a partir do Python 3.8

---

## Checklist de Entrega

- [ ] Estrutura de diretórios completa
- [ ] `rpa_3003/__init__.py` com versão
- [ ] `core/logger.py` — RPALogger + RPAFormatter
- [ ] `core/config.py` — Config
- [ ] `core/exceptions.py` — Exceções customizadas
- [ ] `utils/file_utils.py` — Funções de arquivo
- [ ] `utils/json_utils.py` — Funções JSON
- [ ] `utils/csv_utils.py` — Funções CSV
- [ ] `bots/base.py` — BotBase (ABC)
- [ ] `bots/selenium/browser.py` — SeleniumBot
- [ ] `bots/selenium/actions.py` — SeleniumActions
- [ ] `bots/playwright/browser.py` — PlaywrightBot
- [ ] `bots/playwright/actions.py` — PlaywrightActions
- [ ] `cli.py` — CLI com todos os comandos
- [ ] `templates/template_manager.py` — TemplateManager
- [ ] `templates/default/*.tpl` — Templates
- [ ] `setup.py` — Instalação
- [ ] `requirements.txt` — Dependências
- [ ] `tests/` — Testes unitários (cobertura >= 70%)
- [ ] `README.md` — Documentação completa
- [ ] Instalação funcional via `pip install -e .`
- [ ] Comando `rpa3003 new meu_teste` gera projeto funcional
- [ ] Comando `rpa3003 run meu_teste --env dev` executa sem erros
