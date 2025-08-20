# funcionamento
- o script lê a config.yaml
- pros snippets, ele aplica:
    - snippets individuais que devem ser listados por nome na config (com ou sem .css no final)
    - todos os snippets específicos de um vault caso "special" esteja na lista
    - todos os snippets globais caso "all" esteja na lista (isso não inclue os especiais. o "special" deve ser adicionado junto do "all" se precisar de todos)
- pra temas, ele instala todos e ativa o primeiro da lista
- pra plugins, ele instala e ativa todos 

# organização
o script deve ter uma fonte de onde copiar os temas, plugins e snippets  
ex: ROOT = `/mnt/seagate/obsidian-central/`  
e dentro dessa pasta, ter subpastas pra:
- snippets globais (`ROOT/vault-agnostic-snippets`)
- snippets especiais (`ROOT/vault-specific-snippets`)
- temas (`ROOT/themes`)
- plugins(`ROOT/plugins`)
essas pastas podem ter qualquer nome e devem ser passadas como argumentos da função run no main.py
  
a pasta local-data serve pra backups e arquivos temporários,  
o persistent_data serve pra arquivos de configuração definitivos, como as configs do plugin iconic