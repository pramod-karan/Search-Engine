

# Secret key for JWT (replace with a secure key)
SECRET_KEY = "intel"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time in minutes



# MongoDB configuration
MONGODB_URL = "mongodb://localhost:27017"  # Replace with your MongoDB connection string
DATABASE_NAME = "intel_db"


# Logged-in users dictionary to track active sessions
logged_in_users = {}

#index to be moved to mongo DB
INDEX_NAME = "intel_search"
