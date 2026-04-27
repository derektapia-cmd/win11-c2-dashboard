[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

$repoRoot = (& git rev-parse --show-toplevel).Trim()
Push-Location $repoRoot

try {
    $trackedFiles = & git ls-files
    $patterns = @(
        @{
            Name = "Private key block"
            Regex = "-----BEGIN [A-Z ]*PRIVATE KEY-----"
        },
        @{
            Name = "OpenAI API key"
            Regex = "sk-[A-Za-z0-9_-]{20,}"
        },
        @{
            Name = "GitHub token"
            Regex = "gh[pousr]_[A-Za-z0-9_]{36,}"
        },
        @{
            Name = "AWS access key"
            Regex = "AKIA[0-9A-Z]{16}"
        },
        @{
            Name = "Google API key"
            Regex = "AIza[0-9A-Za-z_-]{35}"
        },
        @{
            Name = "Slack token"
            Regex = "xox[baprs]-[0-9A-Za-z-]{10,}"
        },
        @{
            Name = "JWT"
            Regex = "eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"
        },
        @{
            Name = "Secret assignment"
            Regex = "(?i)\b(api[_-]?key|secret|token|password|private[_-]?key)\b\s*[:=]\s*[""']?([A-Za-z0-9_./+=-]{12,})[""']?"
        }
    )
    $allowedLinePatterns = @(
        "^\s*#",
        "(?i)(example|placeholder|changeme|your_|_here)",
        "^\s*(OPENAI_API_KEY|WEATHER_API_KEY|COINGECKO_API_KEY|GMAIL_CLIENT_ID|GMAIL_CLIENT_SECRET|X_CLIENT_ID|X_CLIENT_SECRET)\s*=\s*$"
    )
    $binaryExtensions = @(
        ".ico", ".jpg", ".jpeg", ".png", ".gif", ".webp", ".pdf", ".zip", ".gz",
        ".sqlite3", ".db", ".exe", ".dll"
    )
    $findings = @()

    foreach ($file in $trackedFiles) {
        $extension = [System.IO.Path]::GetExtension($file).ToLowerInvariant()

        if ($binaryExtensions -contains $extension) {
            continue
        }

        if (-not (Test-Path -LiteralPath $file)) {
            continue
        }

        $lines = Get-Content -LiteralPath $file -ErrorAction Stop

        for ($index = 0; $index -lt $lines.Count; $index += 1) {
            $line = $lines[$index]
            $isAllowed = $false

            foreach ($allowedLinePattern in $allowedLinePatterns) {
                if ($line -match $allowedLinePattern) {
                    $isAllowed = $true
                    break
                }
            }

            if ($isAllowed) {
                continue
            }

            foreach ($pattern in $patterns) {
                if ($line -match $pattern.Regex) {
                    $findings += [PSCustomObject]@{
                        File = $file
                        Line = $index + 1
                        Rule = $pattern.Name
                    }
                }
            }
        }
    }

    if ($findings.Count -gt 0) {
        Write-Host "Potential committed secrets found:" -ForegroundColor Red
        $findings | Format-Table -AutoSize | Out-String | Write-Host
        exit 1
    }

    Write-Host "No committed secrets found across $($trackedFiles.Count) tracked files."
}
finally {
    Pop-Location
}
