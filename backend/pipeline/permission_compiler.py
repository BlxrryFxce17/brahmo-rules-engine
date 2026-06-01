from models.user import User
from typing import Dict

def compile_permissions(user: User) -> Dict[int, Dict[str, bool]]:
    """
    Compile user permissions into an O(1) lookup dictionary.
    Output: {level_number: {can_read: bool, can_write: bool}}
    """
    permissions = {}
    for level in range(1, 16):
        can_read = False
        can_write = False
        
        if user.role == 'VIEWER':
            if level >= user.ceiling_level:
                can_read = True
            can_write = False
        elif user.role == 'EDITOR':
            if level >= user.ceiling_level:
                can_read = True
            if user.write_ceiling and level >= user.write_ceiling:
                can_write = True
        elif user.role == 'HOD':
            can_read = True # HOD can read all levels
            if user.write_ceiling and level >= user.write_ceiling:
                can_write = True
        elif user.role == 'ADMIN':
            can_read = True
            can_write = True
        elif user.role == 'QUALITY':
            if level >= user.ceiling_level:
                can_read = True
            if user.write_ceiling and level >= user.write_ceiling:
                can_write = True
        elif user.role == 'AUDITOR':
            if level >= user.ceiling_level:
                can_read = True
            can_write = False
            
        permissions[level] = {"can_read": can_read, "can_write": can_write}
    
    return permissions
