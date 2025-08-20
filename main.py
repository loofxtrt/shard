import yaml
import json
from pathlib import Path

import apply

ALL_SNIPPETS = Path("/mnt/seagate/obsidian-central/vault-agnostic-snippets/")
SPECIAL_SNIPPETS = Path("/mnt/seagate/obsidian-central/vault-specific-snippets/")
ALL_THEMES = Path("/mnt/seagate/obsidian-central/themes/")
ALL_PLUGINS = Path("/mnt/seagate/obsidian-central/plugins/")
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
DEFAULT_COMMUNITY_PLUGINS = []

def apply_all_snippets(full_vault_path: Path, vault_name: str, vault_config: list, all_snippets_source: Path, special_snippets_source: Path, data_appearance_instance: dict):
    """
    aplicar os snippets e adiciona-los a config  
    no array de snippets da config, se "all" estiver presente, vai ser a aplicação de todos os snippets globais  
    se "special" estiver presente, vai aplicar os snippets específicos pra aquele vault  
    e se for uma listagem de nomes individuais, eles serão adicionados um por um  
          
    @param full_vault_path  
        caminho do vault onde o snippet deve ser aplicado  
      
    @param vault_name, vault_config  
        valores obtidos pela função run ao ler o config.yaml  
        vault_name é a chave e vault_config é o valor dessa chave contendo todas as listas necessárias  
        (themes, plugins, snippets etc.)  
      
    @param all_snippets_source, special_snippets_source  
        de onde a func deve pegar os snippets globais e específicos de vaults  
        melhor explicado na documentação da função run  
      
    @param data_appearance_instance  
        cópia do diciońario que representa o data_appearance.json, copiado pela função run
    """

    def wrap_snippet_apply(snippet_name: str, snippet_source: Path):
        """
        @param snippet_name  
            o nome do arquivo css (com ou sem .css)  
            
        @param snippet_source  
            um dos dois paths que foram passados pra função principal  
            (all_snippets_source e special_snippets_source)
        """
        
        # IMPORTANTE: no appearance.json, o snippet não deve ter .css no final
        # mas a extensão deve ser mantida pra função de apply_snippet não falhar
        s_stem = snippet_name.replace(".css", "")

        data_appearance_instance["enabledCssSnippets"].append(s_stem)
        apply.apply_snippet(full_vault_path, snippet_source / snippet_name)

    snippets = vault_config.get("snippets") or []
    if "all" in snippets:
        # obter todos os arquivos que terminam em .css
        for css_file in all_snippets_source.glob("*.css"):
            wrap_snippet_apply(snippet_name=css_file.name, snippet_source=all_snippets_source)
    else:
        # obter o nome de todos os snippets listados na config
        for s_name in snippets:
            if not s_name.endswith(".css"):
                s_name += ".css"
            wrap_snippet_apply(snippet_name=s_name, snippet_source=all_snippets_source)
    
    if "special" in snippets:
        # aplicar os snippets específicos pra um vault só
        for css_file in special_snippets_source.glob("*.css"):
            if css_file.name.startswith(vault_name):
                wrap_snippet_apply(snippet_name=css_file.name, snippet_source=special_snippets_source)

def apply_all_themes(full_vault_path: Path, vault_config: list, themes_source: Path, data_appearance_instance: dict):
    """
    aplicar todos os temas e adiciona-los a config  
    essa função tem explicação de parâmetros limitada porque alguns já foram explicados em apply_all_snippets  
      
    @param vault_config  
        dicionário obtido pela função run que contém a lista "themes"  
        é necessário apenas a config, e não o nome como na apply_all_snippets,  
        porque não existem plugins que só servem pra um vault com nome específico  
      
    @param themes_source  
        de onde a função deve pegar os temas pra copiar  
    """
    
    # aplicar os temas e adiciona-los a config
    # (com enumerate pra saber qual ativar)
    for i, theme_name in enumerate(vault_config["themes"] or []):
        # caso o tema seja o primeiro da lista, ele vai ser o ativo por padrão
        if i == 0:
            data_appearance_instance["cssTheme"] = theme_name
        apply.apply_theme(full_vault_path, themes_source / theme_name)

def apply_all_plugins(full_vault_path: Path, vault_config: list, plugins_source: Path, data_community_plugins_instance: list):
    """
    aplica todos os temas e os adiciona ao array do community-plugins.json  
    explicação de parâmetros limitada por explicação já existente em apply_all_themes  
      
    @param plugins_source  
        de onde a função vai pegar os temas pra copiar  
      
    @param data_community_plugins_instance  
        cópia do array que representa esse arquivo de configuração, copiado pela função run
    """

    plugins = vault_config.get("plugins") or []
    for p_name in plugins:
        data_community_plugins_instance.append(p_name)
        apply.apply_plugin(full_vault_path, plugins_source / p_name)

def run(obsidian_root: Path, plugins_source: Path, themes_source: Path, all_snippets_source: Path, special_snippets_source: Path):
    """
    função principal que lê o arquivo yaml de configuração dos vaults  
    e chama outras funções correspondentes as configs encontradas  
      
    @param obsidian_root
        diretório base onde todos os vaults ficam
      
    @param all_snippets_source, plugins_source, themes_source  
        de onde a func deve pegar os snippets/temas/plugins
        é de lá que eles serão copiados pra dentro do vault  
      
    @param special_snippets_source  
        de onde a func deve pegar os snippets específicos de vaults  
        os .css desse diretório devem sempre começar com o nome exato do diretório do vault  
        ex: pro main-vault, main-vault_account-card.css
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
        data_community_plugins = DEFAULT_COMMUNITY_PLUGINS.copy()
        
        # aplicar snippets, temas e plugins
        apply_all_snippets(
            full_vault_path=path_current_vault, vault_name=vault_name, vault_config=vault_config,
            all_snippets_source=all_snippets_source, special_snippets_source=special_snippets_source, data_appearance_instance=data_appearance
        )

        apply_all_themes(
            full_vault_path=path_current_vault, vault_config=vault_config,
            themes_source=themes_source, data_appearance_instance=data_appearance
        )

        apply_all_plugins(
            full_vault_path=path_current_vault, vault_config=vault_config,
            plugins_source=plugins_source, data_community_plugins_instance=data_community_plugins
        )
        
        # escrever os arquivos de configuração do obsidian pro vault
        this_vault_dot = apply.get_dot_obsidian(path_current_vault)

        write_dot_obsidian_json(dot_obsidian=this_vault_dot, data_to_write=data_app, json_name="app.json")
        write_dot_obsidian_json(dot_obsidian=this_vault_dot, data_to_write=data_appearance, json_name="appearance.json")
        write_dot_obsidian_json(dot_obsidian=this_vault_dot, data_to_write=data_community_plugins, json_name="community-plugins.json")

def generate_yaml_config(obsidian_root: Path, snippets_all: bool = True, default_theme_list: list[str] = None, default_plugin_list: list[str] = None):
    """
    gera um arquivo yaml de config listando todos os vaults disponíveis no obsidian_root  
      
    @param obsidian_root  
        onde todos os vaults estão  
      
    @param snippets_all  
        definir se por padrão todos os vaults vão ter os mesmos snippets ativos  
      
    @param default_theme_list  
        definir os temas padrão de todos os vaults  
      
    @param default_plugin_list  
        definir os plugins padrão de todos os vaults
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
            "plugins": None if not default_plugin_list else default_plugin_list,
            "themes": None if not default_theme_list else default_theme_list,
            "snippets": None if not snippets_all else ["all"],
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
    
    print(f"{dot_obsidian.parent.name}: {json_name} escrito")

#generate_yaml_config(obsidian_root=ALL_VAULTS, default_theme_list=["Crying Obsidian"], default_plugin_list=["iconic"], snippets_all=True)
run(obsidian_root=TEST_VAULTS, plugins_source=ALL_PLUGINS, themes_source=ALL_THEMES, all_snippets_source=ALL_SNIPPETS, special_snippets_source=SPECIAL_SNIPPETS)