import pandas as pd
import os

# Define local folders
v1_path = "data/v1/data.csv"
v2_path = "data/v2/data.csv"
output_dir = "data"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "data.csv")

# ✅ Load both versions
print("📥 Loading v1 and v2 datasets...")
df_v1 = pd.read_csv(v1_path)
df_v2 = pd.read_csv(v2_path)

# ✅ Merge / augment data
print("🔄 Merging datasets...")
df_merged = pd.concat([df_v1, df_v2], ignore_index=True)

# ✅ Save merged data
df_merged.to_csv(output_file, index=False)

print(f"✅ Merged dataset saved at: {output_file}")
print(f"Total rows after merge: {df_merged.shape[0]}")
print(f"Columns: {list(df_merged.columns)}")
