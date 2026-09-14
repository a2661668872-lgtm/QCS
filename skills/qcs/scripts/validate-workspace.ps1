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
$skillsRoot = Join-Path $resolvedVault "skills"
$codexSkills = Join-Path $env:USERPROFILE ".codex\skills"
$errors = @()

$requiredVaultFiles = @(
    "AGENTS.md",
    "00_个人背景\定位总览_v0.1.md",
    "00_个人背景\创作方法升级_从改稿执行到编导系统_v0.1.md",
    "04_选题库\选题池.md",
    "07_AI编导系统\AI编导总纲.md",
    "07_AI编导系统\当前导演规则.md",
    "07_AI编导系统\指标与内容目标字典.md",
    "07_AI编导系统\实验假设池.md",
    "07_AI编导系统\规则升级日志.md",
    "07_AI编导系统\模板\单条编导卡模板.md",
    "07_AI编导系统\模板\发布复盘模板.md",
    "01_学习对象\安先生\5.0课程逐字稿目录.md",
    "01_学习对象\安先生\5.0课程逐字稿校订\_校订索引.md",
    "01_学习对象\安先生\5.0课程逐字稿校订\核心方法校订_v0.1.md",
    ".cheat-state.json"
)

foreach ($relative in $requiredVaultFiles) {
    if (-not (Test-Path -LiteralPath (Join-Path $resolvedVault $relative))) {
        $errors += "缺少工作区文件：$relative"
    }
}

$sharedReferences = @(
    "qcs\references\router.md",
    "qcs\references\shared-contract.md",
    "qcs\references\course-map.md",
    "qcs\references\director-card-schema.md",
    "qcs\references\metrics-and-diagnosis.md",
    "qcs\references\upgrade-protocol.md"
)
foreach ($relative in $sharedReferences) {
    if (-not (Test-Path -LiteralPath (Join-Path $skillsRoot $relative))) {
        $errors += "缺少共享参考：skills\$relative"
    }
}

foreach ($name in $skillNames) {
    $source = Join-Path $skillsRoot $name
    $skillFile = Join-Path $source "SKILL.md"
    $metadataFile = Join-Path $source "agents\openai.yaml"

    if (-not (Test-Path -LiteralPath $skillFile)) {
        $errors += "缺少 Skill：skills\$name\SKILL.md"
    }
    else {
        $skillText = Get-Content -LiteralPath $skillFile -Raw -Encoding UTF8
        $namePattern = "(?m)^name:\s*" + [regex]::Escape($name) + "\s*$"
        if ($skillText -notmatch $namePattern) {
            $errors += "frontmatter 名称与目录不一致：$name"
        }
    }

    if (-not (Test-Path -LiteralPath $metadataFile)) {
        $errors += "缺少元数据：skills\$name\agents\openai.yaml"
    }
    else {
        $metadataText = Get-Content -LiteralPath $metadataFile -Raw -Encoding UTF8
        $requiredInvocation = '$' + $name
        if (-not $metadataText.Contains($requiredInvocation)) {
            $errors += "default_prompt 未显式包含 $requiredInvocation：$name"
        }
    }

    $target = Join-Path $codexSkills $name
    $item = Get-Item -LiteralPath $target -Force -ErrorAction SilentlyContinue
    if ($null -eq $item) {
        $errors += "用户级 Skill 未安装：$target"
    }
    elseif ($item.LinkType -ne "Junction") {
        $errors += "用户级目标不是 Junction：$target"
    }
    else {
        $existingTarget = @($item.Target) | Select-Object -First 1
        if ([string]::IsNullOrWhiteSpace($existingTarget)) {
            $errors += "Junction 缺少目标：$target"
        }
        else {
            $expected = Get-NormalizedPath $source
            $actual = Get-NormalizedPath $existingTarget
            if (-not [string]::Equals($actual, $expected, [System.StringComparison]::OrdinalIgnoreCase)) {
                $errors += "Junction 指向错误：$target -> $actual；应为 $expected"
            }
        }
    }
}

$courseMapPath = Join-Path $skillsRoot "qcs\references\course-map.md"
if (Test-Path -LiteralPath $courseMapPath) {
    $courseMap = Get-Content -LiteralPath $courseMapPath -Raw -Encoding UTF8
    for ($number = 1; $number -le 38; $number++) {
        $id = "{0:D3}" -f $number
        $pattern = "(?m)^\|\s*" + $id + "\s*\|"
        $matches = [regex]::Matches($courseMap, $pattern).Count
        if ($matches -ne 1) {
            $errors += "课程映射 $id 应出现一次，实际出现 $matches 次"
        }
    }
}

$evalPath = Join-Path $skillsRoot "qcs\evals\evals.json"
if (-not (Test-Path -LiteralPath $evalPath)) {
    $errors += "缺少路由评测：skills\qcs\evals\evals.json"
}
else {
    try {
        Get-Content -LiteralPath $evalPath -Raw -Encoding UTF8 | ConvertFrom-Json | Out-Null
    }
    catch {
        $errors += "路由评测 JSON 无效：$($_.Exception.Message)"
    }
}

$resultRoot = Join-Path $skillsRoot "qcs\evals\results"
if (Test-Path -LiteralPath $resultRoot) {
    foreach ($resultFile in Get-ChildItem -LiteralPath $resultRoot -File -Filter "*.json") {
        try {
            Get-Content -LiteralPath $resultFile.FullName -Raw -Encoding UTF8 | ConvertFrom-Json | Out-Null
        }
        catch {
            $errors += "评测结果 JSON 无效：$($resultFile.Name)：$($_.Exception.Message)"
        }
    }
}

$statePath = Join-Path $resolvedVault ".cheat-state.json"
$stateSummary = "unavailable"
if (Test-Path -LiteralPath $statePath) {
    try {
        $state = Get-Content -LiteralPath $statePath -Raw -Encoding UTF8 | ConvertFrom-Json
        $stateSummary = "rubric=$($state.rubric_version); calibration_samples=$($state.calibration_samples); benchmark=$($state.benchmark_status)"
    }
    catch {
        $errors += ".cheat-state.json 无法解析：$($_.Exception.Message)"
    }
}

Write-Output "Vault: $resolvedVault"
Write-Output "Data state: $stateSummary"
Write-Output "Skills checked: $($skillNames.Count)"
Write-Output "Course mappings checked: 38"
Write-Output "Errors: $($errors.Count)"

if ($errors.Count -gt 0) {
    $errors | ForEach-Object { Write-Output "ERROR: $_" }
    exit 1
}

Write-Output "QCS 模块化 Skill 套件验证通过。"
