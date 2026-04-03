# 🛡️ Spam Detection System

Hệ thống phân loại Email/Tin Nhắn Spam hoặc Ham sử dụng **Naive Bayes Classifier** - một trong những techniques phổ biến nhất trong xử lý ngôn ngữ tự nhiên (NLP).

## 📋 Mục Lục

- [Tính Năng](#tính-năng)
- [Cấu Trúc Project](#cấu-trúc-project)
- [Cài Đặt](#cài-đặt)
- [Sử Dụng](#sử-dụng)
- [API Endpoints](#api-endpoints)
- [Kỹ Thuật Sử Dụng](#kỹ-thuật-sử-dụng)

## ✨ Tính Năng

✅ **Ba Chế Độ Phân Tích:**

- 📝 Tin nhắn đơn: Nhập trực tiếp nội dung để phân loại
- 📁 Tải file: Kéo & thả file `.txt` để phân tích hàng loạt
- 📋 Nhập hàng loạt: Nhập danh sách tin nhắn từng dòng

✅ **Giao Diện Hiện Đại:**

- 🎨 Thiết kế đẹp với gradient và animation
- 🖱️ Drag & drop file support
- 📱 Responsive design (mobile-friendly)
- 🎯 Real-time API status indicator

✅ **Phân Tích Chi Tiết:**

- 📊 Hiển thị xác suất (confidence score)
- 📈 Thống kê: tổng tin nhắn, số spam, số ham
- 🎨 Màu sắc trực quan (đỏ=Spam, xanh=Ham)
- 📉 Progress bar cho độ tin cậy

## 📁 Cấu Trúc Project

```
Spam Detection/
├── backend/
│   ├── app.py                 # Flask API backend
│   ├── spam_classifier.py    # Naive Bayes classifier
│   ├── train_model.py        # Script huấn luyện mô hình
│   ├── requirements.txt       # Python dependencies
│   ├── models/
│   │   └── spam_model.pkl    # Mô hình đã huấn luyện (được tạo sau training)
│   ├── data/
│   │   └── spam_data.csv     # Dataset huấn luyện
│   └── frontend/
│       └── index.html         # Giao diện web
```

## 🚀 Cài Đặt

### 1. Yêu Cầu Hệ Thống

- Python 3.8+
- pip hoặc conda

### 2. Cài Đặt Dependencies

```bash
# Đi vào thư mục backend
cd "Spam Detection\backend"

# Cài đặt các package cần thiết
pip install -r requirements.txt
```

**Các package chính:**

- `Flask` - Web framework
- `Flask-CORS` - Xử lý CORS
- `scikit-learn` - Machine learning library
- `pandas` - Data manipulation
- `numpy` - Numerical computing

### 3. Huấn Luyện Mô Hình

Chạy script để huấn luyện mô hình Naive Bayes từ dataset:

```bash
python train_model.py
```

**Output:**

- ✅ Mô hình sẽ được lưu tại `models/spam_model.pkl`
- 📊 Hiển thị accuracy, precision, recall
- 📈 Test results trên một số tin nhắn mẫu

### 4. Khởi Động API

```bash
python app.py
```

**API sẽ chạy tại:** `http://localhost:5000`

### 5. Mở Giao Diện Web

Mở file `frontend/index.html` trong trình duyệt hoặc:

```bash
# Hoặc dùng python simple server
python -m http.server 8000
# Rồi truy cập http://localhost:8000/frontend/index.html
```

## 💻 Sử Dụng

### Chế Độ 1: Tin Nhắn Đơn

1. Chọn tab "✉️ Tin Nhắn Đơn"
2. Nhập nội dung tin nhắn cần kiểm tra
3. Nhấp nút "🔍 Dự Đoán"
4. Xem kết quả với badge và confidence score

**Ví Dụ:**

- ✅ Ham: "Hi babe, how are you doing?"
- ⚠️ Spam: "CLICK HERE TO WIN £1000000 NOW!!!"

### Chế Độ 2: Tải File

1. Chọn tab "📁 Tải File"
2. Kéo file `.txt` vào vùng drop hoặc nhấp chọn
3. Nhấp "🚀 Phân Tích File"
4. Xem thống kê tóm tắt và danh sách kết quả

**Định Dạng File:**

```
Dòng 1: Tin nhắn thứ nhất
Dòng 2: Tin nhắn thứ hai
Dòng 3: Tin nhắn thứ ba
...
```

### Chế Độ 3: Nhập Hàng Loạt

1. Chọn tab "📋 Nhập Hàng Loạt"
2. Nhập danh sách tin nhắn (mỗi dòng một tin nhắn)
3. Nhấp "🔍 Phân Tích Hàng Loạt"
4. Xem thống kê và kết quả chi tiết

## 🔌 API Endpoints

### 1. Health Check

```
GET /api/health
```

**Response:**

```json
{
  "status": "ok",
  "message": "Spam Detection API is running",
  "model_loaded": true
}
```

### 2. Model Info

```
GET /api/model-info
```

**Response:**

```json
{
  "status": "success",
  "info": {
    "model_type": "Naive Bayes Classifier",
    "vectorizer_type": "TfidfVectorizer",
    "status": "Ready for prediction"
  }
}
```

### 3. Dự Đoán Tin Nhắn Đơn

```
POST /api/predict
Content-Type: application/json

{
  "text": "Hello, how are you?"
}
```

**Response:**

```json
{
  "status": "success",
  "prediction": 0,
  "confidence": 0.95,
  "label": "Ham",
  "text": "Hello, how are you?"
}
```

### 4. Dự Đoán Hàng Loạt

```
POST /api/predict-batch
Content-Type: application/json

{
  "texts": [
    "Hello",
    "Click here to win",
    "How are you?"
  ]
}
```

**Response:**

```json
{
  "status": "success",
  "total_messages": 3,
  "spam_count": 1,
  "ham_count": 2,
  "spam_percentage": "33.33%",
  "predictions": [
    { "text": "Hello", "prediction": 0, "confidence": 0.92, "label": "Ham" },
    {
      "text": "Click here to win",
      "prediction": 1,
      "confidence": 0.88,
      "label": "Spam"
    },
    {
      "text": "How are you?",
      "prediction": 0,
      "confidence": 0.96,
      "label": "Ham"
    }
  ]
}
```

### 5. Dự Đoán Từ File

```
POST /api/predict-file
Content-Type: multipart/form-data

file: [file.txt]
```

**Response:** Giống predict-batch

## 🧠 Kỹ Thuật Sử Dụng

### Naive Bayes Classifier

**Nguyên Lý:**

- Dựa trên định lý Bayes trong xác suất thống kê
- Giả định các feature (từ) là độc lập với nhau
- Tính toán P(Spam|Text) và P(Ham|Text)
- Chọn class có xác suất cao nhất

**Công Thức Cơ Bản:**

```
P(Class|Text) = P(Text|Class) × P(Class) / P(Text)
```

**Ưu Điểm:**

- ✅ Nhanh và hiệu quả
- ✅ Hoạt động tốt với dữ liệu ít
- ✅ Dễ hiểu và implement
- ✅ Kết quả tốt cho text classification

**Nhược Điểm:**

- ❌ Giả định độc lập không luôn đúng
- ❌ Nhạy cảm với unbalanced data
- ❌ Không tốt với các mối quan hệ phức tạp

### Text Vectorization

**TF-IDF (Term Frequency-Inverse Document Frequency):**

- Chuyển text thành vector số
- TF: Tần suất từ trong document
- IDF: Nghịch đảo tần suất từ trong tất cả documents
- Giảm trọng số của các từ phổ biến

**Preprocessing:**

- Loại bỏ stop words (a, the, is, ...)
- Convert thành lowercase
- Sử dụng n-grams (1-2)
- Min_df=2, Max_df=0.8

## 📊 Dataset

**File:** `data/spam_data.csv`

**Cấu trúc:**

```
text,label
"Go until jurong point crazy...",0
"Free entry in 2 a wkly comp...",1
```

**Thống Kê:**

- 🔢 Số tin nhắn: ~250+
- 📊 Ham (0): ~80%
- ⚠️ Spam (1): ~20%
- 🌍 Ngôn ngữ: Chủ yếu tiếng Anh

**Nguồn:** UCI Machine Learning Repository - SMS Spam Collection Dataset

## 🔧 Troubleshooting

### Lỗi: "Mô hình chưa được tải"

**Giải Pháp:** Chạy `python train_model.py` trước

### CORS Error

**Giải Pháp:** Flask-CORS đã được cấu hình, nếu vẫn lỗi, check console browser

### Port 5000 đã được sử dụng

**Giải Pháp:** Sửa trong `app.py`:

```python
app.run(port=5001)  # Dùng port khác
```

### File không phải .txt

**Giải Pháp:** Chỉ hỗ trợ file text (.txt), convert file XLSX/CSV thành TXT

## 📈 Cải Thiện Hiệu Suất

1. **Thêm dữ liệu huấn luyện:**
   - Thêm tin nhắn vào `spam_data.csv`
   - Chạy lại `train_model.py`

2. **Tuning hyperparameters:**
   - Thay đổi `max_features`, `ngram_range` trong `spam_classifier.py`
   - Điều chỉnh `alpha` của Naive Bayes

3. **Thử các kỹ thuật khác:**
   - RandomForest Classifier
   - Support Vector Machine (SVM)
   - Deep Learning (LSTM)

## 📚 Tài Liệu Thêm

- [scikit-learn Documentation](https://scikit-learn.org/)
- [TF-IDF Vectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)
- [Naive Bayes Classifier](https://scikit-learn.org/stable/modules/naive_bayes.html)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 📝 Ghi Chú

- Mô hình được huấn luyện trên tiếng Anh, có thể không tốt với các ngôn ngữ khác
- Accuracy hiện tại: ~95%+ trên tập test
- File mô hình (\*.pkl) có thể được commit hoặc skip tùy theo project setup

## 👨‍💻 Author

Phát triển bởi: [AI Class 2026]

---

**Chúc bạn sử dụng hệ thống Spam Detection thành công! 🎉**
# Spam-Detection
