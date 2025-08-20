#!usr/bin/bash
plugin_name=$1
if [[ $plugin_name == "accdiv" ]]; then
    rm -rf /mnt/seagate/obsidian-vaults/main-vault/.obsidian/plugins/accdiv
    rm -rf /mnt/seagate/obsidian-central/plugins/accdiv

    cp -r /mnt/seagate/workspace/coding/projects/addons/obsidian/accdiv /mnt/seagate/obsidian-vaults/main-vault/.obsidian/plugins/accdiv
    cp -r /mnt/seagate/workspace/coding/projects/addons/obsidian/accdiv /mnt/seagate/obsidian-central/plugins/accdiv 
fi