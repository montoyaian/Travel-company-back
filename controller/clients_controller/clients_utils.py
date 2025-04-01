from database.db_utils import DatabaseUtils

class UserUtils:
    @staticmethod
    def check_user_by_id(id: int) -> bool:
        db_utils = DatabaseUtils()
        query = """
            SELECT 1 FROM railway.standart_client WHERE id = %s
            UNION
            SELECT 1 FROM railway.premium_client WHERE id = %s
        """
        rows = db_utils.fetch_all(query, (id, id))
        return bool(rows)