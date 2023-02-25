import psycopg2
from dataobjects.dbobject_utils import DBObjectUtils
from services.connection_pool_singleton import ConnectionPoolSingleton

class TeamsUsersService:
    GET_TEAM_IDS_FOR_USER = """select teamid from teamsusers where userid=%s"""

    @staticmethod
    def get_team_ids_by_user(userid):
        """
        Get a list of teamids for which the given user belongs
        :param userid: Id of user
        :return: List of teamids (integers)
        """

        pool = ConnectionPoolSingleton.getConnectionPool()
        conn = pool.getconn()
        team_ids = []
        try:
            cursor = conn.cursor()
            # The execute() method's second parameter is a tuple that contains the param value of the user id.
            cursor.execute(TeamsUsersService.GET_TEAM_IDS_FOR_USER, (userid,))
            rows = cursor.fetchall()
            for row in rows:
                teamid = row[0]
                team_ids.append(teamid)
            return team_ids
        except (Exception, psycopg2.DatabaseError) as err:
            print(err)
        finally:
            if cursor is not None:
                cursor.close()
            pool.putconn(conn)