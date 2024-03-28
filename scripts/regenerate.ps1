Write-Output "Activating local Python environment..."
&.venv\Scripts\activate
Write-Output "Regenerating schemas..."
&python ./src/DataSchemas/regenerate.py