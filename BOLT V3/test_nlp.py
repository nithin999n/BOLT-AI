# Test if our NLP libraries work
try:
    import nltk
    print("NLTK imported successfully")
    
    import sklearn
    print("Scikit-learn imported successfully")
    
    # Try basic NLTK functionality
    from nltk.tokenize import word_tokenize
    print("NLTK tokenization available")
    
    from sklearn.feature_extraction.text import TfidfVectorizer
    print("Scikit-learn text processing available")
    
    print("\nAll basic NLP libraries are working!")
    print("We can proceed with NLP implementation without spacy")
    
except Exception as e:
    print(f"Error: {e}")