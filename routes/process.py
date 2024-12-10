from flask import Blueprint, request, jsonify, render_template
from utils.pdf_utils import pdf_to_text
from utils.text_utils import chunk_text
from utils.vector_utils import create_vector_store, query_vector_store

process_blueprint = Blueprint('process', __name__)
vector_stores = {}  # Kullanıcı bazında vektör tabanı saklama

@process_blueprint.route('/process', methods=['GET'])
def process_home():
    """
    PDF İşleme ve Sorgulama Ana Sayfası
    """
    return render_template('process.html')

@process_blueprint.route('/process/<user_id>/<file_id>', methods=['POST'])
def process_pdf(user_id, file_id):
    """
    PDF dosyasını işle ve vektör tabanı oluştur.
    """
    from models import UserPDF, session

    # Veritabanından dosya yolunu al
    pdf = session.query(UserPDF).filter_by(user_id=user_id, id=file_id).first()
    if not pdf:
        return jsonify({"error": "Dosya bulunamadı"}), 404

    # PDF'den metin çıkar
    text = pdf_to_text(pdf.pdf_path)
    if not text:
        return jsonify({"error": "PDF'den metin çıkarılamadı!"}), 500

    chunks = chunk_text(text)

    # Vektör tabanı oluştur ve sakla
    try:
        vector_store = create_vector_store(chunks)
        vector_stores[user_id] = vector_store  # Kullanıcı bazında sakla
        print(f"Vektör tabanı oluşturuldu: {vector_stores.keys()}")  # Debug
    except Exception as e:
        return jsonify({"error": f"Vektör tabanı oluşturulurken hata oluştu: {str(e)}"}), 500

    return jsonify({"message": "Dosya başarıyla işlendi ve vektör tabanı oluşturuldu!"}), 200


@process_blueprint.route('/files/<user_id>', methods=['GET'])
def list_user_files(user_id):
    """
    Kullanıcının yüklediği dosyaları listele
    """
    from models import UserPDF, session
    files = session.query(UserPDF).filter_by(user_id=user_id).all()
    file_list = [{"id": f.id, "name": f.pdf_name, "path": f.pdf_path} for f in files]
    return jsonify(file_list)

@process_blueprint.route('/query/<user_id>', methods=['POST'])
def query_pdf(user_id):
    """
    Kullanıcının vektör tabanını sorgula.
    """
    # Kullanıcıdan gelen soruyu alın
    question = request.json.get('question')
    if not question:
        return jsonify({"error": "Soru eksik!"}), 400

    # Kullanıcının vektör tabanını kontrol edin
    if user_id not in vector_stores:
        print(f"Mevcut vektör tabanları: {vector_stores.keys()}")  # Debug
        return jsonify({"error": "Kullanıcı için vektör tabanı bulunamadı!"}), 404

    # Vektör tabanını sorgula
    try:
        vector_store = vector_stores[user_id]
        answer = query_vector_store(vector_store, question)
        return jsonify({"answer": answer}), 200
    except Exception as e:
        return jsonify({"error": f"Sorgu sırasında bir hata oluştu: {str(e)}"}), 500

