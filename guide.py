import requests
import subprocess

def search_library(input_name):
    search_url = f"https://pypi.org/pypi/{input_name}/json"
    response = requests.get(search_url)

    if response.status_code == 200:
        data = response.json()
        releases = data.get("releases", {})
        
        if releases:
            # Obtém a versão mais recente
            latest_version = max(releases, key=lambda x: releases[x][0]["upload_time"])
            return input_name, latest_version
        else:
            return None
    else:
        return None

def install_library(library_name, version=None):
    try:
        if version:
            subprocess.run(["pip", "install", f"{library_name}=={version}"], check=True)
        else:
            subprocess.run(["pip", "install", library_name], check=True)
        print(f"A biblioteca '{library_name}' foi instalada com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao instalar a biblioteca '{library_name}'. Código de erro: {e.returncode}")

def main():
    user_input = input("Digite um termo para buscar a biblioteca: ")
    library_info = search_library(user_input)

    if library_info:
        library_name, latest_version = library_info
        print(f"Encontrada a biblioteca: {library_name} (última versão: {latest_version})")
        install_choice = input("Deseja instalar esta biblioteca? (y/n): ").lower()

        if install_choice == 'y':
            install_library(library_name, latest_version)
    else:
        print(f"Nenhuma biblioteca encontrada para o termo: {user_input}")

if __name__ == "__main__":
    main()
