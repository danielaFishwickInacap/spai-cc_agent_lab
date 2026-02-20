{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  # The name of our shell
  name = "gemini-dev-env";
  
  # The packages we want to have available in our shell
  buildInputs = [
    pkgs.python3
    pkgs.cope
    # Add other packages here
    pkgs.python3.pkgs.streamlit
  ];

  # Any shell commands to run when entering the environment
  shellHook = ''
    echo "Entering Gemini development environment..."
    # You could set environment variables here, for example:
    # export MY_VAR="hello"
  '';
}
