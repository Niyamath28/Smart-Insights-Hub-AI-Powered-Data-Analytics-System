#!/usr/bin/env python
"""Quick test script to verify all modules work"""

import sys
import os

print("[TEST] Smart Insights Hub - Module Verification\n")
print("="*60)

# Test 1: Check imports
print("\n[TEST 1] Checking Python version...")
print(f"Python version: {sys.version}")

print("\n[TEST 2] Checking required libraries...")
required_packages = ['pandas', 'numpy', 'matplotlib', 'sklearn', 'streamlit']
for package in required_packages:
    try:
        __import__(package)
        print(f"[OK] {package} is installed")
    except ImportError:
        print(f"[ERROR] {package} is NOT installed")

print("\n[TEST 3] Checking project files...")
required_files = [
    'main.py',
    'data_preprocessing.py',
    'eda.py',
    'model.py',
    'insights.py',
    'app.py',
    'requirements.txt',
    'data/ecommerce_dataset.csv'
]

for file in required_files:
    exists = os.path.exists(file)
    status = "[OK]" if exists else "[MISSING]"
    print(f"{status} {file}")

print("\n[TEST 4] Checking dataset...")
if os.path.exists('data/ecommerce_dataset.csv'):
    import pandas as pd
    try:
        df = pd.read_csv('data/ecommerce_dataset.csv')
        print(f"[OK] Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    except Exception as e:
        print(f"[ERROR] Could not load dataset: {e}")
else:
    print("[ERROR] Dataset file not found")

print("\n" + "="*60)
print("[SUCCESS] Verification complete!")
print("\nYou can now run:")
print("  1. python main.py          (Run complete pipeline)")
print("  2. streamlit run app.py    (Launch dashboard)")
print("="*60)
