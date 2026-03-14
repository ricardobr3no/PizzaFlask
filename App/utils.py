import os
from werkzeug.utils import secure_filename


class HandleFile:
    # Define o caminho absoluto para evitar erros de localização
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "..", "uploads")

    # Garante que a pasta exista ao importar a classe
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    @staticmethod
    def get_filename(file):
        return file.filename

    @staticmethod
    def get_secure_name(file):
        return secure_filename(file.filename)

    @staticmethod
    def upload_file(file):
        if file:
            filename = secure_filename(file.filename)
            # Salvamento usando o caminho absoluto construído
            caminho_salvamento = os.path.join(HandleFile.UPLOAD_FOLDER, filename)
            file.save(caminho_salvamento)
            return filename
        return None
