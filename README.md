# Sublime Text CSharpier plugin (forked)

Small plugin that adds a command to run `dotnet-csharpier` on C# files.

[CSharpier][csharpier] is an opinionated code formatter for C#.

You can invoke the formatter manually from the command menu, "CSharpier: format file". You can also configure the plugin to run automatically on save by editing the package settings (Preferences/Package Settings/CSharpier):

```json
{
  "format_on_save": true
}
```

Note that the command is only visible, and runs on save, when used on C# files.

## Install

To install csharpier: `dotnet tool install csharpier -g`.

`dotnet` is part of the .NET CLI, included in the [.NET SDK][dotnet-sdk].

### Package Control

Hopefully soon: in [@wbond's Package Control][package-control]. Until then, open the command menu (default `ctrl-shift-p`), choose `Package Control: Add Repository` and paste in the repo URL: `https://github.com/jonlabelle/sublime-text-csharpier-plugin`.

To install the package, choose `Package Control: Install Package` from the command menu and search for `csharpier`.

### Manual package installation

Clone this repository from your Sublime Text packages directory:

#### Linux

```sh
cd ~/.config/sublime-text/Packages
git clone https://github.com/jonlabelle/sublime-text-csharpier-plugin "Csharpier"
```

#### macOS

```sh
cd "~/Library/Application Support/Sublime Text/Packages"
git clone https://github.com/jonlabelle/sublime-text-csharpier-plugin "Csharpier"
```

#### Windows

```sh
cd "%APPDATA%\Sublime Text\Packages"
git clone https://github.com/jonlabelle/sublime-text-csharpier-plugin "Csharpier"
```

## Settings

You can configure the plugin by editing the package settings (`Preferences/Package Settings/CSharpier`).

```jsonc
{
  // Format C# files on save
  "format_on_save": false,

  // Path to the dotnet-csharpier executable
  "csharpier_path": "~/.dotnet/tools/dotnet-csharpier",

  // The log level to use when running the formatter
  "log_level": "WARNING" // Acceptable values: "debug", "info", "warning", "error", "critical"
}
```

## Key bindings

To add a key binding, open `Preferences: Key Bindings`. Add a new key binding to the key bindings file:

```json
[
  {
    "keys": ["shift+alt+f"],
    "command": "csharpier",
    "context": [
      { "key": "selector", "operator": "equal", "operand": "source.cs" }
    ]
  }
]
```

[csharpier]: https://csharpier.com
[package-control]: https://packagecontrol.io
[dotnet-sdk]: https://learn.microsoft.com/en-us/dotnet/core/sdk#how-to-install-the-net-sdk
