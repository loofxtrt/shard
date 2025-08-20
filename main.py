import yaml
import json
from pathlib import Path

import apply

ALL_SNIPPETS = Path("/mnt/seagate/obsidian-central/snippets/")
ALL_THEMES = Path("/mnt/seagate/obsidian-central/themes/")
ALL_VAULTS = Path("/mnt/seagate/obsidian-vaults/")
TEST_VAULTS = Path("/mnt/seagate/obsidiadididn-tests/")

# gerar os dicionários que depois serão convertidos em configs json pro vault
DEFAULT_APP = {
    "readableLineLength": True, # concentrar o conteúdo no centro
    "spellcheck": False,
    "showInlineTitle": True, # mostrar o título da nota
    "promptDelete": True, # perguntar antes de deletar pastas e arquivos
    "attachmentFolderPath": "_attachments"
}
DEFAULT_APPEARANCE = {
    "enabledCssSnippets": [],
    "cssTheme": None,
    "accentColor": "",
    "showViewHeader": True,
    "showRibbon": True
}

def run(obsidian_root: Path, snippets_source, themes_source):
    """
    função principal que lê o arquivo yaml de configuração dos vaults  
    e chama outras funções correspondentes as configs encontradas  
      
    @param obsidian_root
        diretório base onde todos os vaults ficam
      
    @param snippets_source, themes_source
        de onde a func deve pegar os snippets/temas. é de lá que eles serão copiados  
        pra dentro do vault
    """

    # ler o arquivo de configuração
    with open("config.yaml", "r") as f:
        data = yaml.safe_load(f)

    # iterar pelo nome de cada vault presente no arquivo,
    # aplicando os temas, plugins e snippets especificados
    for vault_name, vault_config in data.items():
        # montar o caminho do vault atual
        path_current_vault = obsidian_root / vault_name
        if not path_current_vault.exists():
            continue

        # gerar configurações base
        data_app = DEFAULT_APP.copy()
        data_appearance = DEFAULT_APPEARANCE.copy()
        
        # aplicar os snippets e adiciona-los a config
        # pode ser uma aplicação de todos caso "all" esteja presente no array de snippets da config
        # ou apenas de alguns específicos caso contrário
        def wrap_snippet_apply(snippet_name: str):
            # IMPORTANTE: no appearance.json, o snippet não deve ter .css no final
            # mas a extensão deve ser mantida pra função de apply_snippet não falhar
            s_stem = snippet_name.replace(".css", "")

            data_appearance["enabledCssSnippets"].append(s_stem)
            apply.apply_snippet(path_current_vault, snippets_source / snippet_name)

        snippets = vault_config.get("snippets") or []
        if "all" in snippets:
            # obter todos os arquivos que terminam em .css
            for css_file in snippets_source.glob("*.css"):
                wrap_snippet_apply(snippet_name=css_file.name)
        else:
            # obter o nome de todos os snippets listados na config
            for s_name in snippets:
                wrap_snippet_apply(snippet_name=s_name)

        # aplicar os temas e adiciona-los a config
        # (com enumerate pra saber qual ativar)
        for i, theme_name in enumerate(vault_config["themes"] or []):
            # caso o tema seja o primeiro da lista, ele vai ser o ativo por padrão
            if i == 0:
                data_appearance["cssTheme"] = theme_name
            apply.apply_theme(path_current_vault, themes_source / theme_name)
        
        # escrever os arquivos de configuração do obsidian pro vault
        this_vault_dot = apply.get_dot_obsidian(path_current_vault)

        write_dot_obsidian_json(dot_obsidian=this_vault_dot, data_to_write=data_app, json_name="app.json")
        write_dot_obsidian_json(dot_obsidian=this_vault_dot, data_to_write=data_appearance, json_name="appearance.json")

def generate_yaml_config(obsidian_root: Path, snippets_all: bool = True, default_theme_list: list[str] = None):
    """
    gera um arquivo yaml de config listando todos os vaults disponíveis no obsidian_root  
      
    @param obsidian_root  
        onde todos os vaults estão  
      
    @param snippets_all  
        definir se por padrão todos os vaults vão ter os mesmos snippets ativos  
      
    @param default_theme_list  
        definir os temas padrão de todos os vaults
    """

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
            "themes": None if not default_theme_list else default_theme_list,
            "snippets": None if not snippets_all else ["all"]
        }
        data[this_vault] = options

    # escrever o arquivo yaml final
    with open("config.yaml", "w") as f:
        yaml.dump(data, f)

def write_dot_obsidian_json(data_to_write, dot_obsidian: Path, json_name: str):
    """
    escreve as configurações passadas pra função num .json que fica no .obsidian  
    esse json pode ser app.json, appearance.json etc.  
      
    @param data_to_write  
        as informações que devem ser escritas  
      
    @param dot_obsidian  
        o .obsidian do vault em que essas informações devem ser escritas  
      
    @param json_name  
        que nome o arquivo json deve levar
    """

    if not json_name.endswith(".json"):
        json_name += ".json"

    with open(dot_obsidian / json_name, "w") as f:
        json.dump(data_to_write, f, indent=4)
    
    print(f"{dot_obsidian.parent.name}: {json_name}.json escrito")

generate_yaml_config(obsidian_root=ALL_VAULTS, default_theme_list=["Crying Obsidian"], snippets_all=True)
run(obsidian_root=TEST_VAULTS, snippets_source=ALL_SNIPPETS, themes_source=ALL_THEMES)