import shutil
from pathlib import Path

def get_dot_obsidian(vault_dir: Path):
    # obter o diretório .obsidian de um vault
    if vault_dir.name == ".obsidian":
       return vault_dir

    return Path(vault_dir, ".obsidian")

def apply_snippet(target_vault: Path, css_file: Path):
    # copiar um arquivo css pro diretório de snippets de um vault
    dir_dot = get_dot_obsidian(target_vault)
    dir_snippets = dir_dot / "snippets"

    shutil.copy2(
        src=css_file,
        dst=dir_snippets
    )

def apply_theme(target_vault: Path, theme_dir: Path):
    # copiar o diretório de um tema pra um vault
    # ignorando temas que não são diretórios ou não têm manifesto
    if not theme_dir.is_dir() or not Path(theme_dir / "manifest.json").exists():
        print("tema inválido")
        return    

    # montar o caminho do diretório de forma que ele seja criado
    # e não substituído pelo copytree
    dir_dot = get_dot_obsidian(target_vault)
    dir_themes = dir_dot / "themes"

    # sem isso, o copytree tentaria substituir a pasta .obsidian/themes
    # com a pasta do tema, ao invés de só adicionar ela
    # isso cria algo como .obsidian/themes/nome-do-tema
    destination = dir_themes / theme_dir.name

    shutil.copytree(
        src=theme_dir,
        dst=destination,
        dirs_exist_ok=True # sobreescrever caso o tema já exista
    )