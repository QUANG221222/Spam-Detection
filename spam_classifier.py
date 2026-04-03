import pickle
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import pandas as pd
import os

class SpamClassifier:
    def __init__(self):
        self.vectorizer = None
        self.model = None
        self.pipeline = None
    
    def create_pipeline(self, use_tfidf=True):
        """Tạo pipeline với Naive Bayes Classifier
        
        Args:
            use_tfidf (bool): Nếu True dùng TfidfVectorizer, nếu False dùng CountVectorizer
        """
        if use_tfidf:
            self.vectorizer = TfidfVectorizer(
                max_features=5000,
                stop_words='english',
                lowercase=True,
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.8
            )
        else:
            self.vectorizer = CountVectorizer(
                max_features=5000,
                stop_words='english',
                lowercase=True,
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.8
            )
        
        self.model = MultinomialNB(alpha=1.0)
        self.pipeline = Pipeline([
            ('vectorizer', self.vectorizer),
            ('classifier', self.model)
        ])
        
        return self.pipeline
    
    def train(self, texts, labels):
        """Huấn luyện mô hình
        
        Args:
            texts (list): Danh sách văn bản
            labels (list): Danh sách nhãn (0=Ham, 1=Spam)
        """
        if self.pipeline is None:
            self.create_pipeline()
        
        self.pipeline.fit(texts, labels)
        print("✅ Model training hoàn tất!")
        return self
    
    def predict(self, text):
        """Dự đoán một văn bản
        
        Args:
            text (str): Văn bản cần dự đoán
            
        Returns:
            dict: {'prediction': 0/1, 'confidence': float, 'label': 'Ham'/'Spam'}
        """
        prediction = self.pipeline.predict([text])[0]
        confidence = max(self.pipeline.predict_proba([text])[0])
        label = 'Spam' if prediction == 1 else 'Ham'
        
        return {
            'prediction': int(prediction),
            'confidence': float(confidence),
            'label': label,
            'text': text[:100] + '...' if len(text) > 100 else text
        }
    
    def predict_batch(self, texts):
        """Dự đoán nhiều văn bản
        
        Args:
            texts (list): Danh sách văn bản
            
        Returns:
            list: Danh sách kết quả dự đoán
        """
        predictions = self.pipeline.predict(texts)
        probabilities = self.pipeline.predict_proba(texts)
        
        results = []
        for i, (pred, probs) in enumerate(zip(predictions, probabilities)):
            label = 'Spam' if pred == 1 else 'Ham'
            confidence = max(probs)
            results.append({
                'text': texts[i][:100] + '...' if len(texts[i]) > 100 else texts[i],
                'prediction': int(pred),
                'confidence': float(confidence),
                'label': label
            })
        
        return results
    
    def save_model(self, filepath):
        """Lưu mô hình vào file
        
        Args:
            filepath (str): Đường dẫn file lưu mô hình
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump(self.pipeline, f)
        print(f"✅ Mô hình đã lưu tại {filepath}")
    
    def load_model(self, filepath):
        """Tải mô hình từ file
        
        Args:
            filepath (str): Đường dẫn file mô hình
        """
        with open(filepath, 'rb') as f:
            self.pipeline = pickle.load(f)
        print(f"✅ Mô hình đã tải từ {filepath}")
        return self
    
    def get_model_info(self):
        """Lấy thông tin về mô hình"""
        if self.pipeline is None:
            return {'status': 'No model loaded'}
        
        return {
            'model_type': 'Naive Bayes Classifier',
            'vectorizer_type': type(self.vectorizer).__name__,
            'max_features': self.vectorizer.max_features if hasattr(self.vectorizer, 'max_features') else 'N/A',
            'status': 'Ready for prediction'
        }


if __name__ == "__main__":
    # Test mô hình
    classifier = SpamClassifier()
    classifier.create_pipeline()
    
    # Dữ liệu mẫu để test
    test_texts = [
        "This is a normal message",
        "Click here to CLAIM YOUR FREE PRIZE NOW!!!",
        "Let's meet tomorrow",
        "You have won $1,000,000! Claim your reward"
    ]
    test_labels = [0, 1, 0, 1]
    
    classifier.train(test_texts, test_labels)
    
    # Dự đoán
    result = classifier.predict("Hello, how are you?")
    print(f"Prediction: {result}")
