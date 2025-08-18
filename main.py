from pathlib import Path
import yaml

ALL_SNIPPETS = Path("/mnt/seagate/obsidian-central/snippets/")
ALL_THEMES = Path("/mnt/seagate/obsidian-central/themes/")

def generate_yaml_config(obsidian_root: Path, snippets_source: Path, themes_source: Path):
    vaults = []
    snippets = []
    themes = []

    for v in obsidian_root.iterdir():
        if not v.is_dir() or v.name.startswith("."):
            continue
            
        vaults.append(v.name)

    for s in snippets_source.iterdir():
        if not s.is_file() or not s.suffix == ".css":
            continue

        snippets.append(s.name)
    
    for t in themes_source.iterdir():
        if not t.is_dir():
            continue

        themes.append(t.name)
    
    data = {}

    for this_vault in vaults:
        options = {
            "themes": themes,
            "snippets": snippets,
        }
        data[this_vault] = options

    print(data)
    with open("config.yaml", "w") as f:
        yaml.dump(data, f)

generate_yaml_config(
    obsidian_root=Path("/mnt/seagate/obsidian-vaults/"),
    snippets_source=ALL_SNIPPETS,
    themes_source=ALL_THEMES
)