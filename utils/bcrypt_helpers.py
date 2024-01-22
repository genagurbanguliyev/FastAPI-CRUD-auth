from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Use lambda functions
bcrypt_verification = lambda password, hashed_password: bcrypt_context.verify(password, hashed_password)

bcrypt_hash = lambda password: bcrypt_context.hash(password)
