

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
