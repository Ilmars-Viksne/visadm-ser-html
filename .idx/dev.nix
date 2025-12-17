{ pkgs, ... }: {
  # Specifies the Nix packages channel. "stable-24.05" ensures we use a
  # consistent and well-tested set of packages.
  channel = "stable-24.05";

  # A list of packages to install from the specified channel.
  packages = [
    # Installs the Python 3.11 interpreter.
    pkgs.python311
    # Installs Python packages directly through Nix for better reproducibility.
    pkgs.python311Packages.pandas
    pkgs.python311Packages.jinja2
  ];

  idx = {
    # A list of VS Code extensions to install from the Open VSX Registry.
    extensions = [ "ms-python.python" ];

    # Workspace lifecycle hooks.
    # The onCreate hook is no longer needed to install python packages,
    # as they are now managed directly by Nix.
    workspace = {
      onCreate = {};
    };
  };
}
