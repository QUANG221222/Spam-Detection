import pandas as pd
import os
import sys
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import numpy as np

# Import classifier
from spam_classifier import SpamClassifier

def train_and_save_model():
    """Huấn luyện mô hình từ dữ liệu CSV và lưu mô hình"""
    
    # Tải dữ liệu
    print("📖 Đang tải dữ liệu...")
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'spam.csv')
    
    if not os.path.exists(data_path):
        print(f"❌ Không tìm thấy file dữ liệu tại {data_path}")
        return False
    
    df = pd.read_csv(data_path)
    print(f"✅ Đã tải {len(df)} bản ghi")
    
    # Kiểm tra dữ liệu
    print(f"\nThống kê dữ liệu:")
    print(f"  - Tổng tin nhắn: {len(df)}")
    print(f"  - Ham: {(df['label']=='ham').sum()}")
    print(f"  - Spam: {(df['label']=='spam').sum()}")
    
    # Convert label sang số (ham=0, spam=1)
    df['label_numeric'] = (df['label'] == 'spam').astype(int)
    
    # Tách dữ liệu training và testing
    X_train, X_test, y_train, y_test = train_test_split(
        df['text'], df['label_numeric'],
        test_size=0.2,
        random_state=42,
        stratify=df['label_numeric']
    )
    
    print(f"\n📊 Tách dữ liệu:")
    print(f"  - Training: {len(X_train)} mẫu")
    print(f"  - Testing: {len(X_test)} mẫu")
    
    # Tạo và huấn luyện mô hình
    print("\n🤖 Đang huấn luyện mô hình Naive Bayes...")
    classifier = SpamClassifier()
    classifier.create_pipeline(use_tfidf=True)
    classifier.train(X_train.values, y_train.values)
    
    # Đánh giá mô hình
    print("\n📈 Đánh giá mô hình trên tập test:")
    predictions = classifier.pipeline.predict(X_test.values)
    
    accuracy = accuracy_score(y_test, predictions)
    print(f"  - Độ chính xác: {accuracy*100:.2f}%")
    
    print("\n📋 Chi tiết báo cáo:")
    print(classification_report(y_test, predictions, target_names=['Ham', 'Spam']))
    
    print("\n📊 Confusion Matrix:")
    cm = confusion_matrix(y_test, predictions)
    print(cm)
    
    # Lưu mô hình
    model_path = os.path.join(os.path.dirname(__file__), 'models', 'spam_model.pkl')
    classifier.save_model(model_path)
    print(f"\n✅ Mô hình đã lưu tại {model_path}")
    
    # Test mô hình
    print("\n" + "="*50)
    print("TEST MỘT SỐ THÔNG ĐIỆP")
    print("="*50)
    
    test_messages = [
        "Hi babe, how are you doing? Can we meet tomorrow?",
        "CONGRATULATIONS! You have won £1000000! Click here now!!!",
        "What time is the meeting tomorrow?",
        "Click here to get FREE iPhone 13 now - LIMITED TIME OFFER",
        "Let's grab coffee at 3pm",
    ]
    
    for msg in test_messages:
        result = classifier.predict(msg)
        print(f"\n📝 Tin nhắn: {msg[:60]}...")
        print(f"   🏷️  Phân loại: {result['label']}")
        print(f"   📊 Độ tin cậy: {result['confidence']*100:.2f}%")
    
    return True

if __name__ == "__main__":
    success = train_and_save_model()
    if success:
        print("\n" + "="*50)
        print("✅ HỌC LUYỆN HOÀN TẤT!")
        print("="*50)
    else:
        print("\n" + "="*50)
        print("❌ HỌC LUYỆN THẤT BẠI!")
        print("="*50)
        sys.exit(1)
