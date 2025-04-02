from database.db_utils import DatabaseUtils



def findflight(id:int,db_utils:DatabaseUtils,flightType:str):

    query = f"""SELECT * FROM railway.{flightType} WHERE id = %s"""

    result = db_utils.execute_query(query,id)

    return True if result else False