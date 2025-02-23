# startup.sh - Main startup script for Django
#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Function to check if PowerShell script exists
check_powershell_script() {
    PS_SCRIPT="${SCRIPT_DIR}/setup-wsl-forwarding.ps1"
    if [ ! -f "$PS_SCRIPT" ]; then
        echo "Creating PowerShell port forwarding script..."
        cat > "$PS_SCRIPT" << 'EOL'
# Script to automate port forwarding from Windows to WSL
function Get-WslIpAddress {
    $wslIp = bash -c "ip addr show eth0 | grep 'inet ' | cut -d ' ' -f 6 | cut -d '/' -f 1"
    return $wslIp.Trim()
}

# Get the WSL IP address
$wslIp = Get-WslIpAddress
if (-not $wslIp) {
    Write-Host "Could not detect WSL IP address. Please ensure WSL is running." -ForegroundColor Red
    exit 1
}

# Remove existing port forwarding
netsh interface portproxy delete v4tov4 listenport=8000 listenaddress=0.0.0.0

# Add new port forwarding
netsh interface portproxy add v4tov4 listenport=8000 listenaddress=0.0.0.0 connectport=8000 connectaddress=$wslIp

Write-Host "Port forwarding configured: Windows 8000 -> WSL ${wslIp}:8000" -ForegroundColor Green
EOL
    fi
}

# Function to setup port forwarding
setup_port_forwarding() {
    echo "Setting up port forwarding..."
    # Convert the path to Windows format
    WINDOWS_PATH=$(wslpath -w "${SCRIPT_DIR}/setup-wsl-forwarding.ps1")
    # Run PowerShell script with elevated privileges using Windows Terminal
    powershell.exe -Command "Start-Process powershell -Verb RunAs -ArgumentList '-ExecutionPolicy Bypass -File \"$WINDOWS_PATH\"'" 
}

# Main execution
echo "Starting Django development environment..."

# Ensure PowerShell script exists
check_powershell_script

# Setup port forwarding
setup_port_forwarding

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Start Django development server
echo "Starting Django development server..."
python3 manage.py runserver 0.0.0.0:8000