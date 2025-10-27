import warnings
warnings.filterwarnings('ignore')

print("Testing NLP libraries...")

try:
    # Test NLTK
    import nltk
    print("SUCCESS: NLTK imported")
    
    # Test scikit-learn  
    from sklearn.feature_extraction.text import TfidfVectorizer
    print("SUCCESS: Scikit-learn text processing imported")
    
    # Test basic functionality
    vectorizer = TfidfVectorizer()
    test_texts = ["play music", "open google", "take screenshot"]
    vectors = vectorizer.fit_transform(test_texts)
    print("SUCCESS: Text vectorization working")
    
    print("\nRESULT: All NLP libraries are functional!")
    print("Ready to proceed with NLP implementation.")
    
except Exception as e:
    print(f"FAILED: {e}")