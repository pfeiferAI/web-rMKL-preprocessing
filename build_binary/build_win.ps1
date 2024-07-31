# Build app for Windows with pyinstaller

# Check if output directory argument is provided
if (-not $args) {
    Write-Error "Error: Output directory argument is missing"
    exit 1
}

# Create dist and build folders in output directory
New-Item -ItemType Directory -Path "$args\dist" -Force
New-Item -ItemType Directory -Path "$args\build" -Force

# Run pyinstaller on winApp.spec
pyinstaller winApp.spec --distpath="$args\dist" --workpath="$args\build" --clean -y

# Check if pyinstaller ran successfully
if ($LASTEXITCODE -eq 0) {
    Write-Output "Pyinstaller ran successfully"
    exit 0
} else {
    Write-Error "Pyinstaller failed"
    exit 1
}