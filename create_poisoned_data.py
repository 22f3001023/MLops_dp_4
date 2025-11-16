import pandas as pd
import numpy as np
import os
from sklearn.datasets import load_iris

def poison_data(df, poison_level):
    """Randomly changes the 'target' label for a percentage of the data."""
    
    # Make a copy so we don't change the original data
    poisoned_df = df.copy()
    
    # Get the number of rows to poison
    num_to_poison = int(len(poisoned_df) * poison_level)
    
    # Get the indices of the rows to poison
    poison_indices = np.random.choice(poisoned_df.index, num_to_poison, replace=False)
    
    num_classes = poisoned_df['target'].nunique()
    
    print(f"Poisoning {num_to_poison} rows...")
    
    for idx in poison_indices:
        # Get the original (correct) label
        original_label = poisoned_df.loc[idx, 'target']
        
        # Create a new, incorrect label.
        # This simple logic adds 1 (or 2) and wraps around (e.g., 0->1, 1->2, 2->0)
        # This guarantees the new label is different from the old one.
        new_label = (original_label + np.random.randint(1, num_classes)) % num_classes
        
        # Apply the poison
        poisoned_df.loc[idx, 'target'] = new_label
        
    return poisoned_df

def main():
    # 1. Load the original IRIS data
    iris = load_iris()
    df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    df['target'] = iris.target
    
    # 2. Create the 'data' directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # 3. Save the original, clean data
    original_path = 'data/iris_original.csv'
    df.to_csv(original_path, index=False)
    print(f"Saved original data to {original_path}")
    
    # 4. Create and save poisoned datasets
    poison_levels = [0.05, 0.10, 0.50] # 5%, 10%, 50%
    
    for level in poison_levels:
        poisoned_df = poison_data(df, level)
        file_path = f'data/iris_poisoned_{int(level*100)}.csv'
        poisoned_df.to_csv(file_path, index=False)
        print(f"Saved {level*100}% poisoned data to {file_path}")

if __name__ == "__main__":
    main()
