from pathlib import Path
import yaml

import apply

ALL_SNIPPETS = Path("/mnt/seagate/obsidian-central/snippets/")
ALL_THEMES = Path("/mnt/seagate/obsidian-central/themes/")

def run():
    # ler o arquivo de configuração
    with open("config.yaml", "r") as f:
        data = yaml.safe_load(f)

    # iterar por cada vault presente no arquivo,
    # aplicando os temas, plugins e snippets especificados  
    for vault_name, vault_config in data.items():
        # snippets
        for snippet in vault_config["snippets"] or []:
            apply.apply_snippet(
                Path(f"/mnt/seagate/obsidian-vaults/{vault_name}"),
                ALL_SNIPPETS / str(snippet)
            )

def generate_yaml_config(obsidian_root: Path):
    vaults = []
    for v in obsidian_root.iterdir():
        if not v.is_dir() or v.name.startswith("."):
            continue
            
        vaults.append(v.name)

    data = {}
    for this_vault in vaults:
        options = {
            "themes": None,
            "snippets": None
        }
        data[this_vault] = options

    with open("config.yaml", "w") as f:
        yaml.dump(data, f)

#generate_yaml_config(
#    obsidian_root=Path("/mnt/seagate/obsidian-vaults/"),
#)

run()