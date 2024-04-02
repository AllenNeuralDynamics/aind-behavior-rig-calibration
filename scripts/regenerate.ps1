Write-Output "Activating local Python environment..."
&.venv\Scripts\activate
Write-Output "Regenerating schemas..."
&python ./scripts/regenerate.py