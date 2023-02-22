import psycopg2
from dataobjects.dbobject_utils import DBObjectUtils
from services.connection_pool_singleton import ConnectionPoolSingleton

class UserService:
    """This class provides static methods that give access to the USERS table."""
    # User table cols: teamid, projectid, userid, roleid, firstname, lastname, email, username, password
    GET_ALL_USERS = """select * from users order by lastname"""
    GET_USER_BY_USERNAME = """select * from users where username like %s"""
    GET_USER_BY_USER_ID = """select * from users where userid=%s"""
    INSERT_NEW_USER = """insert into users (teamid, projectid, userid, roleid, firstname, lastname, email, username, password)\
                            values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    UPDATE_USER = """update users set teamid=%s, projectid=%s, userid=%s, roleid=%s, firstname=%s, lastname=%s,\
                        email=%s, username=%s, password=%s where userid=%s"""
    DELETE_USER = """delete from users where userid=%s"""

    @staticmethod
    def get_all_users():
        """Get all users in the USERS table
        :return: List of User objects ordered by users' last name.  Return empty list if no users found.
        """

        pool = ConnectionPoolSingleton.getConnectionPool()
        conn = pool.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute(UserService.GET_ALL_USERS)
            all_rows = cursor.fetchall()
            user_list = []
            for row in all_rows:
                # Call on utility function to create a User object from a tuple
                # of column values.
                user = UserService.user_utility(row)
                user_list.append(user)
            return user_list
        except (Exception, psycopg2.DatabaseError) as err:
            print(err)
        finally:
            if cursor is not None:
                cursor.close()
            pool.putconn(conn)

    @staticmethod
    def get_user_by_username(username):
        """
        Get a User given the username
        :param username: User's username (String)
        :return: User object that contains all user info for the given username
                 Return None if no user exists with given username
        """
        pool = ConnectionPoolSingleton.getConnectionPool()
        conn = pool.getconn()
        try:
            cursor = conn.cursor()
            # The execute() method's second parameter is a tuple that contains the param value of the username
            cursor.execute(UserService.GET_USER_BY_USERNAME, (username,))
            one_user_tuple = cursor.fetchone()
            if one_user_tuple is not None:
                user = DBObjectUtils.user_utility(one_user_tuple)
                return user
            else:
                return None

        except (Exception, psycopg2.DatabaseError) as err:
            print(err)

        finally:
            if cursor is not None:
                cursor.close()
            pool.putconn(conn)

    @staticmethod
    def get_user_by_userid(userid):
        """
        Get a User with given userid
        :param userid: Id of user
        :return: User object that contains all user info for the given userid
                 Return None if no user exists with given userid
        """
        pool = ConnectionPoolSingleton.getConnectionPool()
        conn = pool.getconn()
        try:
            cursor = conn.cursor()
            # The execute() method's second parameter is a tuple that contains the param value of the user id.
            cursor.execute(UserService.GET_USER_BY_USER_ID, (userid,))
            one_user_tuple = cursor.fetchone()
            if one_user_tuple is not None:
                user = DBObjectUtils.user_utility(one_user_tuple)
                return user
            else:
                return None

        except (Exception, psycopg2.DatabaseError) as err:
            print(err)

        finally:
            if cursor is not None:
                cursor.close()
            pool.putconn(conn)

    @staticmethod
    def create_or_update_user(user):
        """
        Creates or updates a user.  If user exists (by userid) in the USERS table, then update with data contained in the
        given user.  If user does not exist (by userid) then a new row is created in USERS table with the data
        contained in the given user
        :param user: A dataobject.User object with all properties specified
        :return: True if successful, False otherwise
        """
        pool = ConnectionPoolSingleton.getConnectionPool()
        conn = pool.getconn()
        try:
            potential_user = UserService.get_user_by_userid(user.userid)
            cursor = conn.cursor()
            user_as_tuple = DBObjectUtils.user_tuple_utility(user)
            if potential_user is None:
                cursor.execute(UserService.INSERT_NEW_USER, user_as_tuple)
            else:
                user_as_tuple = DBObjectUtils.user_tuple_utility(user)
                query_values_tuple = user_as_tuple + (user.userid,)
                cursor.execute(UserService.UPDATE_USER, query_values_tuple)
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
    def delete_user(userid):
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
            cursor.execute(UserService.DELETE_USER, (userid,))
            conn.commit()
            return True
        except(Exception, psycopg2.DatabaseError) as err:
            print(err)
            return False
        finally:
            if cursor is not None:
                cursor.close()
            pool.putconn(conn)

