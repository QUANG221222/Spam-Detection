import sys
import json
import requests
from spam_classifier import SpamClassifier

def test_classifier():
    """Test classifier locally without API"""
    print("\n" + "="*60)
    print("🧪 TEST SPAM CLASSIFIER - LOCAL MODE")
    print("="*60 + "\n")
    
    # Initialize classifier
    classifier = SpamClassifier()
    
    # Create pipeline
    print("Creating pipeline...")
    classifier.create_pipeline(use_tfidf=True)
    
    # Train data
    train_texts = [
        "Hello, how are you?",
        "Hi there, let's meet tomorrow",
        "Click here to win FREE MONEY!!!",
        "Congratulations! You won £1000000",
        "Can we schedule a meeting?",
        "URGENT: Update your banking details NOW",
    ]
    train_labels = ["ham", "ham", "spam", "spam", "ham", "spam"]
    
    print(f"Training with {len(train_texts)} samples...\n")
    classifier.train(train_texts, train_labels)
    
    # Test messages
    test_messages = [
        ("Hello buddy", "ham"),
        ("Hello how are you doing", "ham"),
        ("FREE MONEY CLICK NOW", "spam"),
        ("Let's go for coffee tomorrow", "ham"),
        ("CONGRATULATIONS YOU WON PRIZE", "spam"),
        ("What time is the meeting", "ham"),
    ]
    
    print("\n" + "-"*60)
    print("Testing Predictions:")
    print("-"*60)
    
    correct = 0
    for text, expected in test_messages:
        result = classifier.predict(text)
        is_correct = result['prediction'] == expected
        correct += is_correct
        
        status = "✅" if is_correct else "❌"
        print(f"\n{status} Text: {text}")
        print(f"   Expected: {'SPAM' if expected == 'spam' else 'HAM'}")
        print(f"   Predicted: {result['label']}")
        print(f"   Confidence: {result['confidence']*100:.1f}%")
    
    accuracy = (correct / len(test_messages)) * 100
    print(f"\n{'='*60}")
    print(f"Local Test Accuracy: {accuracy:.1f}% ({correct}/{len(test_messages)})")
    print(f"{'='*60}\n")
    
    return accuracy >= 50

def test_api():
    """Test API endpoints"""
    print("\n" + "="*60)
    print("🌐 TEST SPAM DETECTION API")
    print("="*60 + "\n")
    
    API_BASE = "http://localhost:5000/api"
    
    # Test 1: Health Check
    print("1️⃣  Testing /api/health...")
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {data['status']}")
            print(f"   ✅ Model Loaded: {data['model_loaded']}")
        else:
            print(f"   ❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Connection Error: {e}")
        return False
    
    # Test 2: Model Info
    print("\n2️⃣  Testing /api/model-info...")
    try:
        response = requests.get(f"{API_BASE}/model-info", timeout=5)
        if response.status_code == 200:
            data = response.json()
            info = data.get('info', {})
            print(f"   ✅ Model Type: {info.get('model_type')}")
            print(f"   ✅ Status: {info.get('status')}")
        else:
            print(f"   ❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 3: Single Prediction
    print("\n3️⃣  Testing /api/predict (Single Message)...")
    test_text = "Click here to WIN FREE iPHONE!!!"
    try:
        response = requests.post(
            f"{API_BASE}/predict",
            json={"text": test_text},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Input: {test_text}")
            print(f"   ✅ Prediction: {data['label']}")
            print(f"   ✅ Confidence: {data['confidence']*100:.1f}%")
        else:
            print(f"   ❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 4: Batch Prediction
    print("\n4️⃣  Testing /api/predict-batch (Multiple Messages)...")
    test_texts = [
        "Hello how are you?",
        "Click here for FREE PRIZE",
        "Let's meet tomorrow"
    ]
    try:
        response = requests.post(
            f"{API_BASE}/predict-batch",
            json={"texts": test_texts},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Total Messages: {data['total_messages']}")
            print(f"   ✅ Spam Count: {data['spam_count']}")
            print(f"   ✅ Ham Count: {data['ham_count']}")
            print(f"   ✅ Spam Percentage: {data['spam_percentage']}")
        else:
            print(f"   ❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 5: File Upload
    print("\n5️⃣  Testing /api/predict-file (File Upload)...")
    try:
        # Create test file
        test_file_path = "test_upload.txt"
        with open(test_file_path, 'w') as f:
            f.write("Hello there\n")
            f.write("FREE MONEY CLICK NOW\n")
            f.write("How are you doing?\n")
        
        with open(test_file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                f"{API_BASE}/predict-file",
                files=files,
                timeout=5
            )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Processed: {data['total_messages']} messages")
            print(f"   ✅ Spam: {data['spam_count']}")
            print(f"   ✅ Ham: {data['ham_count']}")
        else:
            print(f"   ❌ Error: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    finally:
        # Clean up
        import os
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
    
    print("\n" + "="*60)
    print("✅ ALL API TESTS PASSED!")
    print("="*60 + "\n")
    
    return True

def test_file_upload():
    """Test file upload functionality"""
    print("\n" + "="*60)
    print("📁 TEST FILE UPLOAD")
    print("="*60 + "\n")
    
    # Check if sample test file exists
    sample_file = "data/sample_test.txt"
    
    try:
        with open(sample_file, 'r') as f:
            lines = f.readlines()
        
        print(f"✅ Sample test file found: {len(lines)} messages")
        
        API_BASE = "http://localhost:5000/api"
        
        with open(sample_file, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                f"{API_BASE}/predict-file",
                files=files,
                timeout=10
            )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ File Upload Result:")
            print(f"   Total: {data['total_messages']}")
            print(f"   Spam: {data['spam_count']}")
            print(f"   Ham: {data['ham_count']}")
            print(f"   Spam %: {data['spam_percentage']}")
            return True
        else:
            print(f"❌ Upload failed: {response.status_code}")
            return False
    
    except FileNotFoundError:
        print(f"❌ Sample test file not found: {sample_file}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " 🛡️  SPAM DETECTION SYSTEM - TEST SUITE".center(58) + "║")
    print("╚" + "="*58 + "╝")
    
    # Test local classifier
    print("\n[1/3] Running local classifier tests...")
    local_ok = test_classifier()
    
    # Test API
    print("\n[2/3] Running API endpoint tests...")
    print("Make sure Flask app is running: python app.py")
    
    api_ok = False
    try:
        api_ok = test_api()
    except Exception as e:
        print(f"❌ API Tests Failed: {e}")
    
    # Test file upload
    if api_ok:
        print("\n[3/3] Running file upload tests...")
        file_ok = test_file_upload()
    else:
        file_ok = False
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    print(f"Local Classifier: {'✅ PASSED' if local_ok else '❌ FAILED'}")
    print(f"API Endpoints: {'✅ PASSED' if api_ok else '❌ FAILED'}")
    print(f"File Upload: {'✅ PASSED' if file_ok else '❌ FAILED'}")
    print("="*60)
    
    if local_ok and api_ok and file_ok:
        print("✅ ALL TESTS PASSED - System is working correctly!\n")
        return 0
    else:
        print("❌ Some tests failed - Please check the errors above\n")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)
