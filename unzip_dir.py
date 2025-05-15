import os
import sys
from pathlib import Path
import zipfile
import shutil

def tem_zip_dentro(arquivo_zip):
    try:
        print(f"Verificando se {arquivo_zip.name} contém arquivos ZIP...")
        with zipfile.ZipFile(arquivo_zip, 'r') as zip_ref:
            for arquivo in zip_ref.namelist():
                if arquivo.lower().endswith('.zip'):
                    print(f"Encontrado arquivo ZIP dentro de {arquivo_zip.name}: {arquivo}")
                    return True
        print(f"Nenhum arquivo ZIP encontrado dentro de {arquivo_zip.name}")
        return False
    except Exception as e:
        print(f"Erro ao verificar arquivo ZIP {arquivo_zip.name}: {str(e)}")
        return False

def descompactar_zip(arquivo_zip, diretorio_destino):
    try:
        print(f"Descompactando {arquivo_zip.name} para {diretorio_destino}...")
        with zipfile.ZipFile(arquivo_zip, 'r') as zip_ref:
            zip_ref.extractall(diretorio_destino)
        print(f"Descompactação concluída com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao descompactar {arquivo_zip.name}: {str(e)}")
        return False

def converter_para_gb(bytes):
    return bytes / (1024 * 1024 * 1024)

def listar_conteudo_zip(arquivo_zip, arquivo_saida):
    try:
        print(f"Listando conteúdo de {arquivo_zip.name}...")
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
        print(f"Iniciando processamento do diretório: {diretorio}")
        
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
        
        # Cria diretório para arquivos descompactados
        dir_descompactados = caminho / "descompactados"
        print(f"Criando diretório para arquivos descompactados: {dir_descompactados}")
        dir_descompactados.mkdir(exist_ok=True)
        
        # Abre o arquivo de saída
        print("Criando arquivo de relatório...")
        with open("relatorio.txt", "w", encoding="utf-8") as arquivo_saida:
            arquivo_saida.write(f"Listando conteúdo do diretório: {diretorio}\n\n")
            
            # Lista todos os arquivos e diretórios
            print("Iniciando varredura de arquivos...")
            for item in caminho.iterdir():
                print(f"Processando: {item.name}")
                if item.is_file() and item.suffix.lower() == '.zip':
                    # Verifica se o ZIP contém outros ZIPs
                    if tem_zip_dentro(item):
                        arquivo_saida.write(f"Arquivo ZIP com ZIPs internos encontrado: {item.name}\n")
                        
                        # Descompacta o arquivo
                        if descompactar_zip(item, dir_descompactados):
                            # Renomeia o arquivo original
                            novo_nome = item.with_name(f"_{item.stem}{item.suffix}")
                            item.rename(novo_nome)
                            arquivo_saida.write(f"Arquivo descompactado e renomeado para: {novo_nome.name}\n")
                        else:
                            arquivo_saida.write(f"Falha ao descompactar: {item.name}\n")
                    
                    # Lista o conteúdo do ZIP
                    listar_conteudo_zip(item, arquivo_saida)
                else:
                    tipo = "Diretório" if item.is_dir() else "Arquivo"
                    tamanho = ""
                    if item.is_file():
                        tamanho_gb = converter_para_gb(item.stat().st_size)
                        tamanho = f" - Tamanho: {tamanho_gb:.2f} GB"
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