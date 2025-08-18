import shutil
from pathlib import Path

def get_dot_obsidian(vault_dir: Path):
    if vault_dir.name == ".obsidian":
       return vault_dir

    return Path(vault_dir, ".obsidian")

def apply_snippet(target_vault: Path, css_file: Path):
    dir_dot = get_dot_obsidian(target_vault)
    dir_snippets = dir_dot / "snippets"

    shutil.copy2(
        src=css_file,
        dst=dir_snippets
    )

def apply_theme(target_vault: Path, theme_dir: Path):
    if not theme_dir.is_dir():
        print("tema inválido")
        return
    
    dir_dot = get_dot_obsidian(target_vault)
    dir_themes = dir_dot / "themes"

    shutil.copy2(
        src=theme_dir,
        dst=dir_themes
    )