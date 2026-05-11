"""
CLI — Interface de linha de comando do rpa_3003.

Entry point: rpa3003
"""

import click

from rpa_3003 import __version__


@click.group()
@click.version_option(version=__version__, prog_name="rpa3003")
def main():
    """RPA Framework Coop — Automação RPA modular e extensível."""
    pass


@main.command()
@click.argument("nome")
@click.option("--engine", type=click.Choice(["selenium", "playwright"]), default="selenium", help="Engine de automação.")
@click.option("--browser", type=click.Choice(["chrome", "firefox", "edge"]), default="chrome", help="Navegador padrão.")
@click.option("--template", default="default", help="Template do projeto.")
def new(nome: str, engine: str, browser: str, template: str):
    """Cria novo projeto RPA."""
    click.echo(f"Criando projeto '{nome}' com engine={engine}, browser={browser}, template={template}...")
    # TODO: Implementar criação via TemplateManager


@main.command()
@click.argument("nome")
@click.option("--env", type=click.Choice(["dev", "prd"]), default="dev", help="Ambiente de execução.")
@click.option("--headless", is_flag=True, help="Executar em modo headless.")
@click.option("--user", default=None, help="Usuário para os logs.")
def run(nome: str, env: str, headless: bool, user: str):
    """Executa um projeto RPA."""
    click.echo(f"Executando projeto '{nome}' em ambiente={env}, headless={headless}...")
    # TODO: Implementar execução de projetos


@main.command(name="list")
def list_projects():
    """Lista todos os projetos RPA."""
    click.echo("Projetos disponíveis:")
    # TODO: Listar projetos do diretório projects/


@main.command()
@click.argument("nome")
def info(nome: str):
    """Exibe informações de um projeto RPA."""
    click.echo(f"Informações do projeto '{nome}':")
    # TODO: Exibir detalhes do projeto


@main.command()
def version():
    """Exibe a versão do framework."""
    click.echo(f"rpa3003 v{__version__}")


if __name__ == "__main__":
    main()
