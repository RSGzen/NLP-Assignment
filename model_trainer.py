import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib


data = {
    'budget': ['low', 'low', 'low', 'low', 'medium', 'medium', 'medium', 'medium', 'medium', 'medium', 'high', 'high', 'high', 'high', 'high', 'very high', 'very high'],
    'purpose': ['office', 'office', 'gaming', 'programming', 'office', 'gaming', 'gaming', 'design', 'programming', 'streaming', 'gaming', 'design', 'streaming', 'programming', 'ai_development', 'gaming', 'professional'],
    'cpu': ['Ryzen 3 3200G', 'i3-12100', 'Ryzen 5 5600G', 'i5-12400', 'i5-13400', 'Ryzen 5 5600X', 'i5-12600K', 'Ryzen 7 5700X', 'i7-12700', 'Ryzen 7 5800X', 'Ryzen 7 7800X3D', 'i7-13700K', 'Ryzen 9 7900X', 'i9-13900', 'Threadripper 7960X', 'Ryzen 9 7950X3D', 'i9-14900K'],
    'gpu': ['Integrated', 'Integrated', 'RTX 3050', 'RTX A2000', 'GTX 1650', 'RTX 3060', 'RX 6700 XT', 'RTX 4060 Ti', 'RTX 3070', 'RTX 4070', 'RTX 4080', 'RTX 4090', 'RX 7900 XTX', 'RTX A5000', 'RTX 6000 Ada', 'RTX 4090', 'RTX 6000 Ada'],
    'ram': [8, 16, 16, 32, 16, 16, 32, 32, 32, 32, 32, 64, 64, 64, 128, 64, 128],
    'storage': ['256GB SSD', '512GB SSD', '1TB SSD', '512GB NVMe', '1TB HDD + 256GB SSD', '1TB NVMe', '1TB NVMe', '2TB NVMe', '2TB NVMe', '2TB NVMe', '2TB NVMe', '2TB NVMe + 4TB HDD', '2TB NVMe RAID0', '4TB NVMe', '8TB NVMe RAID', '4TB NVMe RAID0', '8TB NVMe RAID'],
    'motherboard': ['A520', 'H610', 'B550', 'B660', 'B760', 'X570', 'Z690', 'X670', 'Z790', 'X670E', 'X670E', 'Z790', 'TRX50', 'WRX80', 'TRX50', 'X670E', 'W790'],
    'psu': ['450W', '500W', '550W', '600W', '650W', '750W', '850W', '750W', '850W', '1000W', '1000W', '1200W', '1200W', '1200W', '1600W', '1600W', '2000W']
}

df = pd.DataFrame(data)

# Encode categorical features
encoders = {}
for col in ['budget', 'purpose']:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

# Encode the target column (e.g., 'cpu')
target_col = 'cpu'
le_target = LabelEncoder()
df[target_col] = le_target.fit_transform(df[target_col])
encoders[target_col] = le_target

# Train model
X = df[['budget', 'purpose']].astype(int)
y = df[target_col].astype(int)

model = RandomForestClassifier()
model.fit(X, y)

# Save model and encoders
joblib.dump(model, 'pc_recommender_model.pkl')
joblib.dump(encoders, 'encoders.pkl')


