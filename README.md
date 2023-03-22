Sublime Text CSharpier plugin
=========================

Small plugin that adds a command to run `dotnet-csharpier` on C# files.

[CSharpier][csharpier] is an opinionated code formatter for C#.

You can invoke the formatter manually from the command menu, "CSharpier: format file". You can also configure the plugin to run automatically on save by editing your user/project settings to include:

    {
        "csharpier.format_on_save": true,
    }

Note that the command is only visible, and runs on save, when used on C# files.

Thanks to [@thijsdezoete's isort plugin][isort-plugin] for providing a convenient starting point!


## Install

To install csharpier: `dotnet tool install csharpier -g`.

`dotnet` is part of the .NET CLI, included in the [.NET SDK][dotnet-sdk].

### Package Control

Hopefully soon: in [@wbond's Package Control][package-control]. Until then, open the command menu (default `ctrl-shift-p`), choose `Package Control: Add Repository` and paste in the repo URL: `https://github.com/mkonstapel/sublime-text-csharpier-plugin`.

To install the package, choose `Package Control: Install Package` from the command menu and search for `csharpier`.

### Manual package installation

Clone this repository from your Sublime packages directory:

#### Linux

```
$ cd ~/.config/sublime-text/Packages
$ git clone https://github.com/mkonstapel/sublime-text-csharpier-plugin
```

#### OSX (untested)

```
$ cd "~/Library/Application Support/Sublime Text/Packages"
$ git clone https://github.com/mkonstapel/sublime-text-csharpier-plugin
```

#### Windows

```
$ cd "%APPDATA%\Sublime Text\Packages"
$ git clone https://github.com/mkonstapel/sublime-text-csharpier-plugin
```

NOTE: if you install the package manually, but you also use Package Control, delete the `sublime-text-csharpier-plugin/package-metadata.json` file. Otherwise, Package Control will think it's an "orphaned" package (on disk, but not requested by you) and will delete it the next time you start Sublime Text.

[csharpier]: https://csharpier.com
[package-control]: https://packagecontrol.io/
[isort-plugin]: https://github.com/thijsdezoete/sublime-text-isort-plugin
[dotnet-sdk]: https://learn.microsoft.com/en-us/dotnet/core/sdk#how-to-install-the-net-sdk

