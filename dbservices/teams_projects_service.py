

import psycopg2
from services.connection_pool_singleton import ConnectionPoolSingleton
from dataobjects.dbobject_utils import DBObjectUtils


class TeamsProjectsService:

    GET_ALL_TEAMS_PROJECTS = """select * from teamsprojects order by timestamp"""
    GET_PROJECTS_BY_TEAM = """select projectid from teamsprojects where teamid=%s"""

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
    def get_projectids_by_team_id(teamid):
        """
        Get a list of project ids with the given teamid from the TEAMSPROJECTS table
        :param teamid: Id of team
        :return: List that contains all project ids for the given teamid
                 Return Empty list if no modelids exists with given teamid
        """
        pool = ConnectionPoolSingleton.getConnectionPool()
        conn = pool.getconn()
        project_id_list = []
        try:
            cursor = conn.cursor()
            # The execute() method's second parameter is a tuple that contains the param value of the user id.
            cursor.execute(TeamsProjectsService.GET_PROJECTS_BY_TEAM, (teamid,))
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
