from passlib.context import CryptContext
################################################################################

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

################################################################################
def hash(password: str) -> str:
    
    return pwd_ctx.hash(password)

################################################################################
def verify(password: str, pwd_hash: str) -> bool:
    
    return pwd_ctx.verify(password, pwd_hash)

################################################################################
