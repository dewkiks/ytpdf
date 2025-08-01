# This variable will hold the API key during a user's session.
# It acts as a shared state that other modules can access.
_API_KEY = None

def set_api_key(key: str):
    """
    Sets the Gemini API key for the current session.
    Your Streamlit app will call this function.
    """
    global _API_KEY
    _API_KEY = key

def get_api_key() -> str:
    """
    Retrieves the currently set Gemini API key.
    Any other module (like younote.py) will call this.
    """
    return _API_KEY