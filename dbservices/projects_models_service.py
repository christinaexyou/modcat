import psycopg2
from services.connection_pool_singleton import ConnectionPoolSingleton
from dataobjects.dbobject_utils import DBObjectUtils


class ProjectsModelsService:

    GET_ALL_PROJECTS_MODELS = """select * from projectsmodels order by timestamp"""
    GET_PROJECTS_BY_MODELS = """select projectid from projectsmodels where modelid=%s"""

    @staticmethod
    def get_all_projects_models():
        """Get all ProjectsModels in the PROJECTSMODELS table
        :return: List of ProjectsModels objects ordered by timestamp.  Return empty list if no ProjectsModels found.
        """

        pool = ConnectionPoolSingleton.getConnectionPool()
        conn = pool.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute(ProjectsModelsService.GET_ALL_PROJECTS_MODELS)
            all_rows = cursor.fetchall()
            projects_models_list = []
            for row in all_rows:
                # Call on utility function to create a ModelsUsers object from a tuple
                # of column values.
                projectsmodel = DBObjectUtils.models_users_utility(row)
                projectsmodel.append(projectsmodel)
            return projects_models_list
        except (Exception, psycopg2.DatabaseError) as err:
            print(err)
        finally:
            if cursor is not None:
                cursor.close()
            pool.putconn(conn)

    @staticmethod
    def get_projects_by_modelid(modelid):
        """
        Get a list of project ids with the given modelid
        :param modelid: Id of model
        :return: List that contains all project ids for the given modelid
                 Return Empty list if no project ids exists with given model
        """
        pool = ConnectionPoolSingleton.getConnectionPool()
        conn = pool.getconn()
        model_id_list = []
        try:
            cursor = conn.cursor()
            # The execute() method's second parameter is a tuple that contains the param value of the user id.
            cursor.execute(ProjectsModelsService.GET_PROJECTS_BY_MODELS, (modelid,))
            rows = cursor.fetchall()
            for row in rows:
                projectid = row[0]
                model_id_list.append(projectid)
            return model_id_list
        except (Exception, psycopg2.DatabaseError) as err:
            print(err)

        finally:
            if cursor is not None:
                cursor.close()
            pool.putconn(conn)