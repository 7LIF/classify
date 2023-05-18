################################################################################
##      Specifies the public interface of this module
################################################################################

__all__ = (
    'hash_password'
)





# simula - TEMPORARIAMENTE
def hash_password(password: str) -> str:
    return password + '-hashpw'