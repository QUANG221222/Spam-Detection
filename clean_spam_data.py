import csv
import pandas as pd

# Đọc file spam.csv hiện tại (thử nhiều encoding)
try:
    df = pd.read_csv('data/spam.csv', usecols=[0, 1], engine='python', encoding='latin-1')
except:
    try:
        df = pd.read_csv('data/spam.csv', usecols=[0, 1], engine='python', encoding='cp1252')
    except:
        df = pd.read_csv('data/spam.csv', usecols=[0, 1], engine='python', encoding='iso-8859-1')

# Đổi tên cột
df.columns = ['label', 'text']

# Loại bỏ cột thừa
df = df[['label', 'text']]

# Làm sạch dữ liệu
df['label'] = df['label'].astype(str).str.strip().str.lower()
df['text'] = df['text'].astype(str).str.strip()

# Xóa dòng trống
df = df.dropna(subset=['text'])
df = df[df['text'] != '']
df = df[df['label'] != 'nan']

# Lưu lại dưới dạng chuẩn (encoding UTF-8)
df.to_csv('data/spam.csv', index=False, quoting=csv.QUOTE_MINIMAL, encoding='utf-8')

print(f"✅ Chuẩn hóa file spam.csv")
print(f"   - Tổng dòng: {len(df)}")
print(f"   - Ham: {(df['label']=='ham').sum()}")
print(f"   - Spam: {(df['label']=='spam').sum()}")
print(f"\n📋 5 dòng đầu tiên:")
print(df.head())
