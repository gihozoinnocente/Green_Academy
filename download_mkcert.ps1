$url = "https://github.com/FiloSottile/mkcert/releases/download/v1.4.4/mkcert-v1.4.4-windows-amd64.exe"
$output = "mkcert.exe"
Invoke-WebRequest -Uri $url -OutFile $output
Write-Host "mkcert downloaded successfully!"
