import os

# Dosya yükleme klasörü
UPLOAD_FOLDER = './uploads'

# İzin verilen dosya uzantıları
ALLOWED_EXTENSIONS = {'pdf'}

# Veritabanı bağlantısı
DATABASE_URL = 'sqlite:///chatbot.db'

# OpenAI API anahtarını çevresel değişken olarak tanımlayın
os.environ["OPENAI_API_KEY"] = "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"
