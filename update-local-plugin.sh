#!/usr/bin/bash
set -euo pipefail

plugin_name=$1

OBSIDIAN_ROOT="/mnt/seagate/obsidian-vaults"
PLUGIN_ICONIC_MOD="/mnt/seagate/obsidian-central/plugins/iconic-mod"

# backup
#id=$(printf "%05d" $((RANDOM % 100000)))
#cp -r $OBSIDIAN_ROOT /mnt/seagate/temporary/$id

if [[ $plugin_name == "accdiv" ]]; then
    rm -rf /mnt/seagate/obsidian-vaults/main-vault/.obsidian/plugins/accdiv
    rm -rf /mnt/seagate/obsidian-central/plugins/accdiv

    cp -r /mnt/seagate/workspace/coding/projects/addons/obsidian/accdiv /mnt/seagate/obsidian-vaults/main-vault/.obsidian/plugins/accdiv
    cp -r /mnt/seagate/workspace/coding/projects/addons/obsidian/accdiv /mnt/seagate/obsidian-central/plugins/accdiv 
fi

if [[ $plugin_name == "iconic-mod" ]]; then
    # ESSE SCRIPT SOBREESCREVE ÍCONES CONFIGURADOS MANUALMENTE

    cd "$OBSIDIAN_ROOT" || exit

    # loop por cada vault
    for dir in */; do
        # verifica se o plugin antigo existe antes de remover
        old_plugin="$dir/.obsidian/plugins/iconic"
        
        if [[ -d "$old_plugin" ]]; then
            rm -rf "$old_plugin"
            echo "removido iconic antigo do vault: $dir"
        #else
            #echo "nenhum iconic antigo encontrado no vault: $dir"
        fi

        # copia o novo plugin
        #rm -rf "$dir/.obsidian/plugins/iconic-mod"
        cp -r "$PLUGIN_ICONIC_MOD" "$dir/.obsidian/plugins/"
        echo "copiado iconic-mod pro vault: $dir"
    done
fi