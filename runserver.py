from application.commands import InitDbCommand
from application import create_app
import config

app = create_app(config.Config)

if __name__ == "__main__":
    app.run()