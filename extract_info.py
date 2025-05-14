import os
import zipfile
import re
from pathlib import Path
import sys

def extract_info_from_html(html_content):
    # Padrões para encontrar IMEI e Users
    imei_pattern = r'IMEI\(s\): (.*?)<br/>'
    users_pattern = r'Users: (.*?)<br/>'
    
    # Encontrar IMEI
    imei_match = re.search(imei_pattern, html_content)
    imei = imei_match.group(1).strip() if imei_match else "Não encontrado"
    
    # Encontrar Users
    users_match = re.search(users_pattern, html_content)
    users = users_match.group(1).strip() if users_match else "Não encontrado"
    
    return imei, users

def process_zip_files(directory_path):
    # Lista para armazenar resultados
    results = []
    
    # Iterar sobre todos os arquivos no diretório
    for zip_file in Path(directory_path).glob('*.zip'):
        try:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                # Procurar por arquivos HTML no ZIP
                html_files = [f for f in zip_ref.namelist() if f.endswith('.html')]
                
                for html_file in html_files:
                    try:
                        # Ler o conteúdo do arquivo HTML
                        with zip_ref.open(html_file) as f:
                            html_content = f.read().decode('utf-8')
                            
                            # Extrair informações
                            imei, users = extract_info_from_html(html_content)
                            
                            # Adicionar resultados
                            results.append({
                                'arquivo_zip': zip_file.name,
                                'arquivo_html': html_file,
                                'imei': imei,
                                'users': users
                            })
                    except Exception as e:
                        print(f"Erro ao processar {html_file} em {zip_file.name}: {str(e)}")
                        
        except Exception as e:
            print(f"Erro ao abrir {zip_file.name}: {str(e)}")
    
    return results

def main():
    # Verificar se o caminho do diretório foi fornecido como argumento
    if len(sys.argv) != 2:
        print("Uso: python extract_info.py <caminho_do_diretorio>")
        print("Exemplo: python extract_info.py C:/Users/public/Documents/MACAW/GOOGLE/6.1")
        return
    
    # Obter o caminho do diretório do argumento
    directory = sys.argv[1]
    
    # Verificar se o diretório existe
    if not os.path.exists(directory):
        print(f"Diretório não encontrado: {directory}")
        return
    
    # Processar arquivos
    results = process_zip_files(directory)
    
    # Exibir resultados
    print("\nResultados encontrados:")
    print("-" * 80)
    for result in results:
        print(f"\nArquivo ZIP: {result['arquivo_zip']}")
        print(f"Arquivo HTML: {result['arquivo_html']}")
        print(f"IMEI: {result['imei']}")
        print(f"Users: {result['users']}")
        print("-" * 80)

if __name__ == "__main__":
    main() 