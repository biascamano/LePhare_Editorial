<#
.SYNOPSIS
  Construit le POC Le Phare 2.0 et le publie par SFTP (WinSCP) sur l'hébergement OVH Perso, dans un dossier dédié.

.DESCRIPTION
  Sans option : SIMULATION. Build, contrôles et préparation du lot, sans aucune connexion.
  -VerifierDistant  Connexion SFTP en lecture seule : périmètre, marqueur, aperçu des transferts.
  -Executer         Transfert réel. Exige -Confirmer <dossier>, plus -Initialiser au premier déploiement.
  -Restaurer <dir>  Republie une sauvegarde de .deploy\sauvegardes (simulation sans -Executer).
  -VerifierHttps    Contrôles HTTPS en GET (auth, noindex, redirection, site principal intact).
  -EnregistrerIdentifiants / -CreerAccesHttp : stockage chiffré (DPAPI) hors dépôt.

  Aucun fichier distant n'est jamais supprimé. Aucun mot de passe n'est lu depuis le dépôt ni écrit dans les journaux.
#>
[CmdletBinding()]
param(
  [switch]$VerifierDistant,
  [switch]$Executer,
  [switch]$Initialiser,
  [string]$Confirmer,
  [string]$Restaurer,
  [switch]$VerifierHttps,
  [switch]$SansBuild,
  [switch]$SansAuthentification,
  [ValidateSet('mock', 'wordpress')][string]$Source,
  [switch]$JournalWinSCP,
  [switch]$EnregistrerIdentifiants,
  [switch]$CreerAccesHttp
)

Set-StrictMode -Version 3
$ErrorActionPreference = 'Stop'

$PocDir     = Split-Path $PSScriptRoot -Parent
$DeployDir  = Join-Path $PocDir '.deploy'
$SecretsDir = Join-Path $env:APPDATA 'LePhare-POC'
$Dist       = Join-Path $PocDir 'dist'
$Lot        = Join-Path $DeployDir 'lot'
$Sauvegardes = Join-Path $DeployDir 'sauvegardes'
$MarkerName = '.phare-poc-marker'
$MarkerId   = 'le-phare-2.0-poc'
$Horodatage = Get-Date -Format 'yyyyMMdd-HHmmss'
$DossiersInterdits = @('www', 'public_html', 'htdocs', 'wordpress', 'wp', 'cgi-bin', 'private', 'logs', 'ovhconfig', '.', '..')
$SignaturesWordPress = @('wp-config.php', 'wp-content', 'wp-admin', 'wp-includes', 'wp-login.php', 'xmlrpc.php')
$ExtensionsAutorisees = @('.html', '.css', '.js', '.svg', '.png', '.jpg', '.jpeg', '.webp', '.avif', '.gif', '.ico', '.txt', '.woff2', '.xml', '.webmanifest')
$FichiersTechniques = @('.htaccess', '.htpasswd', $MarkerName)
$MotifsInterdits = @('\.env', '\.local\.json$', '\.cred', '\.ps1$', '\.mjs$', '\.ts$', '\.md$', '\.astro$', '^package(-lock)?\.json$', 'node_modules', '(^|[\\/])\.git([\\/]|$)', '\.map$', 'wp-config')

New-Item -ItemType Directory -Force -Path (Join-Path $DeployDir 'logs') | Out-Null
$LogFile = Join-Path $DeployDir "logs\deploy-$Horodatage.log"
$Echecs = New-Object System.Collections.Generic.List[string]

function Log([string]$Message, [string]$Niveau = 'INFO') {
  $ligne = '{0} [{1}] {2}' -f (Get-Date -Format 'HH:mm:ss'), $Niveau, $Message
  $couleur = @{ INFO = 'Gray'; OK = 'Green'; ATTENTION = 'Yellow'; ERREUR = 'Red'; ETAPE = 'Cyan' }[$Niveau]
  Write-Host $ligne -ForegroundColor $couleur
  Add-Content -Path $LogFile -Value $ligne -Encoding UTF8
}
function Arreter([string]$Message) { Log $Message 'ERREUR'; throw "ARRET : $Message" }
function Masquer([string]$v) { if (-not $v) { return '(vide)' }; if ($v.Length -le 3) { return '***' }; return $v.Substring(0, 2) + '***' }
function Ecrire-Texte([string]$Chemin, [string]$Texte) {
  [IO.File]::WriteAllText($Chemin, ($Texte -replace "`r`n", "`n"), (New-Object Text.UTF8Encoding $false))
}
function Interactif { try { return -not [Console]::IsInputRedirected } catch { return $false } }

# --- Configuration : variables d'environnement > .env.deploy (non versionné) > défaut ---
$FichierConfig = @{}
$cheminEnv = Join-Path $PocDir '.env.deploy'
if (Test-Path $cheminEnv) {
  foreach ($l in Get-Content $cheminEnv -Encoding UTF8) {
    if ($l -match '^\s*([A-Z0-9_]+)\s*=\s*(.*?)\s*$') { $FichierConfig[$Matches[1]] = $Matches[2].Trim('"', "'") }
  }
  $secrets = @($FichierConfig.Keys | Where-Object { $_ -match 'PASSWORD|PASSWD_PLAIN|SECRET|MOT_DE_PASSE|TOKEN' })
  if ($secrets.Count) { Log ".env.deploy contient une clé de secret ($($secrets -join ', ')) : les mots de passe ne vont jamais dans un fichier du dépôt." 'ERREUR'; exit 1 }
}
function Cfg([string]$Nom, [string]$Defaut = '') {
  $v = [Environment]::GetEnvironmentVariable($Nom)
  if ($v) { return $v }
  if ($FichierConfig.ContainsKey($Nom) -and $FichierConfig[$Nom]) { return $FichierConfig[$Nom] }
  return $Defaut
}

$C = [ordered]@{
  Hote       = Cfg 'OVH_SFTP_HOST'
  Port       = [int](Cfg 'OVH_SFTP_PORT' '22')
  Utilisateur = Cfg 'OVH_SFTP_USER'
  CleHote    = Cfg 'OVH_SFTP_HOSTKEY'
  Dossier    = Cfg 'OVH_REMOTE_DIR' 'poc-phare-2'
  Site       = (Cfg 'PHARE_SITE' 'https://test.le-phare.info').TrimEnd('/')
  HomeAbs    = Cfg 'OVH_HOME_ABS'
  Htpasswd   = Cfg 'OVH_HTPASSWD_FILE' (Join-Path $SecretsDir 'htpasswd')
  WinSCPDir  = Cfg 'WINSCP_DIR'
}
if (-not $Source) { $Source = Cfg 'PHARE_SOURCE' 'mock' }
$SiteHote = ([Uri]$C.Site).Host

# --- Utilitaires de secrets (hors dépôt, DPAPI : lisibles par ce seul compte Windows sur cette machine) ---
if ($EnregistrerIdentifiants -or $CreerAccesHttp) {
  New-Item -ItemType Directory -Force -Path $SecretsDir | Out-Null
  if ($EnregistrerIdentifiants) {
    $cred = Get-Credential -Message 'Identifiant et mot de passe SFTP OVH' -UserName $C.Utilisateur
    $cred | Export-Clixml -Path (Join-Path $SecretsDir 'sftp.xml')
    Log "Identifiants SFTP chiffrés dans $SecretsDir\sftp.xml (utilisateur $(Masquer $cred.UserName))." 'OK'
  }
  if ($CreerAccesHttp) {
    $openssl = (Get-Command openssl -ErrorAction SilentlyContinue)
    if ($openssl) { $openssl = $openssl.Source }
    else { foreach ($p in @("$env:ProgramFiles\Git\usr\bin\openssl.exe", "$env:ProgramFiles\Git\mingw64\bin\openssl.exe")) { if (Test-Path $p) { $openssl = $p } } }
    if (-not $openssl) { Arreter 'openssl introuvable (fourni avec Git for Windows) : impossible de hacher le mot de passe HTTP.' }
    $cred = Get-Credential -Message 'Accès HTTP au POC (identifiant à choisir, mot de passe distinct du SFTP)'
    if ($cred.UserName -match '[:\s]') { Arreter "L'identifiant HTTP ne doit contenir ni espace ni « : »." }
    $clair = $cred.GetNetworkCredential().Password
    if ($clair.Length -lt 12) { Arreter 'Mot de passe HTTP trop court (12 caractères minimum).' }
    $hash = ($clair | & $openssl passwd -apr1 -stdin)
    $clair = $null
    if ($LASTEXITCODE -ne 0 -or $hash -notmatch '^\$apr1\$') { Arreter 'Échec du hachage apr1 par openssl.' }
    Ecrire-Texte $C.Htpasswd ("{0}:{1}`n" -f $cred.UserName, $hash)
    $cred | Export-Clixml -Path (Join-Path $SecretsDir 'http.xml')
    Log "Fichier htpasswd écrit dans $($C.Htpasswd) ; accès HTTP chiffré dans $SecretsDir\http.xml." 'OK'
  }
  exit 0
}

# --- Validation de la configuration ---
function Valider-Config([bool]$Distant) {
  Log 'Configuration' 'ETAPE'
  Log ("  Hôte SFTP      : {0}" -f $(if ($C.Hote) { $C.Hote } else { '(à renseigner : OVH_SFTP_HOST)' }))
  Log ("  Port           : {0}" -f $C.Port)
  Log ("  Utilisateur    : {0}" -f $(if ($C.Utilisateur) { Masquer $C.Utilisateur } else { '(à renseigner : OVH_SFTP_USER)' }))
  Log ("  Clé d'hôte     : {0}" -f $(if ($C.CleHote) { $C.CleHote } else { '(à renseigner : OVH_SFTP_HOSTKEY)' }))
  Log ("  Dossier distant: {0}" -f $C.Dossier)
  Log ("  Site           : {0}" -f $C.Site)
  Log ("  Source         : {0}" -f $Source)

  if ($C.Dossier -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$') { Arreter "OVH_REMOTE_DIR doit être un seul nom de dossier (lettres, chiffres, . _ -), sans / ni .. : « $($C.Dossier) »." }
  if ($DossiersInterdits -contains $C.Dossier.ToLowerInvariant()) { Arreter "Dossier distant interdit : « $($C.Dossier) » (racine WordPress ou dossier système)." }
  if ($C.Site -notmatch '^https://[a-z0-9.-]+$') { Arreter "PHARE_SITE doit être une origine HTTPS sans chemin : « $($C.Site) »." }
  if (@('le-phare.info', 'www.le-phare.info') -contains $SiteHote) { Arreter "PHARE_SITE vise le site de production ($SiteHote) : interdit pour le POC." }
  if ($C.CleHote -and ($C.CleHote -match '\*' -or $C.CleHote -notmatch '^(ssh-ed25519|ecdsa-sha2-nistp(256|384|521)|ssh-rsa) \d+ [A-Za-z0-9+/=:]+$')) {
    Arreter "OVH_SFTP_HOSTKEY invalide : format attendu « ssh-ed25519 255 <empreinte SHA-256> ». Aucune acceptation automatique de clé n'est permise."
  }
  $manquants = @(); foreach ($k in 'Hote', 'Utilisateur', 'CleHote') { if (-not $C[$k]) { $manquants += $k } }
  if ($manquants.Count) {
    if ($Distant) { Arreter "Paramètres SFTP manquants : $($manquants -join ', '). Voir .env.example." }
    Log "Paramètres SFTP encore inconnus ($($manquants -join ', ')) : sans effet en simulation." 'ATTENTION'
  }
}

# --- Build et contrôles locaux ---
function Executer-Natif([string]$Libelle, [string]$Fichier, [string[]]$Arguments) {
  $ancien = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
  try { $sortie = & $Fichier @Arguments 2>&1 | ForEach-Object { "$_" } } finally { $ErrorActionPreference = $ancien }
  $code = $LASTEXITCODE
  $sortie | Add-Content -Path $LogFile -Encoding UTF8
  if ($code -ne 0) { $sortie | Select-Object -Last 25 | ForEach-Object { Write-Host "    $_" }; Arreter "$Libelle en échec (code $code), détail dans $LogFile." }
  return $sortie
}

function Construire {
  Log "Build Astro (source $Source, site $($C.Site))" 'ETAPE'
  $sauve = @{}; foreach ($k in 'ASTRO_TELEMETRY_DISABLED', 'PHARE_SITE', 'PHARE_SOURCE') { $sauve[$k] = [Environment]::GetEnvironmentVariable($k) }
  try {
    $env:ASTRO_TELEMETRY_DISABLED = '1'; $env:PHARE_SITE = $C.Site; $env:PHARE_SOURCE = $Source
    Push-Location $PocDir
    $s = Executer-Natif 'Build Astro' 'npm.cmd' @('run', 'build', '--silent')
    ($s | Where-Object { $_ -match 'page\(s\) built' }) | ForEach-Object { Log ('  ' + ($_ -replace '\x1b\[[0-9;]*m', '').Trim()) }
    $v = Executer-Natif 'Contrôle verify-dist' 'node' @('scripts/verify-dist.mjs', 'dist')
    ($v | Select-Object -First 1) | ForEach-Object { Log "  $_" }
    Log '  verify-dist : aucune erreur.' 'OK'
  } finally {
    Pop-Location
    foreach ($k in $sauve.Keys) { [Environment]::SetEnvironmentVariable($k, $sauve[$k]) }
  }
}

function Contenu-Htaccess([string]$HomeAbs) {
  $t = Get-Content (Join-Path $PocDir 'deploy\htaccess.template') -Raw -Encoding UTF8
  if ($SansAuthentification) { $t = [regex]::Replace($t, '(?s)# AUTH-DEBUT.*?# AUTH-FIN\r?\n?', '') }
  $chemin = '{0}/{1}/.htpasswd' -f $HomeAbs.TrimEnd('/'), $C.Dossier
  return $t.Replace('{{SITE_HOST}}', $SiteHote).Replace('{{HTPASSWD}}', $chemin)
}

function Preparer-Lot {
  Log 'Préparation du lot (dist + fichiers web)' 'ETAPE'
  foreach ($f in 'index.html', '404.html', 'explorer\index.html', 'sentier\index.html') {
    if (-not (Test-Path (Join-Path $Dist $f))) { Arreter "Build incomplet : dist\$f absent." }
  }
  $plein = [IO.Path]::GetFullPath($Lot)
  if (-not $plein.StartsWith([IO.Path]::GetFullPath($DeployDir) + '\')) { Arreter 'Chemin du lot hors de .deploy : refus de nettoyer.' }
  if (Test-Path $Lot) { Remove-Item -Recurse -Force $Lot }
  New-Item -ItemType Directory -Path $Lot | Out-Null
  Copy-Item -Path (Join-Path $Dist '*') -Destination $Lot -Recurse

  $commit = (& git -C $PocDir rev-parse --short HEAD 2>$null); if (-not $commit) { $commit = 'inconnu' }
  $script:BuildId = "$Horodatage-$commit-$Source"
  Ecrire-Texte (Join-Path $Lot 'phare-version.txt') "$MarkerId`nbuild=$script:BuildId`n"
  Ecrire-Texte (Join-Path $Lot $MarkerName) "$MarkerId`nsite=$SiteHote`ndossier=$($C.Dossier)`n"
  Ecrire-Texte (Join-Path $Lot '.htaccess') (Contenu-Htaccess $(if ($C.HomeAbs) { $C.HomeAbs } else { '<HOME_OVH>' }))
  if (-not $SansAuthentification) {
    if (Test-Path $C.Htpasswd) { Copy-Item $C.Htpasswd (Join-Path $Lot '.htpasswd') }
    else { Log "Fichier htpasswd absent ($($C.Htpasswd)) : lancer -CreerAccesHttp avant tout transfert réel." 'ATTENTION' }
  }
  Controler-Lot $Lot
}

function Controler-Lot([string]$Dossier) {
  $fichiers = @(Get-ChildItem -Path $Dossier -Recurse -File -Force)
  $racine = [IO.Path]::GetFullPath($Dossier).TrimEnd('\') + '\'
  $refus = @()
  foreach ($f in $fichiers) {
    $rel = $f.FullName.Substring($racine.Length)
    if ($FichiersTechniques -contains $rel) { continue }
    if ($ExtensionsAutorisees -notcontains $f.Extension.ToLowerInvariant()) { $refus += "$rel (extension non autorisée)"; continue }
    foreach ($m in $MotifsInterdits) { if ($rel -match $m) { $refus += "$rel (motif interdit $m)"; break } }
    if ($f.Length -gt 10MB) { $refus += "$rel (plus de 10 Mo)" }
  }
  if ($refus.Count) { $refus | Select-Object -First 20 | ForEach-Object { Log "  refusé : $_" 'ERREUR' }; Arreter "$($refus.Count) fichier(s) ne doivent pas être publiés." }
  $total = ($fichiers | Measure-Object Length -Sum).Sum
  Log ('  {0} fichiers, {1:N1} Mo ; liste d''exclusion respectée.' -f $fichiers.Count, ($total / 1MB)) 'OK'
  $fichiers | Group-Object { if ($FichiersTechniques -contains $_.Name) { $_.Name } else { $_.Extension } } | Sort-Object Count -Descending |
    ForEach-Object { Log ('    {0,-18} {1}' -f $_.Name, $_.Count) }
  $fichiers | ForEach-Object { 'LOT ' + $_.FullName.Substring($racine.Length) } | Add-Content -Path $LogFile -Encoding UTF8
}

# --- SFTP (WinSCP .NET, lecture seule sauf dans Publier) ---
function Charger-WinSCP {
  $candidats = @($C.WinSCPDir, "${env:ProgramFiles(x86)}\WinSCP", "$env:ProgramFiles\WinSCP", "$env:LOCALAPPDATA\Programs\WinSCP") | Where-Object { $_ }
  foreach ($d in $candidats) {
    if ((Test-Path (Join-Path $d 'WinSCPnet.dll')) -and (Test-Path (Join-Path $d 'WinSCP.exe'))) {
      Add-Type -Path (Join-Path $d 'WinSCPnet.dll'); return $d
    }
  }
  Arreter "WinSCP (WinSCP.exe + WinSCPnet.dll) introuvable. Installer WinSCP ou définir WINSCP_DIR (voir DEPLOIEMENT_OVH.md §2)."
}

function Mot-De-Passe-SFTP {
  if ($env:OVH_SFTP_PASSWORD) { Log '  Mot de passe : variable OVH_SFTP_PASSWORD.'; return (ConvertTo-SecureString $env:OVH_SFTP_PASSWORD -AsPlainText -Force) }
  $f = Join-Path $SecretsDir 'sftp.xml'
  if (Test-Path $f) { Log '  Mot de passe : stockage chiffré DPAPI.'; return (Import-Clixml $f).Password }
  if (Interactif) { return (Read-Host -AsSecureString 'Mot de passe SFTP OVH') }
  Arreter 'Aucun mot de passe SFTP disponible : lancer -EnregistrerIdentifiants dans un terminal, ou définir OVH_SFTP_PASSWORD pour la session.'
}

function Ouvrir-Session {
  $dir = Charger-WinSCP
  $o = New-Object WinSCP.SessionOptions
  $o.Protocol = [WinSCP.Protocol]::Sftp
  $o.HostName = $C.Hote; $o.PortNumber = $C.Port; $o.UserName = $C.Utilisateur
  $o.SecurePassword = Mot-De-Passe-SFTP
  $o.SshHostKeyFingerprint = $C.CleHote
  $o.TimeoutInMilliseconds = 30000
  $s = New-Object WinSCP.Session
  $s.ExecutablePath = Join-Path $dir 'WinSCP.exe'
  if ($JournalWinSCP) { $s.SessionLogPath = Join-Path $DeployDir "logs\winscp-$Horodatage.log" }
  Log "Connexion SFTP à $($C.Hote):$($C.Port) (clé d'hôte vérifiée par WinSCP)" 'ETAPE'
  $s.Open($o)
  Log '  Connecté ; empreinte du serveur conforme.' 'OK'
  return $s
}

function Inspecter-Distant($s) {
  Log 'Inspection du périmètre distant (lecture seule)' 'ETAPE'
  $racineCompte = $s.HomePath
  $racine = @($s.ListDirectory($racineCompte).Files | Where-Object { $_.Name -ne '..' -and $_.Name -ne '.' } | ForEach-Object { $_.Name })
  Log "  Racine du compte : $racineCompte"
  Log "  Entrées : $($racine -join ', ')"
  if ($racine -notcontains 'www') { Log '  Pas de dossier www à la racine : vérifier que ce compte est bien celui de le-phare.info.' 'ATTENTION' }
  $cible = [WinSCP.RemotePath]::Combine($racineCompte, $C.Dossier)
  $etat = [ordered]@{ Home = $racineCompte; Cible = $cible; Statut = 'absent'; Entrees = @() }
  if ($s.FileExists($cible)) {
    $info = $s.GetFileInfo($cible)
    if (-not $info.IsDirectory) { Arreter "$cible existe mais n'est pas un dossier." }
    if ("$($info.FileType)" -eq 'L') { Arreter "$cible est un lien symbolique : refus (il pourrait viser la racine WordPress)." }
    $etat.Entrees = @($s.ListDirectory($cible).Files | Where-Object { $_.Name -ne '..' -and $_.Name -ne '.' } | ForEach-Object { $_.Name })
    $wp = @($etat.Entrees | Where-Object { $SignaturesWordPress -contains $_ })
    if ($wp.Count) { Arreter "Le dossier cible contient des fichiers WordPress ($($wp -join ', ')) : ce n'est pas le dossier du POC." }
    if ($etat.Entrees -contains $MarkerName) {
      $tmp = Join-Path $DeployDir 'tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null
      $s.GetFiles([WinSCP.RemotePath]::EscapeFileMask("$cible/$MarkerName"), "$tmp\*").Check()
      $m = @(Get-Content (Join-Path $tmp $MarkerName) -Encoding UTF8)
      Remove-Item -Force (Join-Path $tmp $MarkerName)
      if ($m.Count -lt 2 -or $m[0] -ne $MarkerId -or $m[1] -ne "site=$SiteHote") { Arreter "Marqueur présent mais étranger au POC ($($m -join ' | '))." }
      $etat.Statut = 'marque'
    } elseif ($etat.Entrees.Count -eq 0) { $etat.Statut = 'vide' }
    else { $etat.Statut = 'inconnu' }
  }
  $lib = @{ absent = 'absent (créé au premier déploiement avec -Initialiser)'; vide = 'vide, sans marqueur (premier déploiement : -Initialiser)'; marque = 'marqué POC : mises à jour autorisées'; inconnu = 'NON VIDE et sans marqueur : refus' }
  Log "  Dossier cible $cible : $($lib[$etat.Statut])" $(if ($etat.Statut -eq 'inconnu') { 'ERREUR' } else { 'OK' })
  if ($etat.Statut -eq 'inconnu') { Log "  Contenu : $($etat.Entrees -join ', ')"; Arreter 'Dossier cible non vide sans marqueur du POC : vider ou choisir un autre dossier à la main, après vérification.' }
  return $etat
}

function Apercu-Transferts($s, $etat, [string]$Local) {
  if ($etat.Statut -ne 'marque') { Log "  Aperçu : tout le lot serait envoyé (dossier $($etat.Statut))."; return }
  $diff = $s.CompareDirectories([WinSCP.SynchronizationMode]::Remote, $Local, $etat.Cible, $false, $true, [WinSCP.SynchronizationCriteria]::Time)
  $parAction = @($diff) | Group-Object { "$($_.Action)" }
  foreach ($g in $parAction) { Log ('  {0,-14} {1}' -f $g.Name, $g.Count) }
  @($diff) | ForEach-Object { 'DIFF ' + $_.Action + ' ' + $(if ($_.Local) { $_.Local.FileName } else { $_.Remote.FileName }) } | Add-Content -Path $LogFile -Encoding UTF8
  $racineLocale = [IO.Path]::GetFullPath($Local).TrimEnd('\') + '\'
  $locaux = @{}; Get-ChildItem $Local -Recurse -File -Force | ForEach-Object { $locaux[$_.FullName.Substring($racineLocale.Length).Replace('\', '/')] = $true }
  $orphelins = @($s.EnumerateRemoteFiles($etat.Cible, $null, [WinSCP.EnumerationOptions]::AllDirectories) |
    ForEach-Object { $_.FullName.Substring($etat.Cible.Length + 1) } | Where-Object { -not $locaux.ContainsKey($_) })
  if ($orphelins.Count) {
    Log "  $($orphelins.Count) fichier(s) distant(s) absents du lot : conservés (aucune suppression automatique). Liste dans le journal." 'ATTENTION'
    $orphelins | ForEach-Object { "ORPHELIN $_" } | Add-Content -Path $LogFile -Encoding UTF8
  }
}

function Sauvegarder($s, $etat) {
  $dest = Join-Path $Sauvegardes $Horodatage
  New-Item -ItemType Directory -Force -Path $dest | Out-Null
  Log "Sauvegarde de la version en ligne vers $dest" 'ETAPE'
  $o = New-Object WinSCP.TransferOptions; $o.TransferMode = [WinSCP.TransferMode]::Binary
  $s.GetFiles([WinSCP.RemotePath]::EscapeFileMask($etat.Cible) + '/*', "$dest\*", $false, $o).Check()
  if (-not (Test-Path (Join-Path $dest $MarkerName))) { Arreter 'Sauvegarde incomplète (marqueur absent) : transfert annulé.' }
  $n = @(Get-ChildItem $dest -Recurse -File -Force).Count
  Log "  $n fichiers sauvegardés." 'OK'
  return $dest
}

function Publier($s, $etat, [string]$Local) {
  $o = New-Object WinSCP.TransferOptions
  $o.TransferMode = [WinSCP.TransferMode]::Binary
  $o.PreserveTimestamp = $true
  if ($etat.Statut -eq 'absent') { Log "Création de $($etat.Cible)" 'ETAPE'; $s.CreateDirectory($etat.Cible) }
  Log 'Envoi des fichiers techniques en premier (marqueur, .htpasswd, .htaccess)' 'ETAPE'
  foreach ($t in $MarkerName, '.htpasswd', '.htaccess') {
    $p = Join-Path $Local $t
    if (Test-Path $p) { $s.PutFiles($p, $etat.Cible + '/', $false, $o).Check(); Log "  $t" 'OK' }
  }
  Log "Synchronisation vers $($etat.Cible) (ajouts et mises à jour, aucune suppression)" 'ETAPE'
  $r = $s.SynchronizeDirectories([WinSCP.SynchronizationMode]::Remote, $Local, $etat.Cible, $false, $true, [WinSCP.SynchronizationCriteria]::Time, $o)
  $r.Check()
  Log "  $(@($r.Uploads).Count) fichier(s) envoyés, 0 supprimé." 'OK'
  @($r.Uploads) | ForEach-Object { 'ENVOI ' + $_.FileName } | Add-Content -Path $LogFile -Encoding UTF8
}

# --- Vérification HTTPS (GET uniquement) ---
function Requete([string]$Url, $Cred) {
  $r = [Net.HttpWebRequest]::Create($Url)
  $r.Method = 'GET'; $r.AllowAutoRedirect = $false; $r.Timeout = 20000; $r.UserAgent = 'LePhare-POC-verif'
  if ($Cred) {
    $b = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($Cred.UserName + ':' + $Cred.GetNetworkCredential().Password))
    $r.Headers['Authorization'] = "Basic $b"
  }
  try { $rep = $r.GetResponse() } catch [Net.WebException] {
    if ($_.Exception.Response) { $rep = $_.Exception.Response } else { return @{ Code = 0; Erreur = $_.Exception.Message } }
  }
  $corps = ''; try { $corps = (New-Object IO.StreamReader($rep.GetResponseStream())).ReadToEnd() } catch {}
  $res = @{ Code = [int]$rep.StatusCode; Location = $rep.Headers['Location']; Robots = $rep.Headers['X-Robots-Tag']; Corps = $corps; Erreur = '' }
  $rep.Close(); return $res
}
function Attendre([string]$Libelle, [bool]$Condition, [string]$Detail) {
  if ($Condition) { Log "  OK    $Libelle" 'OK' } else { Log "  ÉCHEC $Libelle ($Detail)" 'ERREUR'; $Echecs.Add($Libelle) }
}
function Verifier-Https([string]$BuildAttendu) {
  Log "Vérification HTTPS de $($C.Site)" 'ETAPE'
  [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
  $base = $C.Site
  $r = Requete "$base/" $null
  if ($r.Code -eq 0) { Attendre 'certificat TLS valide et site joignable' $false $r.Erreur; return }
  if ($SansAuthentification) { Attendre 'accueil sans authentification : 200' ($r.Code -eq 200) "code $($r.Code)" }
  else { Attendre 'accueil sans identifiants : 401' ($r.Code -eq 401) "code $($r.Code)" }
  Attendre 'en-tête X-Robots-Tag noindex' ("$($r.Robots)" -match 'noindex') "reçu « $($r.Robots) »"
  $h = Requete ("http://$SiteHote/") $null
  Attendre 'HTTP redirigé vers HTTPS avant toute authentification' (@(301, 302, 307, 308) -contains $h.Code -and "$($h.Location)" -like "https://$SiteHote/*") "code $($h.Code), Location « $($h.Location) »"

  $cred = $null; $f = Join-Path $SecretsDir 'http.xml'
  if ($SansAuthentification) { $cred = $null } elseif (Test-Path $f) { $cred = Import-Clixml $f }
  if ($SansAuthentification -or $cred) {
    foreach ($p in '/', '/explorer/', '/sentier/') { $x = Requete "$base$p" $cred; Attendre "$p : 200" ($x.Code -eq 200) "code $($x.Code)" }
    $v = Requete "$base/phare-version.txt" $cred
    Attendre 'phare-version.txt servi' ($v.Code -eq 200 -and $v.Corps -match "^$MarkerId") "code $($v.Code)"
    if ($BuildAttendu) { Attendre "version en ligne = $BuildAttendu" ($v.Corps -match [regex]::Escape("build=$BuildAttendu")) ($v.Corps -replace "`n", ' ') }
    foreach ($p in "/$MarkerName", '/.htpasswd', '/.htaccess') { $x = Requete "$base$p" $cred; Attendre "$p refusé (403)" ($x.Code -eq 403) "code $($x.Code)" }
    $x = Requete "$base/page-inexistante-poc/" $cred; Attendre 'page inexistante : 404' ($x.Code -eq 404) "code $($x.Code)"
  } else { Log "  Accès HTTP non enregistré ($f) : contrôles authentifiés sautés." 'ATTENTION' }

  $wp = Requete 'https://le-phare.info/' $null
  Attendre 'site principal le-phare.info : 200' ($wp.Code -eq 200) "code $($wp.Code)"
  $fuite = Requete 'https://le-phare.info/phare-version.txt' $null
  Attendre 'aucun fichier du POC dans la racine WordPress' ($fuite.Code -ne 200 -or $fuite.Corps -notmatch "^$MarkerId") "code $($fuite.Code)"
}

# --- Déroulé ---
$session = $null
$code = 0
try {
  Log "deploy-ovh.ps1 - journal $LogFile" 'ETAPE'
  if ($Executer -and $VerifierHttps) { Arreter '-Executer inclut déjà la vérification HTTPS.' }
  if ($Initialiser -and -not $Executer) { Log '-Initialiser sans -Executer : simple rappel, rien ne sera créé.' 'ATTENTION' }
  $distant = [bool]($VerifierDistant -or $Executer)
  Valider-Config $distant

  if ($VerifierHttps) {
    Verifier-Https ''
  } else {
    if ($Restaurer) {
      $plein = [IO.Path]::GetFullPath($Restaurer)
      if (-not $plein.StartsWith([IO.Path]::GetFullPath($Sauvegardes) + '\') -or -not (Test-Path (Join-Path $plein $MarkerName))) {
        Arreter "-Restaurer attend un dossier de $Sauvegardes contenant le marqueur du POC."
      }
      $LocalAEnvoyer = $plein
      Log "Restauration demandée depuis $plein" 'ETAPE'
      Controler-Lot $plein
    } else {
      if (-not $SansBuild) { Construire } else { Log 'Build sauté (-SansBuild) : dist existant utilisé.' 'ATTENTION' }
      Preparer-Lot
      $LocalAEnvoyer = $Lot
    }

    if (-not $distant) {
      Log 'SIMULATION terminée : aucune connexion, aucun transfert.' 'OK'
      Log "  .htaccess prévu (chemin du compte résolu à la connexion) : $(Join-Path $Lot '.htaccess')"
      Log '  Étapes suivantes : -VerifierDistant (lecture seule), puis -Executer -Confirmer <dossier> [-Initialiser].'
    } else {
      $session = Ouvrir-Session
      $etat = Inspecter-Distant $session
      if (-not $Restaurer) {
        $homeAbs = if ($C.HomeAbs) { $C.HomeAbs } else { $etat.Home }
        if (-not $C.HomeAbs -and $homeAbs -notmatch '^/home[^/]*/[^/]+') {
          $msg = "Racine SFTP « $homeAbs » : chemin absolu côté Apache inconnu, AuthUserFile serait faux. Renseigner OVH_HOME_ABS (DEPLOIEMENT_OVH.md §8)."
          if ($Executer -and -not $SansAuthentification) { Arreter $msg } else { Log "  $msg" 'ATTENTION' }
        }
        Ecrire-Texte (Join-Path $Lot '.htaccess') (Contenu-Htaccess $homeAbs)
        Log "  AuthUserFile : $homeAbs/$($C.Dossier)/.htpasswd"
      }
      Log 'Aperçu des transferts' 'ETAPE'
      Apercu-Transferts $session $etat $LocalAEnvoyer

      if (-not $Executer) {
        Log 'VÉRIFICATION DISTANTE terminée : rien n''a été écrit sur le serveur.' 'OK'
      } else {
        if ($Restaurer -and $etat.Statut -ne 'marque') { Arreter 'Restauration impossible : le dossier distant ne porte pas le marqueur du POC.' }
        if ($etat.Statut -ne 'marque' -and -not $Initialiser) { Arreter "Premier déploiement (dossier $($etat.Statut)) : ajouter -Initialiser pour l'autoriser explicitement." }
        if (-not $SansAuthentification -and -not (Test-Path (Join-Path $LocalAEnvoyer '.htpasswd'))) { Arreter 'Pas de .htpasswd dans le lot : lancer -CreerAccesHttp, ou -SansAuthentification si OVH ne le permet pas.' }
        if (-not $Confirmer -and (Interactif)) { $Confirmer = Read-Host "Confirmer la publication dans $($etat.Cible) : taper le nom du dossier ($($C.Dossier))" }
        if ($Confirmer -ne $C.Dossier) { Arreter "Confirmation absente ou différente de « $($C.Dossier) » : aucun transfert." }
        $sauvegarde = if ($etat.Statut -eq 'marque') { Sauvegarder $session $etat } else { '' }
        Publier $session $etat $LocalAEnvoyer
        $ligne = '{0};{1};{2};{3};{4}' -f $Horodatage, $(if ($Restaurer) { 'restauration' } else { 'deploiement' }), $(if ($Restaurer) { $Restaurer } else { $script:BuildId }), $etat.Cible, $sauvegarde
        Add-Content -Path (Join-Path $DeployDir 'historique.csv') -Value $ligne -Encoding UTF8
        $session.Dispose(); $session = $null
        $attendu = ''
        if (-not $Restaurer) { $attendu = $script:BuildId }
        Verifier-Https $attendu
      }
    }
  }
  if ($Echecs.Count) { Log "$($Echecs.Count) contrôle(s) en échec." 'ERREUR'; $code = 1 }
} catch {
  if ("$_" -notlike 'ARRET :*') { Log ("Erreur : " + $_.Exception.Message) 'ERREUR' }
  $code = 1
} finally {
  if ($session) { $session.Dispose() }
}
exit $code
