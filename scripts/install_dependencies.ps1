Write-Host "Installing dependencies..." -ForegroundColor White
$autoaccept = @("--accept-package-agreements", "--accept-source-agreements")

winget install -e --id 7zip.7zip @autoaccept
winget install ffmpeg -v 7.0 @autoaccept
winget install -e --id Git.Git @autoaccept
winget install -e --id Python.Python.3.11 -v 3.11.8 --scope user @autoaccept
winget install -e --id Microsoft.VisualStudioCode --scope user @autoaccept --override '/SILENT /mergetasks="!runcode,addcontextmenufiles,addcontextmenufolders"'
winget install -e --id Microsoft.DotNet.Framework.DeveloperPack_4 @autoaccept
Winget install "Microsoft Visual C++ 2012 Redistributable (x64)" --force @autoaccept
winget install -e --id Nvidia.GeForceExperience -v 3.26.0.160 @autoaccept
winget install -e --id Nvidia.CUDA -v 11.3 @autoaccept
winget install -e --id Notepad++.Notepad++ @autoaccept
winget install --id=Microsoft.DotNet.SDK.8  -e @autoaccept

## Install dotnet tools

dotnet tool install --global Bonsai.Sgen
dotnet tool install --global Harp.Toolkit

## Install vscode extensions
$extensions =
    "eamodio.gitlens",
    "donjayamanne.python-extension-pack"
    "redhat.vscode-yaml"

$cmd = "code --list-extensions"
Invoke-Expression $cmd -OutVariable output | Out-Null
$installed = $output -split "\s"

foreach ($ext in $extensions) {
    if ($installed.Contains($ext)) {
        Write-Host $ext "already installed." -ForegroundColor Gray
    } else {
        Write-Host "Installing" $ext "..." -ForegroundColor White
        code --install-extension $ext
    }
}