try:
    from decouple import config
    print("Decouple module is working correctly.")
except ImportError as e:
    print(f"Error: {e}")