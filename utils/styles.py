def load_css():
    return """
    <style>
        .main {
            padding: 2rem;
        }
        
        .stButton button {
            width: 100%;
            padding: 1rem;
            border-radius: 10px;
            border: 1px solid #e0e0e0;
            background-color: white;
            transition: all 0.3s ease;
        }
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .success-message {
            padding: 1rem;
            border-radius: 10px;
            background-color: #d4edda;
            color: #155724;
            margin: 1rem 0;
        }
        
        .link-container {
            padding: 1rem;
            border-radius: 10px;
            border: 1px solid #e0e0e0;
            margin: 0.5rem 0;
        }
        
        .custom-button {
            background-color: #4CAF50;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            text-decoration: none;
            transition: background-color 0.3s ease;
        }
        .custom-button:hover {
            background-color: #45a049;
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        .stForm > div {
            margin-bottom: 1.5rem;
        }
        
        .stTextInput > div > div > input {
            border-radius: 5px;
        }
        
        .user-container {
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
        background-color: #f8f9fa;
        }
        
        .user-container h3 {
            margin: 0;
            color: #1a1a1a;
        }
        
        .user-container p {
            margin: 0.25rem 0;
            color: #666;
        }
    </style>
    """