#$url = "https://github.com/AllenNeuralDynamics/aind-watchdog-service/actions/runs/9781777954/artifacts/1664898054"
$outputPath = Join-Path -Path $PSScriptRoot -ChildPath "watchdog.exe"
$outputPath = $outputPath | Resolve-Path
#Invoke-WebRequest -Uri $url -OutFile $outputPath


$taskAction = New-ScheduledTaskAction -Execute "$outputPath" # TODO add default arguments via cli if/when PR gets merged
$taskTriggerStartup = New-ScheduledTaskTrigger -AtStartup
$taskTriggerLogOn = New-ScheduledTaskTrigger -AtLogOn
$taskTriggerStartup.Delay = "PT30S"
$taskTriggerLogOn.Delay = "PT30S"

$taskSettings = New-ScheduledTaskSettingsSet -DontStopOnIdleEnd -ExecutionTimeLimit '00:00:00'
$taskPrincipal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType S4U -RunLevel Highest
$taskPath = "AIND"
$taskName = "aind-watchdog-service"
if (Get-ScheduledTask -TaskPath ("\" + $taskPath + "\") -TaskName $taskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskPath ("\" + $taskPath + "\") -TaskName $taskName -Confirm:$false
}
$fullTaskPath = "\" + $taskPath + "\" + $taskName
Register-ScheduledTask -TaskName $fullTaskPath -Action $taskAction -Trigger @($taskTriggerStartup, $taskTriggerLogOn) -Settings $taskSettings -Principal $taskPrincipal
