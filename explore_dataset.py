#!/usr/bin/env python3
"""
Simple script to explore the dataset
"""

try:
    import pandas as pd
    print("✓ Pandas imported successfully")
    
    # Load dataset
    df = pd.read_csv('augmented_dataset_75000.csv')
    print(f"✓ Dataset loaded successfully")
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"\nFirst 3 rows:")
    print(df.head(3))
    print(f"\nData types:")
    print(df.dtypes)
    print(f"\nMissing values:")
    print(df.isnull().sum())
    
    # Check for label columns
    label_cols = [col for col in df.columns if 'label' in col.lower() or 'depression' in col.lower()]
    print(f"\nLabel columns: {label_cols}")
    
    # Check for text columns
    text_cols = [col for col in df.columns if 'text' in col.lower() or 'transcript' in col.lower()]
    print(f"Text columns: {text_cols}")
    
    # Check for audio columns
    audio_cols = [col for col in df.columns if 'audio' in col.lower() or 'file' in col.lower()]
    print(f"Audio columns: {audio_cols}")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("Please install pandas: pip install pandas")
except Exception as e:
    print(f"✗ Error: {e}")
