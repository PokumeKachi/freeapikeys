{
    pkgs ? import <nixpkgs> { },
}:
pkgs.mkShell {
    packages = with pkgs; [
        python3
        python3Packages.cryptography
        python3Packages.argon2-cffi

        dialog

        just
    ];
}
