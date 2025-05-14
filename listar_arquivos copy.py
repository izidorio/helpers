import os
import sys
from pathlib import Path
import zipfile

def converter_para_gb(bytes):
    return bytes / (1024 * 1024 * 1024)

def listar_conteudo_zip(arquivo_zip, arquivo_saida):
    try:
        with zipfile.ZipFile(arquivo_zip, 'r') as zip_ref:
            arquivo_saida.write(f"\nConteúdo do arquivo ZIP: {arquivo_zip.name}\n")
            arquivo_saida.write("-" * 50 + "\n")
            for arquivo in zip_ref.namelist():
                info = zip_ref.getinfo(arquivo)
                tamanho_gb = converter_para_gb(info.file_size)
                arquivo_saida.write(f"Arquivo: {arquivo} - Tamanho: {tamanho_gb:.2f} GB\n")
            arquivo_saida.write("-" * 50 + "\n")
    except Exception as e:
        arquivo_saida.write(f"Erro ao ler arquivo ZIP {arquivo_zip.name}: {str(e)}\n")

def listar_arquivos(diretorio):
    try:
        # Converte o caminho para objeto Path
        caminho = Path(diretorio)
        
        # Verifica se o diretório existe
        if not caminho.exists():
            print(f"Erro: O diretório '{diretorio}' não existe.")
            return
        
        # Verifica se é realmente um diretório
        if not caminho.is_dir():
            print(f"Erro: '{diretorio}' não é um diretório.")
            return
        
        # Abre o arquivo de saída
        with open("relatorio.txt", "w", encoding="utf-8") as arquivo_saida:
            arquivo_saida.write(f"Listando conteúdo do diretório: {diretorio}\n\n")
            
            # Lista todos os arquivos e diretórios
            for item in caminho.iterdir():
                tipo = "Diretório" if item.is_dir() else "Arquivo"
                tamanho = ""
                if item.is_file():
                    tamanho_gb = converter_para_gb(item.stat().st_size)
                    tamanho = f" - Tamanho: {tamanho_gb:.2f} GB"
                    arquivo_saida.write(f"{tipo}: {item.name}{tamanho}\n")
                    
                    # Se for um arquivo ZIP, lista seu conteúdo
                    if item.suffix.lower() == '.zip':
                        listar_conteudo_zip(item, arquivo_saida)
                else:
                    arquivo_saida.write(f"{tipo}: {item.name}{tamanho}\n")
            
        print("Relatório gerado com sucesso em 'relatorio.txt'")
            
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")

if __name__ == "__main__":
    # Verifica se foi passado um argumento
    if len(sys.argv) != 2:
        print("Uso: python script.py <caminho_do_diretorio>")
        sys.exit(1)
    
    # Pega o diretório passado como argumento
    diretorio = sys.argv[1]
    listar_arquivos(diretorio)