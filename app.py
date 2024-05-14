from flask import Flask
import dashboard


app = Flask(__name__)
app.register_blueprint(dashboard.dashboard)


if __name__ == '__main__':
    app.run(debug=True)