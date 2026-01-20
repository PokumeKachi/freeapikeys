set shell := ["bash", "-cu"]

_default:
    @just --choose

shell:
    nix-shell

encrypt:
    cd data && pass=$(systemd-ask-password "password:"); \
    echo "The password is $pass"; \
    printf "%s" "$pass" | python ../secure.py encrypt

decrypt:
    cd data && pass=$(systemd-ask-password "password:"); \
    echo "The password is $pass"; \
    printf "%s" "$pass" | python ../secure.py decrypt

git:
    gitui
