def create_user(username: str, password: str):
    """Create a new user for the secure file transfer system"""
    auth = Authentication(secret_key="your_secret_key")  # Use the actual secret key
    
    # Hash the password
    hashed_password = auth.hash_password(password)
    
    # Store user data
    user_data = {
        "username": username,
        "password": hashed_password.decode(),
        "created_at": time.time()
    }
    
    user_file = Path(f"users/{username}.json")
    with open(user_file, "w") as f:
        json.dump(user_data, f)
    
    print(f"User {username} created successfully!")