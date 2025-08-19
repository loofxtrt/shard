import yaml
import json
from pathlib import Path

import apply

ALL_SNIPPETS = Path("/mnt/seagate/obsidian-central/snippets/")
ALL_THEMES = Path("/mnt/seagate/obsidian-central/themes/")
ALL_VAULTS = Path("/mnt/seagate/obsidian-vaults/")
TEST_VAULTS = Path("/mnt/seagate/obsidiadididn-tests/")

def run(obsidian_root: Path, snippets_source, themes_source):
    # ler o arquivo de configuração
    with open("config.yaml", "r") as f:
        data = yaml.safe_load(f)

    # iterar por cada vault presente no arquivo,
    # aplicando os temas, plugins e snippets especificados
    for vault_name, vault_config in data.items():
        # montar o caminho do vault atual
        path_current_vault = obsidian_root / vault_name
        if not path_current_vault.exists():
            continue

        # gerar os dicionários que depois serão convertidos em configs json pro vault
        data_app = {
            "readableLineLength": True, # concentrar o conteúdo no centro
            "spellcheck": False,
            "showInlineTitle": True, # mostrar o título da nota
            "promptDelete": True, # perguntar antes de deletar pastas e arquivos
            "attachmentFolderPath": "_attachments"
        }
        data_appearance = {
            "enabledCssSnippets": [],
            "cssTheme": None,
            "accentColor": "",
            "showViewHeader": True,
            "showRibbon": True
        }
        
        # snippets
        for snippet_name in vault_config["snippets"] or []:
            # aplicar os snippets e gerar a config
            # IMPORTANTE: no appearance.json, o snippet não deve ter .css no final
            data_appearance["enabledCssSnippets"].append(
                snippet_name.replace(".css", "")
            )
            apply.apply_snippet(path_current_vault, snippets_source / snippet_name)

        # temas (com enumerate pra saber qual aplicar)
        for index, theme_name in enumerate(vault_config["themes"] or []):
            # aplicar todos os temas e gerar a config caso ele seja o primeiro da lista
            if index == 0: data_appearance["cssTheme"] = theme_name
            apply.apply_theme(path_current_vault, themes_source / theme_name)
        
        # escrever os arquivos de configuração do obsidian pro vault
        this_vault_dot = apply.get_dot_obsidian(path_current_vault)

        with open(this_vault_dot / "app.json", "w") as app_file:
            json.dump(data_app, app_file, indent=4)
            print(f"{vault_name}: app.json escrito")
        
        with open(this_vault_dot / "appearance.json", "w") as appearance_file:
            json.dump(data_appearance, appearance_file, indent=4)
            print(f"{vault_name}: appearance.json escrito")

def generate_yaml_config(obsidian_root: Path):
    # ESSA FUNÇÃO ATUALMENTE SOBREESCREVE O YAML, RESETANDO ELE

    # obter os nomes de todos os vaults a partir de um nível do obsidian root
    # o obsidian root deve ser o diretório pai de todos os vaults
    vaults = []
    for v in obsidian_root.iterdir():
        # eliminando arquivos ou diretórios ocultos
        if not v.is_dir() or v.name.startswith("."):
            continue
            
        vaults.append(v.name)

    # criar o dicionário vazio pra cada vault
    data = {}
    for this_vault in vaults:
        options = {
            "themes": None,
            "snippets": None
        }
        data[this_vault] = options

    # escrever o arquivo yaml final
    with open("config.yaml", "w") as f:
        yaml.dump(data, f)

#generate_yaml_config(obsidian_root=ALL_VAULTS)

run(obsidian_root=TEST_VAULTS, snippets_source=ALL_SNIPPETS, themes_source=ALL_THEMES)