from dataobjects.user import User
from dataobjects.project import Project


class DBObjectUtils:
    @staticmethod
    def user_utility(user_tuple):
        """
        Create a User object from a tuple of column values
        User tuple is in the following order:
        teamid, projectid, userid, roleid, firstname, lastname, email, username, password
        :param user_tuple A tuple of column values whose order is determined by the query to the user table.
        :return: A User object whose values are retrieved by the query to the user table.
        """
        teamid = user_tuple[0]
        projectid = user_tuple[1]
        userid = user_tuple[2]
        roleid = user_tuple[3]
        firstname = user_tuple[4]
        lastname = user_tuple[5]
        email = user_tuple[6]
        username = user_tuple[7]
        password = user_tuple[8]
        user = User(teamid, projectid, userid, roleid, firstname, lastname,
                    email, username, password)
        return user

    @staticmethod
    def user_tuple_utility(user):
        """
        Create a tuple of user column values from a User object
        :param user: User object
        :return: tuple of user column values
        """
        return (user.teamid, user.projectid, user.userid, user.roleid, user.firstname, user.lastname,
                user.email, user.username, user.password)

    @staticmethod
    def project_utility(project_tuple):
        """
            Create a Project object from a tuple of column values
            Project tuple is in the following order:
            projectid, teamid, modelid, projectname
            :param project_tuple A tuple of column values whose order is determined by the query to the project table.
            :return: A Project object whose values are retrieved by the query to the project table.
            """
        projectid = project_tuple[0]
        teamid = project_tuple[1]
        modelid = project_tuple[2]
        projectname = project_tuple[3]

        project = Project(projectid, teamid, modelid, projectname)
        return project

    @staticmethod
    def project_tuple_utility(project):
        """
        Create a tuple of project column values for the given project object
        :param project: Project object
        :return: tuple of project column values
        """
        return (project.projectid, project.teamid, project.modelid, project.projectname)