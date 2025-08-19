import shutil
from pathlib import Path

def get_dot_obsidian(vault_dir: Path):
    # obter o diretório .obsidian de um vault
    # retornar diretóro caso o path passado já seja um .obsidian
    if vault_dir.name == ".obsidian":
        return vault_dir
    
    # construir o path e fazer as verificações
    if not vault_dir.exists():
        print(f"{vault_dir.name}: o path do vault não existe"); return False

    dot_obsidian = vault_dir / ".obsidian"
    
    if not dot_obsidian.exists:
        print(f"{vault_dir.name}: .obsidian não existe, vault inválido"); return False
    
    return dot_obsidian

def get_sub_dot(vault_dir: Path, sub_dir_name: str):
    """
    @param vault_dir  
        o diretório no qual a função vai obter o .obsidian e a partir daí obter o subdiretório
        por que é usado vault_dir ao invés de um .obsidian logo?  
        porque caso o vault não exista, essa função faz o mkdir, então isso quebra a segurança do get_dot_obsidian  
        porque mesmo seja um vault inválido, a get_sub_dot vai fazer ele existir
    """

    # apenas prosseguir caso seja um vault válido
    dot_obsidian = get_dot_obsidian(vault_dir)
    if not dot_obsidian:
        return

    # obter um diretório que é filho do .obsidian, como snippets, themes, plugins etc
    # também garante que o diretório existe antes de retornar
    sub_dot = dot_obsidian / sub_dir_name
    sub_dot.mkdir(parents=True, exist_ok=True)

    return sub_dot

def apply_snippet(target_vault: Path, css_file: Path):
    # copiar um arquivo css pro diretório de snippets de um vault
    dir_snippets = get_sub_dot(target_vault, "snippets")
    if not dir_snippets:
        return

    shutil.copy2(
        src=css_file,
        dst=dir_snippets
    )

    print(f"{target_vault.name}: snippet {css_file.name} aplicado")

def apply_theme(target_vault: Path, theme_dir: Path):
    # copiar o diretório de um tema pra um vault
    # ignorando temas que não são diretórios ou não têm manifesto
    if not theme_dir.is_dir() or not Path(theme_dir / "manifest.json").exists():
        print("tema inválido")
        return    

    # montar o caminho do diretório de forma que ele seja criado
    # e não substituído pelo copytree
    dir_themes = get_sub_dot(target_vault, "themes")
    if not dir_themes:
        return

    # sem isso, o copytree tentaria substituir a pasta .obsidian/themes
    # com a pasta do tema, ao invés de só adicionar ela
    # isso cria algo como .obsidian/themes/nome-do-tema
    destination = dir_themes / theme_dir.name

    shutil.copytree(
        src=theme_dir,
        dst=destination,
        dirs_exist_ok=True # sobreescrever caso o tema já exista
    )

    print(f"{target_vault.name}: tema {theme_dir.name} aplicado")