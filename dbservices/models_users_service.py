import psycopg2
from services.connection_pool_singleton import ConnectionPoolSingleton
from dataobjects.dbobject_utils import DBObjectUtils


class ModelsUsersService:

    GET_ALL_MODELS_USERS = """select * from modelsusers order by timestamp"""
    GET_MODELS_BY_USERID = """select modelid from modelsusers where userid=%s"""

    @staticmethod
    def get_all_model_users():
        """Get all modelsusers in the MODELSUSERS table
        :return: List of ModelsUsers objects ordered by timestamp.  Return empty list if no modelsusers found.
        """

        pool = ConnectionPoolSingleton.getConnectionPool()
        conn = pool.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute(ModelsUsersService.GET_ALL_MODELS_USERS)
            all_rows = cursor.fetchall()
            models_users_list = []
            for row in all_rows:
                # Call on utility function to create a ModelsUsers object from a tuple
                # of column values.
                modelsuser = DBObjectUtils.models_users_utility(row)
                models_users_list.append(modelsuser)
            return models_users_list
        except (Exception, psycopg2.DatabaseError) as err:
            print(err)
        finally:
            if cursor is not None:
                cursor.close()
            pool.putconn(conn)

    @staticmethod
    def get_modelids_by_userid(userid):
        """
        Get a list of model ids with the given userid
        :param userid: Id of user
        :return: List that contains all model ids for the given userid
                 Return Empty list if no modelids exists with given userid
        """
        pool = ConnectionPoolSingleton.getConnectionPool()
        conn = pool.getconn()
        model_id_list = []
        try:
            cursor = conn.cursor()
            # The execute() method's second parameter is a tuple that contains the param value of the user id.
            cursor.execute(ModelsUsersService.GET_MODELS_BY_USERID, (userid,))
            rows = cursor.fetchall()
            for row in rows:
                modelid = row[0]
                model_id_list.append(modelid)
            return model_id_list
        except (Exception, psycopg2.DatabaseError) as err:
            print(err)

        finally:
            if cursor is not None:
                cursor.close()
            pool.putconn(conn)