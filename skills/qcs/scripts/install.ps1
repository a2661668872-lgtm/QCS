param(
    [string]$VaultRoot = ""
)

$ErrorActionPreference = "Stop"

$skillNames = @(
    "qcs",
    "qcs-positioning",
    "qcs-topic",
    "qcs-outline",
    "qcs-viewer-path",
    "qcs-structure",
    "qcs-language",
    "qcs-situation",
    "qcs-story",
    "qcs-visual",
    "qcs-cover",
    "qcs-conversion"
)

function Get-NormalizedPath {
    param([string]$Path)
    return [System.IO.Path]::GetFullPath($Path).TrimEnd("\")
}

if ([string]::IsNullOrWhiteSpace($VaultRoot)) {
    $skillRoot = Split-Path -Parent $PSScriptRoot
    $skillItem = Get-Item -LiteralPath $skillRoot -Force
    if ($skillItem.LinkType -eq "Junction" -and @($skillItem.Target).Count -gt 0) {
        $skillRoot = @($skillItem.Target)[0]
    }
    $skillsRoot = Split-Path -Parent $skillRoot
    $VaultRoot = Split-Path -Parent $skillsRoot
}

$resolvedVault = (Resolve-Path -LiteralPath $VaultRoot).Path
$sourceSkillsRoot = Join-Path $resolvedVault "skills"

# 先验证全部源目录，避免中途创建一半。
$sources = @{}
foreach ($name in $skillNames) {
    $source = Join-Path $sourceSkillsRoot $name
    $skillFile = Join-Path $source "SKILL.md"
    $metadataFile = Join-Path $source "agents\openai.yaml"
    if (-not (Test-Path -LiteralPath $skillFile)) {
        throw "找不到技能源文件：$skillFile"
    }
    if (-not (Test-Path -LiteralPath $metadataFile)) {
        throw "找不到 Skill 元数据：$metadataFile"
    }
    $sources[$name] = Get-NormalizedPath $source
}

$codexSkills = Join-Path $env:USERPROFILE ".codex\skills"
$conflicts = @()
$existingLinks = @()
$missingLinks = @()

foreach ($name in $skillNames) {
    $source = $sources[$name]
    $target = Join-Path $codexSkills $name
    $item = Get-Item -LiteralPath $target -Force -ErrorAction SilentlyContinue
    if ($null -eq $item) {
        $missingLinks += [PSCustomObject]@{ Name = $name; Source = $source; Target = $target }
        continue
    }

    $existingTarget = @($item.Target) | Select-Object -First 1
    $isCorrect = $false
    if ($item.LinkType -eq "Junction" -and -not [string]::IsNullOrWhiteSpace($existingTarget)) {
        $normalizedExisting = Get-NormalizedPath $existingTarget
        $isCorrect = [string]::Equals($normalizedExisting, $source, [System.StringComparison]::OrdinalIgnoreCase)
    }

    if ($isCorrect) {
        $existingLinks += [PSCustomObject]@{ Name = $name; Source = $source; Target = $target }
    }
    else {
        $conflicts += "$target"
    }
}

if ($conflicts.Count -gt 0) {
    $details = $conflicts -join [Environment]::NewLine
    throw "以下目标已存在且不是指向当前 Vault 的正确 Junction。脚本不会覆盖或删除它们：$([Environment]::NewLine)$details"
}

if (-not (Test-Path -LiteralPath $codexSkills)) {
    New-Item -ItemType Directory -Path $codexSkills | Out-Null
}

foreach ($link in $existingLinks) {
    Write-Output "已安装，无需重复操作：$($link.Target) -> $($link.Source)"
}

foreach ($link in $missingLinks) {
    New-Item -ItemType Junction -Path $link.Target -Target $link.Source | Out-Null
    Write-Output "安装完成：$($link.Target) -> $($link.Source)"
}

Write-Output "QCS Skill 套件安装检查完成：总数=$($skillNames.Count)，已存在=$($existingLinks.Count)，新建=$($missingLinks.Count)。"
