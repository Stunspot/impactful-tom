param(
    [string]$RepositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

Add-Type -AssemblyName System.Drawing

$sourcePath = Join-Path $RepositoryRoot 'plugins\impactful-tom\assets\founder-constraint-mark.png'
$outputRoot = Join-Path $RepositoryRoot 'docs\assets\images'

if (-not (Test-Path -LiteralPath $sourcePath -PathType Leaf)) {
    throw "Approved source mark not found: $sourcePath"
}

[void](New-Item -ItemType Directory -Force -Path $outputRoot)

function New-BrushColor {
    param(
        [Parameter(Mandatory = $true)][string]$Hex,
        [int]$Alpha = 255
    )

    $normalized = $Hex.TrimStart('#')
    if ($normalized.Length -ne 6) {
        throw "Expected a six-digit hex color, received '$Hex'."
    }

    return [System.Drawing.Color]::FromArgb(
        $Alpha,
        [Convert]::ToInt32($normalized.Substring(0, 2), 16),
        [Convert]::ToInt32($normalized.Substring(2, 2), 16),
        [Convert]::ToInt32($normalized.Substring(4, 2), 16)
    )
}

function New-Canvas {
    param(
        [Parameter(Mandatory = $true)][int]$Width,
        [Parameter(Mandatory = $true)][int]$Height
    )

    $bitmap = New-Object System.Drawing.Bitmap(
        $Width,
        $Height,
        [System.Drawing.Imaging.PixelFormat]::Format32bppArgb
    )
    $bitmap.SetResolution(96, 96)
    return $bitmap
}

function Set-Quality {
    param(
        [Parameter(Mandatory = $true)][System.Drawing.Graphics]$Graphics
    )

    $Graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $Graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $Graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $Graphics.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
    $Graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
}

function Paint-Field {
    param(
        [Parameter(Mandatory = $true)][System.Drawing.Graphics]$Graphics,
        [Parameter(Mandatory = $true)][int]$Width,
        [Parameter(Mandatory = $true)][int]$Height
    )

    $bounds = New-Object System.Drawing.Rectangle(0, 0, $Width, $Height)
    $gradient = New-Object System.Drawing.Drawing2D.LinearGradientBrush(
        $bounds,
        (New-BrushColor '#040C2E'),
        (New-BrushColor '#02071D'),
        16
    )
    try {
        $Graphics.FillRectangle($gradient, $bounds)
    }
    finally {
        $gradient.Dispose()
    }

    $cyanPen = New-Object System.Drawing.Pen((New-BrushColor '#03BFFC' 24), 1)
    $goldPen = New-Object System.Drawing.Pen((New-BrushColor '#FDB707' 32), 1)
    try {
        for ($x = 0; $x -le $Width; $x += 80) {
            $Graphics.DrawLine($cyanPen, $x, 0, $x, $Height)
        }
        for ($y = 0; $y -le $Height; $y += 80) {
            $Graphics.DrawLine($cyanPen, 0, $y, $Width, $y)
        }
        $Graphics.DrawEllipse(
            $goldPen,
            [int]($Width * 0.73),
            [int](-$Height * 0.35),
            [int]($Height * 1.15),
            [int]($Height * 1.15)
        )
    }
    finally {
        $cyanPen.Dispose()
        $goldPen.Dispose()
    }
}

function Draw-SourceMark {
    param(
        [Parameter(Mandatory = $true)][System.Drawing.Graphics]$Graphics,
        [Parameter(Mandatory = $true)][System.Drawing.Image]$Source,
        [Parameter(Mandatory = $true)][System.Drawing.Rectangle]$Destination
    )

    $sourceCrop = New-Object System.Drawing.Rectangle(238, 242, 780, 780)
    $Graphics.DrawImage(
        $Source,
        $Destination,
        $sourceCrop.X,
        $sourceCrop.Y,
        $sourceCrop.Width,
        $sourceCrop.Height,
        [System.Drawing.GraphicsUnit]::Pixel
    )
}

function Save-Png {
    param(
        [Parameter(Mandatory = $true)][System.Drawing.Bitmap]$Bitmap,
        [Parameter(Mandatory = $true)][string]$Name
    )

    $path = Join-Path $outputRoot $Name
    $Bitmap.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
    return $path
}

function New-MarkDerivative {
    param(
        [Parameter(Mandatory = $true)][System.Drawing.Image]$Source,
        [Parameter(Mandatory = $true)][int]$Size,
        [Parameter(Mandatory = $true)][string]$Name
    )

    $bitmap = New-Canvas -Width $Size -Height $Size
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    try {
        Set-Quality -Graphics $graphics
        $graphics.Clear((New-BrushColor '#040C2E'))
        $destination = New-Object System.Drawing.Rectangle(0, 0, $Size, $Size)
        Draw-SourceMark -Graphics $graphics -Source $Source -Destination $destination
        return Save-Png -Bitmap $bitmap -Name $Name
    }
    finally {
        $graphics.Dispose()
        $bitmap.Dispose()
    }
}

function New-ReadmeHeader {
    param(
        [Parameter(Mandatory = $true)][System.Drawing.Image]$Source
    )

    $bitmap = New-Canvas -Width 1600 -Height 500
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $titleFont = New-Object System.Drawing.Font('Segoe UI', 62, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
    $subtitleFont = New-Object System.Drawing.Font('Segoe UI', 30, [System.Drawing.FontStyle]::Regular, [System.Drawing.GraphicsUnit]::Pixel)
    $statementFont = New-Object System.Drawing.Font('Segoe UI', 25, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
    $metaFont = New-Object System.Drawing.Font('Segoe UI', 17, [System.Drawing.FontStyle]::Regular, [System.Drawing.GraphicsUnit]::Pixel)
    $white = New-Object System.Drawing.SolidBrush((New-BrushColor '#F4F7FF'))
    $muted = New-Object System.Drawing.SolidBrush((New-BrushColor '#B9C6E2'))
    $cyan = New-Object System.Drawing.SolidBrush((New-BrushColor '#03BFFC'))
    $gold = New-Object System.Drawing.SolidBrush((New-BrushColor '#FDB707'))
    try {
        Set-Quality -Graphics $graphics
        Paint-Field -Graphics $graphics -Width 1600 -Height 500

        $graphics.FillRectangle($gold, 108, 82, 72, 7)
        $graphics.DrawString('IMPACTFUL TOM', $titleFont, $white, 106, 104)
        $graphics.DrawString('Founder-performance judgment', $subtitleFont, $cyan, 110, 188)
        $graphics.DrawString('Name the real constraint.', $statementFont, $white, 110, 266)
        $graphics.DrawString('Choose the owned move.', $statementFont, $white, 110, 302)
        $graphics.DrawString('Independent | Unofficial | Evidence-calibrated', $metaFont, $muted, 110, 386)

        $markDestination = New-Object System.Drawing.Rectangle(1080, 42, 416, 416)
        Draw-SourceMark -Graphics $graphics -Source $Source -Destination $markDestination
        return Save-Png -Bitmap $bitmap -Name 'impactful-tom-header.png'
    }
    finally {
        $titleFont.Dispose()
        $subtitleFont.Dispose()
        $statementFont.Dispose()
        $metaFont.Dispose()
        $white.Dispose()
        $muted.Dispose()
        $cyan.Dispose()
        $gold.Dispose()
        $graphics.Dispose()
        $bitmap.Dispose()
    }
}

function New-SocialCard {
    param(
        [Parameter(Mandatory = $true)][System.Drawing.Image]$Source
    )

    $bitmap = New-Canvas -Width 1280 -Height 640
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $titleFont = New-Object System.Drawing.Font('Segoe UI', 66, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
    $subtitleFont = New-Object System.Drawing.Font('Segoe UI', 31, [System.Drawing.FontStyle]::Regular, [System.Drawing.GraphicsUnit]::Pixel)
    $statementFont = New-Object System.Drawing.Font('Segoe UI', 24, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
    $metaFont = New-Object System.Drawing.Font('Segoe UI', 18, [System.Drawing.FontStyle]::Regular, [System.Drawing.GraphicsUnit]::Pixel)
    $white = New-Object System.Drawing.SolidBrush((New-BrushColor '#F4F7FF'))
    $muted = New-Object System.Drawing.SolidBrush((New-BrushColor '#B9C6E2'))
    $cyan = New-Object System.Drawing.SolidBrush((New-BrushColor '#03BFFC'))
    $gold = New-Object System.Drawing.SolidBrush((New-BrushColor '#FDB707'))
    try {
        Set-Quality -Graphics $graphics
        Paint-Field -Graphics $graphics -Width 1280 -Height 640

        $graphics.FillRectangle($gold, 86, 120, 72, 8)
        $graphics.DrawString('IMPACTFUL TOM', $titleFont, $white, 84, 151)
        $graphics.DrawString('Founder-performance judgment', $subtitleFont, $cyan, 88, 244)
        $graphics.DrawString('Find the constraint. Choose the move.', $statementFont, $white, 88, 333)
        $graphics.DrawString('Independent | Unofficial', $metaFont, $muted, 88, 500)

        $markDestination = New-Object System.Drawing.Rectangle(802, 92, 432, 432)
        Draw-SourceMark -Graphics $graphics -Source $Source -Destination $markDestination
        return Save-Png -Bitmap $bitmap -Name 'impactful-tom-social-card.png'
    }
    finally {
        $titleFont.Dispose()
        $subtitleFont.Dispose()
        $statementFont.Dispose()
        $metaFont.Dispose()
        $white.Dispose()
        $muted.Dispose()
        $cyan.Dispose()
        $gold.Dispose()
        $graphics.Dispose()
        $bitmap.Dispose()
    }
}

$sourceImage = [System.Drawing.Image]::FromFile($sourcePath)
try {
    $outputs = @()
    $outputs += New-MarkDerivative -Source $sourceImage -Size 512 -Name 'impactful-tom-mark-512.png'
    $outputs += New-MarkDerivative -Source $sourceImage -Size 192 -Name 'impactful-tom-mark-192.png'
    $outputs += New-MarkDerivative -Source $sourceImage -Size 180 -Name 'apple-touch-icon.png'
    $outputs += New-MarkDerivative -Source $sourceImage -Size 48 -Name 'favicon-48.png'
    $outputs += New-MarkDerivative -Source $sourceImage -Size 32 -Name 'favicon-32.png'
    $outputs += New-MarkDerivative -Source $sourceImage -Size 16 -Name 'favicon-16.png'
    $outputs += New-ReadmeHeader -Source $sourceImage
    $outputs += New-SocialCard -Source $sourceImage
}
finally {
    $sourceImage.Dispose()
}

$sourceHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $sourcePath).Hash.ToLowerInvariant()
$receipts = @()
foreach ($output in $outputs) {
    $item = Get-Item -LiteralPath $output
    $image = [System.Drawing.Image]::FromFile($output)
    try {
        $receipts += [ordered]@{
            path = $item.FullName.Substring($RepositoryRoot.Length + 1).Replace('\', '/')
            width = $image.Width
            height = $image.Height
            bytes = $item.Length
            sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $output).Hash.ToLowerInvariant()
        }
    }
    finally {
        $image.Dispose()
    }
}

[ordered]@{
    source = [ordered]@{
        path = $sourcePath.Substring($RepositoryRoot.Length + 1).Replace('\', '/')
        sha256 = $sourceHash
    }
    outputs = $receipts
} | ConvertTo-Json -Depth 5
