@echo off
REM Remplace index_editorial.csv par index_editorial.merged.csv (meme contenu que derniere fusion).
REM A lancer quand index_editorial.csv n'est plus verrouille : fermer Cursor/Excel/OneDrive sync si besoin.
cd /d "%~dp0.."
copy /y "index_editorial.merged.csv" "index_editorial.csv"
if errorlevel 1 (
  echo ECHEC : fichier probablement encore ouvert ailleurs.
  exit /b 1
)
echo OK : index_editorial.csv synchronise depuis index_editorial.merged.csv
exit /b 0
