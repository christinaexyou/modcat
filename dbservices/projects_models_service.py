import psycopg2
from services.connection_pool_singleton import ConnectionPoolSingleton
from dataobjects.dbobject_utils import DBObjectUtils
import pandas as pd


class ProjectsModelsService:

    GET_ALL_PROJECTS_MODELS = """select * from projectsmodels order by timestamp"""
    GET_PROJECTS_BY_MODELS = """select projectid from projectsmodels where modelid=%s"""
    GET_MODELS_BY_TEAMS = """select projects.projectid, models.modelid, modelname  from projects, models, 
                                projectsmodels where models.modelid = projectsmodels.modelid and
                                projects.projectid = projectsmodels.projectid and projects.projectid 
                                in (select projectid from teamsprojects where teamid in {teamids})"""
    INSERT_NEW_PROJECTS_MODELS  = """insert into projectsmodels (projectid, modelid, timestamp) \
                                         values (%s, %s, %s)"""
    UPDATE_PROJECTS_MODELS = """"update projectsmodels set projectid =%s, modelid=%s, timestamp=%s \
                                    projects_modelsid=%s"""
    DELETE_PROJECTS_MODELS = """delete from projectsmodels where projects_modelsid=%s"""

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

    @staticmethod
    def get_models_by_teams(teamids):
        pool = ConnectionPoolSingleton.getConnectionPool()
        conn = pool.getconn()

        dict_array = []
        try:
            cursor = conn.cursor()
            # The execute() method's second parameter is a tuple that contains the param value of the user id.
            final_sql = ProjectsModelsService.GET_MODELS_BY_TEAMS.format(teamids=tuple(teamids))
            print(cursor.mogrify(final_sql, teamids).decode('utf8'))
            cursor.execute(final_sql, teamids)
            rows = cursor.fetchall()
            for row in rows:
                projectid = row[0]
                modelid = row[1]
                modelname = row[2]
                row_dict = {'projectid': projectid, 'modelid': modelid, 'modelname': modelname}
                dict_array.append(row_dict)

            return pd.DataFrame.from_records(dict_array)
        except (Exception, psycopg2.DatabaseError) as err:
            print(err)

        finally:
            if cursor is not None:
                cursor.close()
            pool.putconn(conn)

    @staticmethod
    def create_or_update_projects_models(projectsmodels):
        """"
        Creates or updates a project. If the project exists (by projectid) for a given modelid in PROJECTSMODELS table, 
        then update with data contained in the given project and model. If the project does not exist (by projectid) 
        then a new row is created in PROJECTSMODELS table with the contained data in the given project and model.
        """
        pool = ConnectionPoolSingleton.getConnectionPool()
        conn = pool.getconn()
        try:
            potential_project_model = ProjectsModelsService.get_projects_by_modelid(projectsmodels.modelsid)
            cursor = conn.cursor()
            project_model_as_tuple = DBObjectUtils.projects_models_tuple_utility(projectsmodels)
            # Drop first and last column in tuple since they are projectsmodelsid and timestamp
            project_model_as_tuple = project_model_as_tuple[1: len(project_model_as_tuple) - 1]
            if potential_project_model is None:
                cursor.execute(ProjectsModelsService.INSERT_NEW_PROJECTS_MODELS, project_model_as_tuple)
            else:
                project_model_as_tuple = DBObjectUtils.projects_models_tuple_utility(projectsmodels)
                cursor.execute(ProjectsModelsService.UPDATE_PROJECTS_MODELS, project_model_as_tuple)
            conn.commit()
            return True
        except(Exception, psycopg2.DatabaseError) as err:
            print("Error in create_or_update_projects_models(): {}".format(err))
            return False
        finally:
            if cursor is not None:
                cursor.close()
            pool.putconn(conn)

    @staticmethod
    def delete_projects_models(projectsmodelsid):
        """
        DELETE projectmodel from PROJECTSMODELS table given projectsmodelsid
        CAUTION:  THIS METHOD SHOULD NOT BE USED EXCEPT FOR TESTING.  THERE IS NO USE CASE FOR DELETION OF A PROJECTMODEL
        :param userid: Id of projectmodel to delete
        :return: True if deletion was successful, False otherwise
        """
        pool = ConnectionPoolSingleton.getConnectionPool()
        conn = pool.getconn()
        try:
            cursor = conn.cursor
            cursor.execute(ProjectsModelsService.DELETE_PROJECTS_MODELS, (projectsmodelsid,))
            conn.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as err:
            print(err)
            return False
        finally:
            if cursor is not None:
                cursor.close()
            pool.putconn(conn)