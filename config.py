import os

# Dosya yükleme klasörü
UPLOAD_FOLDER = './uploads'

# İzin verilen dosya uzantıları
ALLOWED_EXTENSIONS = {'pdf'}

# Veritabanı bağlantısı
DATABASE_URL = 'sqlite:///chatbot.db'

# OpenAI API anahtarını çevresel değişken olarak tanımlayın
os.environ["OPENAI_API_KEY"] = "key"
