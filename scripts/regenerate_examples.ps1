Write-Output "Regenerating examples..."

if (-not (Test-Path -Path "./local")) {
    New-Item -ItemType Directory -Path "./local"
}
&.venv\Scripts\activate
ls examples\*.py | %{ python $_.Fullname}
