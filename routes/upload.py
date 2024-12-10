from flask import Blueprint, request, jsonify, render_template
import os
from models import UserPDF, session

upload_blueprint = Blueprint('upload', __name__)

@upload_blueprint.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """
    PDF dosyası yükler ve uploads/ klasörüne kaydeder.
    GET isteğinde bir yükleme formu döndürür.
    """
    if request.method == 'GET':
        # Yükleme formunu döndür
        return render_template('upload.html')

    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error": "Dosya bulunamadı. Lütfen bir dosya seçin!"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "Dosya seçilmedi. Lütfen bir dosya seçin!"}), 400

        if file:
            user_id = request.form.get('user_id', 'default_user')  # Kullanıcı ID'si alınır
            user_folder = os.path.join('./uploads', user_id)
            os.makedirs(user_folder, exist_ok=True)  # Kullanıcıya özel klasör oluştur

            file_path = os.path.join(user_folder, file.filename)
            file.save(file_path)  # Dosyayı fiziksel olarak kaydet

            # Veritabanına kayıt
            pdf_record = UserPDF(user_id=user_id, pdf_name=file.filename, pdf_path=file_path)
            session.add(pdf_record)
            session.commit()

            return jsonify({"message": "Dosya başarıyla yüklendi!", "file_path": file_path}), 200
