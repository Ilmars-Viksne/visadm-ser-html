{ pkgs, ... }: {
  # Specifies the Nix packages channel.
  # "stable-24.11" for Antigravity's next-gen runtime.
  channel = "stable-24.11";

  # A list of packages to install from the specified channel.
  packages = [
    # Installs the Python 3.12 interpreter (stable for Antigravity).
    pkgs.python312Full
    # Installs Python packages directly through Nix for better reproducibility.
    pkgs.python312Packages.pandas
    pkgs.python312Packages.jinja2
    pkgs.python312Packages.python-dotenv
    pkgs.python312Packages.pytest
  ];

  # Antigravity-specific workspace configuration.
  idx = {
    # Extensions for the Antigravity 'Preview' and 'Debugger' tools.
    extensions = [
      "ms-python.python"
      "ms-python.debugpy"
      "google.antigravity-preview" # Antigravity Preview
      "google.antigravity-debugger" # Antigravity Debugger
    ];

    # Workspace lifecycle hooks.
    workspace = {
      # Initial setup for the Antigravity environment.
      onCreate = {
        # Ensure dependencies are installed if not using Nix packages exclusively.
        # pip-install = "pip install -e .";
      };
      # Start services or tools every time the workspace starts.
      onStart = {};
    };

    # Configure the Antigravity Preview tool.
    previews = {
      enable = true;
      previews = {
        # Since this is a CLI tool, we don't have a web server by default.
        # However, we can define a preview if it was a web app.
      };
    };
  };
}
