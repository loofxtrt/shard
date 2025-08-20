import json
from pathlib import Path

import apply
import main

def update_iconic_rules(persistent_data_dir: Path, obsidian_root: Path):
    rules = persistent_data_dir / "iconic_data.json"
    if not rules.exists():
        return
    
    with open(rules, "r") as f:
        contents = json.load(f)
    
    for vault in obsidian_root.iterdir():
        if vault.name.startswith("."):
            continue

        plugins = apply.get_sub_dot(vault_dir=vault, sub_dir_name="plugins")
        
        iconic_dir = plugins / "iconic"
        if not iconic_dir.exists():
            print(f"{vault.name}: não tem o plugin iconic")
            continue
        
        iconic_data = iconic_dir / "data.json"
        if not iconic_data.exists():
            print(f"{vault.name}: {iconic_data} não é um arquivo data.json válido")
            continue
        
        with open(iconic_data, "w") as f:
            json.dump(contents, f, indent=4)
        
        print(f"{vault.name} regras do iconic sobreescritas")

update_iconic_rules(
    persistent_data_dir=main.PERSISTENT_DATA,
    obsidian_root=main.ALL_VAULTS
)