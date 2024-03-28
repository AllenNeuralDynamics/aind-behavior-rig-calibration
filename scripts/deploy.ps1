Write-Output "Creating a Python environment..."
if (Test-Path -Path ./.venv) {
    Remove-Item ./.venv -Recurse -Force
}
&python -m venv ./.venv
&.venv\Scripts\activate
Write-Output "Installing python packages..."
&pip install .
Write-Output "Creating a Bonsai environment and installing packages..."
Set-Location ./bonsai
.\setup.ps1
Set-Location ../.
