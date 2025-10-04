from fastapi import Depends, HTTPException, status
from security.dependencies import get_current_user

def get_has_role(*roles):
    def role_dependency(current_user = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para acceder a este recurso"
            )
        return current_user
    return Depends(role_dependency)

