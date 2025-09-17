Executar a descompactação em 1º nível dos arquivos baixados do Google LERS

```bash
python unzip_dir.py C:/Users/Public/Documents/MISTER/GOOGLE/2.2
```

Executar a extração da bilhetagem dos arquivos .zip

```bash
python extract_info.py C:/Users/Public/Documents/MISTER/GOOGLE/2.1/descompactados
```

comando para executar com o Powershell para criar uma nova pasta vazia para o output do IPED

```powershell
$list = @(
    "c:\Users\Public\Documents\MACAW\GOOGLE\6.2\emaila@gmail.com"
    "c:\Users\Public\Documents\MACAW\GOOGLE\6.2\emailb@gmail.com"
)

foreach ($folder in $list) {
    $newFolder = "C:\Users\Public\Documents\MISTER\GOOGLE\2.2\descompactados\_$folder"
    New-Item -ItemType Directory -Path $newFolder -Force
}

Write-Host "Pastas criadas com sucesso!"
```

Comando do IPD

```bash
C:\IPED-4.2.0_and_IPEDIAR\iped-4.2.0\iped.exe -d `
"c:\Users\Public\Documents\MACAW\GOOGLE\6.2\emaila@gmail.com" `
-o `
"c:\Users\Public\Documents\MACAW\GOOGLE\6.2\_emaila@gmail.com"
```
