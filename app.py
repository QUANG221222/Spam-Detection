from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from spam_classifier import SpamClassifier
import traceback
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Tải mô hình
classifier = SpamClassifier()
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'spam_model.pkl')

def load_model():
    """Tải mô hình từ file"""
    if os.path.exists(MODEL_PATH):
        try:
            classifier.load_model(MODEL_PATH)
            print(f"✅ Mô hình đã được tải từ {MODEL_PATH}")
            return True
        except Exception as e:
            print(f"❌ Lỗi khi tải mô hình: {e}")
            return False
    else:
        print(f"❌ Không tìm thấy mô hình tại {MODEL_PATH}")
        return False

@app.route('/api/health', methods=['GET'])
def health_check():
    """Kiểm tra trạng thái API"""
    return jsonify({
        'status': 'ok',
        'message': 'Spam Detection API is running',
        'model_loaded': classifier.pipeline is not None
    }), 200

@app.route('/api/model-info', methods=['GET'])
def model_info():
    """Lấy thông tin về mô hình"""
    if classifier.pipeline is None:
        return jsonify({
            'status': 'error',
            'message': 'Mô hình chưa được tải'
        }), 400
    
    return jsonify({
        'status': 'success',
        'info': classifier.get_model_info()
    }), 200

@app.route('/api/predict', methods=['POST'])
def predict_spam():
    """Dự đoán một tin nhắn"""
    try:
        if classifier.pipeline is None:
            return jsonify({
                'status': 'error',
                'message': 'Mô hình chưa được tải'
            }), 400
        
        # Lấy dữ liệu từ request
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({
                'status': 'error',
                'message': 'Vui lòng cung cấp nội dung tin nhắn'
            }), 400
        
        # Dự đoán
        result = classifier.predict(text)
        
        return jsonify({
            'status': 'success',
            'prediction': result['prediction'],
            'confidence': result['confidence'],
            'label': result['label'],
            'text': result['text']
        }), 200
    
    except Exception as e:
        print(f"❌ Lỗi trong predict: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/predict-file', methods=['POST'])
def predict_file():
    """Dự đoán từ file text"""
    try:
        if classifier.pipeline is None:
            return jsonify({
                'status': 'error',
                'message': 'Mô hình chưa được tải'
            }), 400
        
        # Kiểm tra file
        if 'file' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'Không tìm thấy file'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'status': 'error',
                'message': 'Chưa chọn file'
            }), 400
        
        # Đọc file
        if file.filename.endswith('.txt'):
            content = file.read().decode('utf-8')
            lines = content.strip().split('\n')
        else:
            return jsonify({
                'status': 'error',
                'message': 'Chỉ hỗ trợ file .txt'
            }), 400
        
        # Dự đoán từng dòng
        results = []
        for line in lines:
            if line.strip():
                result = classifier.predict(line.strip())
                results.append(result)
        
        # Tính thống kê
        spam_count = sum(1 for r in results if r['prediction'] == 1)
        ham_count = len(results) - spam_count
        
        return jsonify({
            'status': 'success',
            'total_messages': len(results),
            'spam_count': spam_count,
            'ham_count': ham_count,
            'spam_percentage': f"{(spam_count/len(results)*100):.2f}%" if results else "0%",
            'predictions': results[:50]  # Trả về 50 kết quả đầu tiên
        }), 200
    
    except Exception as e:
        print(f"❌ Lỗi trong predict_file: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/predict-batch', methods=['POST'])
def predict_batch():
    """Dự đoán nhiều tin nhắn"""
    try:
        if classifier.pipeline is None:
            return jsonify({
                'status': 'error',
                'message': 'Mô hình chưa được tải'
            }), 400
        
        data = request.get_json()
        texts = data.get('texts', [])
        
        if not texts or not isinstance(texts, list):
            return jsonify({
                'status': 'error',
                'message': 'Vui lòng cung cấp danh sách tin nhắn'
            }), 400
        
        # Lọc tin nhắn rỗng
        texts = [t.strip() for t in texts if t.strip()]
        
        if not texts:
            return jsonify({
                'status': 'error',
                'message': 'Danh sách tin nhắn trống'
            }), 400
        
        # Dự đoán
        results = classifier.predict_batch(texts)
        
        # Tính thống kê
        spam_count = sum(1 for r in results if r['prediction'] == 1)
        ham_count = len(results) - spam_count
        
        return jsonify({
            'status': 'success',
            'total_messages': len(results),
            'spam_count': spam_count,
            'ham_count': ham_count,
            'spam_percentage': f"{(spam_count/len(results)*100):.2f}%",
            'predictions': results
        }), 200
    
    except Exception as e:
        print(f"❌ Lỗi trong predict_batch: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Xử lý lỗi 404"""
    return jsonify({
        'status': 'error',
        'message': 'Endpoint không tồn tại'
    }), 404

@app.errorhandler(500)
def server_error(error):
    """Xử lý lỗi 500"""
    return jsonify({
        'status': 'error',
        'message': 'Lỗi máy chủ'
    }), 500

if __name__ == '__main__':
    print("🚀 Đang khởi động Spam Detection API...")
    print("-" * 50)
    
    # Tải mô hình
    if load_model():
        print("\n✅ Sẵn sàng cho dự đoán!")
    else:
        print("\n⚠️  Mô hình chưa được huấn luyện. Vui lòng chạy train_model.py trước.")
    
    print("-" * 50)
    print("🌐 API đang chạy tại http://localhost:5000")
    print("\nAPI Endpoints:")
    print("  GET  /api/health          - Kiểm tra trạng thái")
    print("  GET  /api/model-info      - Thông tin mô hình")
    print("  POST /api/predict         - Dự đoán một tin nhắn")
    print("  POST /api/predict-batch   - Dự đoán nhiều tin nhắn")
    print("  POST /api/predict-file    - Dự đoán từ file")
    print("-" * 50)
    
    # Chạy Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
