<#
  Publish an itinerary so everyone who opens the site gets it.

  Click Export in the app, then point this at the downloaded file:

      .\publish.ps1 ~\Downloads\trip-forecast-2026-09-24.json

  It stamps the file as the current version, writes it to trip.json, and pushes.
  Every visitor picks it up on their next load; anyone with local edits is told
  a new version arrived and can undo.
#>
param(
  [Parameter(Mandatory = $true)][string]$File,
  [switch]$NoPush
)
$ErrorActionPreference = 'Stop'
$repo = $PSScriptRoot

if (-not (Test-Path $File)) { throw "No such file: $File" }
$trip = Get-Content $File -Raw | ConvertFrom-Json
if (-not $trip.legs) { throw "$File has no 'legs' - is it an export from the app?" }

$trip | Add-Member -NotePropertyName published `
                   -NotePropertyValue (Get-Date).ToString('yyyy-MM-ddTHH:mm:ssK') -Force
$trip | ConvertTo-Json -Depth 10 | Set-Content (Join-Path $repo 'trip.json') -Encoding utf8

$stops = $trip.legs.Count
Write-Host "trip.json <- $stops stop$(if($stops -ne 1){'s'}), published $($trip.published)"

git -C $repo add trip.json
git -C $repo commit -q -m "Publish itinerary: $stops stop$(if($stops -ne 1){'s'})"
if (-not $NoPush) {
  git -C $repo push -q origin main
  Write-Host "Pushed. Live in ~30s at https://kmykytyn.github.io/multiweather/"
} else {
  Write-Host "Committed, not pushed (-NoPush)."
}
