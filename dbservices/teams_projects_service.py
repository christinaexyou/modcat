

import psycopg2
from psycopg2 import sql
from services.connection_pool_singleton import ConnectionPoolSingleton
from dataobjects.dbobject_utils import DBObjectUtils
import pandas as pd


class TeamsProjectsService:

    GET_ALL_TEAMS_PROJECTS = """select * from teamsprojects order by timestamp"""
    GET_PROJECT_IDS_BY_TEAM = """select projectid from teamsprojects where teamid=%s"""
    GET_PROJECTS_BY_TEAMS = """select teamsprojects.teamid,projects.projectid, projectname   
                                    from projects,   teamsprojects  
                                    where 
                                        projects.projectid = teamsprojects.projectid and projects.projectid 
                                        in (select projectid from teamsprojects where teamid in {teamids}) 
                                    order by teamsprojects.teamid;"""
    INSERT_NEW_TEAMS_PROJECTS = """insert into teamsprojects (teamid, projectid, timestamp) values \
                                        (%s, %s, %s)"""
    UPDATE_TEAMS_PROJECTS = """update teamsprojects set teamid=%s, projectid=%s, timestamp=%s where \
                                        where teamsprojects=%s """
    DELETE_TEAMS_PROJECTS = """delete from teamsprojects where teamsprojectsid=%s"""


    @staticmethod
    def get_all_teams_projects():
        """Get all TeamsProjects in the TEAMSPROJECTS table
        :return: List of TeamsProjects objects ordered by timestamp.  Return empty list if no TeamsProjects found.
        """

        pool = ConnectionPoolSingleton.getConnectionPool()
        conn = pool.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute(TeamsProjectsService.GET_ALL_TEAMS_PROJECTS)
            all_rows = cursor.fetchall()
            teams_projects_list = []
            for row in all_rows:
                # Call on utility function to create a TeamsProjects object from a tuple
                # of column values.
                teamsprojects = DBObjectUtils.teams_projects_utility(row)
                teams_projects_list.append(teamsprojects)
            return teams_projects_list
        except (Exception, psycopg2.DatabaseError) as err:
            print(err)
        finally:
            if cursor is not None:
                cursor.close()
            pool.putconn(conn)

    @staticmethod
    def get_project_df(teamids):
        """
        Get a list of project ids with the given teamid from the TEAMSPROJECTS table
        :param teamids: tuple of team ids
        :return: DataFrame
        """
        pool = ConnectionPoolSingleton.getConnectionPool()
        conn = pool.getconn()

        dict_array = []
        try:
            cursor = conn.cursor()
            # The execute() method's second parameter is a tuple that contains the param value of the user id.
            final_sql = TeamsProjectsService.GET_PROJECTS_BY_TEAMS.format(teamids=tuple(teamids))

            print(cursor.mogrify(final_sql).decode('utf8'))
            cursor.execute(final_sql)
            rows = cursor.fetchall()
            for row in rows:
                teamid = row[0]
                projectid = row[1]
                projectname = row[2]
                row_dict = {'teamid': teamid, 'projectid': projectid, 'projectname': projectname}
                dict_array.append(row_dict)

            return pd.DataFrame.from_records(dict_array)
        except (Exception, psycopg2.DatabaseError) as err:
            print(err)

        finally:
            if cursor is not None:
                cursor.close()
            pool.putconn(conn)

    @staticmethod
    def get_project_ids_by_team(teamid):
        """

        :param teamids: tuple of teamids
        :return:
        """
        pool = ConnectionPoolSingleton.getConnectionPool()
        conn = pool.getconn()

        project_id_list = []
        try:
            cursor = conn.cursor()
            # The execute() method's second parameter is a tuple that contains the param value of the user id.
            cursor.execute(TeamsProjectsService.GET_PROJECT_IDS_BY_TEAM, teamid)
            rows = cursor.fetchall()
            for row in rows:
                projectid = row[0]
                project_id_list.append(projectid)
            return project_id_list
        except (Exception, psycopg2.DatabaseError) as err:
            print(err)

        finally:
            if cursor is not None:
                cursor.close()
            pool.putconn(conn)

    @staticmethod 
    def create_or_update_teams_projects(teamsprojects):
        """"
        Creates or updates a project for a given team. If the project exists (by projectid) for a given teamid in TEAMSPROJECTS table, 
        then update with data contained in the given team and project. If the project does not exist (by projectid) 
        then a new row is created in TEAMSPROJECTS table with the contained data in the given team and prohect.
        """
        pool = ConnectionPoolSingleton.getConnectionPool()
        conn = pool.getconn()
        try:
            potential_team_project = TeamsProjectsService.get_project_ids_by_team(teamsprojects.teamid)
            cursor = conn.cursor()
            teamsprojects_as_tuple = DBObjectUtils.teams_projects_tuple_utility(teamsprojects)
            # Drop first column and columns since they are teamsprojectid and timestamp
            teamsprojects_as_tuple = teamsprojects_as_tuple[1:len(teamsprojects_as_tuple) - 1]
            if potential_team_project is None:
                cursor.execute(TeamsProjectsService.INSERT_NEW_TEAMS_PROJECTS, teamsprojects_as_tuple)
            else:
                teamsprojects_as_tuple = DBObjectUtils.teams_projects_tuple_utility(teamsprojects)
                cursor.execute(TeamsProjectsService.UPDATE_TEAMS_PROJECTS, teamsprojects_as_tuple)
            conn.commit()
            return True 
        except (Exception, psycopg2.DatabaseError) as err:
            print("Error in create_or_update_teams_projects(): {}".format(err))
            return False 
        finally:
            if cursor is not None:
                cursor.close()
            pool.putconn(conn)

    def delete_teams_projects(teamsprojectsid):
        """
        Delete user from USER table given userid
        CAUTION:  THIS METHOD SHOULD NOT BE USED EXCEPT FOR TESTING.  THERE IS NO USE CASE FOR DELETION OF A USER
        :param userid: Id of user to delete
        :return: True if deletion was successful, False otherwise
        """
        pool = ConnectionPoolSingleton.getConnectionPool()
        conn = pool.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute(TeamsProjectsService.DELETE_TEAMS_PROJECTS, (teamsprojectsid,))
            conn.commit()
            return True
        except(Exception, psycopg2.DatabaseError) as err:
            print(err)
            return False
        finally: 
            if cursor is not None:
                cursor.close()
            pool.putconn(conn)



            
