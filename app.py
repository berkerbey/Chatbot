from flask import Flask, render_template
from routes.upload import upload_blueprint
from routes.process import process_blueprint
from models import Base, engine

# Flask Uygulaması
app = Flask(__name__)

# Konfigürasyon
app.config.from_pyfile('config.py')

# Blueprint'leri kaydet
app.register_blueprint(upload_blueprint)
app.register_blueprint(process_blueprint)

# Veritabanını oluştur
Base.metadata.create_all(engine)

# Ana Sayfa Rotası
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
