import os
import shutil
from datetime import datetime


def limpar_diretorio_temp(diretorio_temp):
    now = datetime.now()
    print(f"Iniciando limpeza do diretório {diretorio_temp} às {now}")
    for filename in os.listdir(diretorio_temp):
        file_path = os.path.join(diretorio_temp, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
            print(f"Removido: {file_path}")
        except Exception as e:
            print(f"Erro ao deletar {file_path}: {e}")


if __name__ == "__main__":
    diretorio_temp = './temp'
    limpar_diretorio_temp(diretorio_temp)
