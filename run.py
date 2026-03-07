from dotenv import load_dotenv
from App.app import App

if __name__ == "__main__":
    load_dotenv()
    app = App()
    app.run()
