import psycopg2
from dataobjects.project import Project
from dataobjects.dbobject_utils import DBObjectUtils
from services.connection_pool_singleton import ConnectionPoolSingleton
class ProjectService:
    """This class provides static methods that give access to the PROJECT table."""
    # User table cols: projectid, teamid, modelid, projectname

    GET_PROJECT_BY_ID = """Select * from projects where projectid=%s"""

    @staticmethod
    def get_project_by_projectid(projectid):
        """
        Get a User with given userid
        :param projectid: Id of project
        :return: Project object that contains all project info for the given projectid
                 Return None if no Project exists with given projectid
        """
        pool = ConnectionPoolSingleton.getConnectionPool()
        conn = pool.getconn()
        try:
            cursor = conn.cursor()
            # The execute() method's second parameter is a tuple that contains the param value of the user id.
            cursor.execute(ProjectService.GET_PROJECT_BY_ID, (projectid,))
            one_project_tuple = cursor.fetchone()
            if one_project_tuple is not None:
                project = DBObjectUtils.project_utility(one_project_tuple)
                return project
            else:
                return None

        except (Exception, psycopg2.DatabaseError) as err:
            print(err)

        finally:
            if cursor is not None:
                cursor.close()
            pool.putconn(conn)

