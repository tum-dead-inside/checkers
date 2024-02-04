{ pkgs ? import <nixpkgs> {} }:

let
  my-python-packages = ps: with ps; [ tkinter pillow ];
  my-python = pkgs.python3.withPackages my-python-packages;
  pyright = pkgs.nodePackages.pyright;
  pipreqs = pkgs.pipreqs;
in
pkgs.mkShell {
  buildInputs = [ my-python pyright pipreqs ];
}
