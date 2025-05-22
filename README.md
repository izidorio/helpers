Executar a descompactação em 1º nível dos arquivos baixados do Google LERS

```bash
python unzip_dir.py C:/Users/public/Documents/MACAW/GOOGLE/6.1
```

Executar a extração da bilhetagem dos arquivos .zip

```bash
python extract_info.py C:/Users/public/Documents/MACAW/GOOGLE/6.1/descompactados
```

comando para executar com o Powershell para criar uma nova pasta vazia para o output do IPED

```bash
$list = @(
    "c:\Users\Public\Documents\MACAW\GOOGLE\6.2\emaila@gmail.com"
    "c:\Users\Public\Documents\MACAW\GOOGLE\6.2\emailb@gmail.com"
)

foreach ($folder in $list) {
    $newFolder = "$($folder -replace '(?<=6.2\\)', '_')"
    New-Item -ItemType Directory -Path $newFolder -Force
}

Write-Host "Pastas criadas com sucesso!"
```

Comando do IPD

```bash
C:\IPED-4.2.0_and_IPEDIAR\iped-4.2.0\iped.exe -d "C:\Users\Public\Documents\MACAW\GOOGLE\6.2\emaila@gmail.com" -o "C:\Users\Public\Documents\MACAW\GOOGLE\6.2\_emaila@gmail.com"
```
