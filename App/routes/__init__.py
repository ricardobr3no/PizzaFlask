import os
from werkzeug.utils import secure_filename


class HandleFile:
    UPLOAD_FOLFER = "uploads"
    os.makedirs(UPLOAD_FOLFER, exist_ok=True)

    @staticmethod
    def get_filename(file):
        return file.filename

    @staticmethod
    def get_secure_name(file):
        return secure_filename(file.filename)

    @staticmethod
    def upload_file(file):
        filename = HandleFile.get_secure_name(file)
        caminho_salvamento = os.path.join(HandleFile.UPLOAD_FOLFER, filename)
        print(caminho_salvamento)
        # salva arquivo no servidor
        file.save(caminho_salvamento)

    @staticmethod
    def get_image(filename: str):
        pass


from .admin_routes import admin_bp
from .home_routes import home_bp
from .login_routes import login_cadastro_bp
