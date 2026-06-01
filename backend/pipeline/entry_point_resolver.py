from models.user import User
from supabase import Client

def resolve_entry_point(user: User, db: Client) -> str:
    """
    Map user's department to their DAG leaf node (entry point).
    """
    if user.department == "admin" or user.department == "quality" or user.role == "ADMIN":
        return "HL-01" # Admin/Quality entry point (root)
        
    response = db.table("hierarchy_levels") \
        .select("id, level_number") \
        .eq("org_id", user.org_id) \
        .eq("department", user.department) \
        .order("level_number", desc=True) \
        .execute()
        
    if not response.data:
        # Fallback if no specific department node is found
        return "HL-01"
        
    # Return the leafiest node (highest level_number) for that department
    return response.data[0]["id"]
