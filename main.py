from pathlib import Path
import yaml

import apply

ALL_SNIPPETS = Path("/mnt/seagate/obsidian-central/snippets/")
ALL_THEMES = Path("/mnt/seagate/obsidian-central/themes/")
ALL_VAULTS = Path("/mnt/seagate/obsidian-vaults/")

def run():
    # ler o arquivo de configuração
    with open("config.yaml", "r") as f:
        data = yaml.safe_load(f)

    # iterar por cada vault presente no arquivo,
    # aplicando os temas, plugins e snippets especificados
    for vault_name, vault_config in data.items():
        # montar o caminho do vault atual
        path_current_vault = ALL_VAULTS / vault_name
        
        # snippets
        for snippet in vault_config["snippets"] or []:
            apply.apply_snippet(path_current_vault, ALL_SNIPPETS / snippet)

        # temas
        for theme in vault_config["themes"] or []:
            apply.apply_theme(path_current_vault, ALL_THEMES / theme)

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

#generate_yaml_config(
#    obsidian_root=Path("/mnt/seagate/obsidian-vaults/"),
#)

run()