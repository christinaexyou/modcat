import psycopg2
from services.connection_pool_singleton import ConnectionPoolSingleton
from dataobjects.dbobject_utils import DBObjectUtils


class TeamService:
    GET_TEAM_BY_TEAM_ID = """select * from teams where teamid=%s"""
    GET_TEAMS_BY_TEAMLEAD_ID = """select * from teams where teamlead_userid=%s"""
    GET_ALL_TEAMS = """select * from teams"""
    INSERT_NEW_TEAM = """insert into teams (teamid, teamname, department, teamlead_userid) values \
                            (%s, %s, %s, %s)"""
    UPDATE_TEAM = """update teams set teamid=%s, teamname=%s, department=%s, teamlead_userid=%s"""
    DELETE_TEAM = """delete from teams where teamid=%s"""
    @staticmethod
    def get_team_by_id(teamid):
        """
                Get a Team object with given teamid
                :param teamid: Id of team
                :return: Team object that contains all team info for the given teamid
                         Return None if no team exists with given teamid
                """
        pool = ConnectionPoolSingleton.getConnectionPool()
        conn = pool.getconn()
        try:
            cursor = conn.cursor()
            # The execute() method's second parameter is a tuple that contains the param value of the team id.
            cursor.execute(TeamService.GET_TEAM_BY_TEAM_ID, (teamid,))
            one_team_tuple = cursor.fetchone()
            if one_team_tuple is not None:
                team = DBObjectUtils.team_utility(one_team_tuple)
                return team
            else:
                return None

        except (Exception, psycopg2.DatabaseError) as err:
            print(err)

        finally:
            if cursor is not None:
                cursor.close()
            pool.putconn(conn)

    @staticmethod
    def get_teams_by_teamlead(teamlead_id):
        """
                Get a list of Team object with given teamlead_id
                :param teamlead_id: Id of team lead
                :return: List of Team objects that contains all team info for the given teamlead_id
                         Return empty list if no team exists with given teamlead_id
                """
        pool = ConnectionPoolSingleton.getConnectionPool()
        conn = pool.getconn()
        team_list = []
        try:
            cursor = conn.cursor()
            # The execute() method's second parameter is a tuple that contains the param value of the team id.
            cursor.execute(TeamService.GET_TEAMS_BY_TEAMLEAD_ID, (teamlead_id,))
            all_rows = cursor.fetchone()
            for row in all_rows:
                # Convert tuple to Team object.
                team = DBObjectUtils.team_utility(row)
                team_list.append(team)
            return team_list
        except (Exception, psycopg2.DatabaseError) as err:
            print(err)
        finally:
            if cursor is not None:
                cursor.close()
            pool.putconn(conn)

    @staticmethod
    def get_all_teams():
        """Get all teams in the TEAMS table
        :return: List of Team objects.  Return empty list if no teams found.
        """

        pool = ConnectionPoolSingleton.getConnectionPool()
        conn = pool.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute(TeamService.GET_ALL_TEAMS)
            all_rows = cursor.fetchall()
            team_list = []
            for row in all_rows:
                # Call on utility function to create a Team object from a tuple
                # of column values.
                team = DBObjectUtils.team_utility(row)
                team_list.append(team)
            return team_list
        except (Exception, psycopg2.DatabaseError) as err:
            print(err)
        finally:
            if cursor is not None:
                cursor.close()
            pool.putconn(conn)

    @staticmethod
    def create_or_update_user(team):
        """
        Creates or updates a team.  If team exists (by teamid) in the TEAMS table, then update with data contained in the
        given team.  If team does not exist (by teamid) then a new row is created in TEAMS table with the data
        contained in the given team
        :param team: A dataobject.Team object with all properties specified
        :return: True if successful, False otherwise
        """
        pool = ConnectionPoolSingleton.getConnectionPool()
        conn = pool.getconn()
        try:
            potential_user = TeamService.get_team_by_id(team.teamid)
            cursor = conn.cursor()
            team_as_tuple = DBObjectUtils.team_tuple_utility(team)
            if potential_user is None:
                cursor.execute(TeamService.INSERT_NEW_TEAM, team_as_tuple)
            else:
                team_as_tuple = DBObjectUtils.user_tuple_utility(team)
                query_values_tuple = team_as_tuple + (team.teamid,)
                cursor.execute(TeamService.UPDATE_TEAM, query_values_tuple)
            conn.commit()
            return True
        except(Exception, psycopg2.DatabaseError) as err:
            print(err)
            return False
        finally:
            if cursor is not None:
                cursor.close()
            pool.putconn(conn)

    @staticmethod
    def delete_team(teamid):
        """
        Delete team from TEAMS table given teamid
        CAUTION:  THIS METHOD SHOULD NOT BE USED EXCEPT FOR TESTING.  THERE IS NO USE CASE FOR DELETION OF A TEAM
        :param teamid: Id of team to delete
        :return: True if deletion was successful, False otherwise
        """
        pool = ConnectionPoolSingleton.getConnectionPool()
        conn = pool.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute(TeamService.DELETE_TEAM, (teamid,))
            conn.commit()
            return True
        except(Exception, psycopg2.DatabaseError) as err:
            print(err)
            return False
        finally:
            if cursor is not None:
                cursor.close()
            pool.putconn(conn)