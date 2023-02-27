from dataobjects.user import User
from dataobjects.project import Project
from dataobjects.team import Team
from dataobjects.models_users import ModelsUser
from dataobjects.teams_projects import TeamsProjects


class DBObjectUtils:
    @staticmethod
    def user_utility(user_tuple):
        """
        Create a User object from a tuple of column values
        User tuple is in the following order:
        teamid, projectid, userid, roleid, firstname, lastname,email,username,password, active
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
        active = user_tuple[9]
        # Order in constructor: teamid, projectid, roleid, firstname, lastname, email,
        #                  username, password, active, userid=None
        user = User(teamid, projectid, roleid, firstname, lastname,
                    email, username, password, active, userid)
        return user

    @staticmethod
    def user_tuple_utility(user):
        """
        Create a tuple of user column values from a User object
        :param user: User object
        :return: tuple of user column values
        """
        # Cols:  teamid, projectid, userid, roleid, firstname, lastname,email,username,password, active
        return (user.teamid, user.projectid, user.roleid, user.firstname, user.lastname,
                user.email, user.username, user.password, user.active, user.userid)

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

    @staticmethod
    def team_utility(team_tuple):
        """
        Create a Team object from a tuple of column values
        Team tuple is in the following order:
        teamid, teamname, department, teamlead_userid
        :param team_tuple A tuple of column values whose order is determined by the query to the team table.
        :return: A Team object whose values are retrieved by the query to the team table.
        """
        teamid = team_tuple[0]
        teamname = team_tuple[1]
        department = team_tuple[2]
        teamlead_userid = team_tuple[3]

        team = Team(teamid, teamname, department, teamlead_userid)
        return team

    @staticmethod
    def team_tuple_utility(team):
        """
        Create a tuple of team column values from a Team object
        :param team: Team object
        :return: tuple of team column values
        """
        return (team.teamid, team.teamname, team.department, team.teamlead_userid)

    @staticmethod
    def models_users_utility(modelsusers_tuple):
        """
            Create a MODELUSER object from a tuple of column values
            MODELSUSERS tuple is in the following order:
            modelsusersid, modelid, userid, timestamp
            :param modelsusers_tuple A tuple of column values whose order is determined by the query to the modelsusers table.
            :return: A ModelUser object whose values are retrieved by the query to the modelsusers table.
            """
        modelsuserid = modelsusers_tuple[0]
        modelid = modelsusers_tuple[1]
        userid = modelsusers_tuple[2]
        timestamp = modelsusers_tuple[3]

        modelsuser = ModelsUser(modelsuserid, modelid, userid, timestamp)
        return modelsuser

    @staticmethod
    def models_users_tuple_utility(modelsusers):
        """
        Create a tuple of MODELUSERS column values for the given MODELSUSER object
        :param project: MODELSUSER object
        :return: tuple of modelsusers column values
        """
        return (modelsusers.modelsusersid, modelsusers.modelid, modelsusers.userid, modelsusers.timestamp)

    @staticmethod
    def projects_models_utility(projects_models_tuple):
        """
            Create a ProjectsModels object from a tuple of column values
            projects_models_tuple is in the following order:
            projectsmodelsid, projectid, modelid, timestamp
            :param projects_models_tuple A tuple of column values whose order is determined by the query to the PROJECTSMODELS table.
            :return: A ProjectsModels object whose values are retrieved by the query to the PROJECTSMODELS table.
            """
        projects_modelsid = projects_models_tuple[0]
        projectid = projects_models_tuple[1]
        modelid = projects_models_tuple[2]
        timestamp = projects_models_tuple[3]

        modelsuser = ModelsUser(projects_modelsid, projectid, modelid, timestamp)
        return modelsuser

    @staticmethod
    def projects_models_tuple_utility(projectsmodels):
        """
        Create a tuple of PROJECTSMODELS column values for the given ProjectsModels object
        :param projectsmodels: ProjectsModels object
        :return: tuple of PROJECTSMODELS column values
        """
        return (projectsmodels.projectsmodelsid, projectsmodels.projectid, projectsmodels.userid, projectsmodels.timestamp)

    @staticmethod
    def teams_projects_utility(teams_project_tuple):
        """
            Create a TeamsProject object from a tuple of column values
            teams_projects_tuple is in the following order:
            teamsprojectsid, teamid, projectid, timestamp
            :param projects_models_tuple A tuple of column values whose order is determined by the query to the PROJECTSMODELS table.
            :return: A ProjectsModels object whose values are retrieved by the query to the PROJECTSMODELS table.
            """
        teamsprojectid = teams_project_tuple[0]
        teamid = teams_project_tuple[1]
        projectid = teams_project_tuple[2]
        timestamp = teams_project_tuple[3]

        teamsprojects = TeamsProjects(teamsprojectid, teamid, projectid, timestamp)
        return teamsprojects


    @staticmethod
    def teams_projects_tuple_utility(teamsprojects):
        """
        Create a tuple of teamsprojects column values for the given TeamsProjects object
        :param projectsmodels: TeamsProjects object
        :return: tuple of teamsprojects column values
        """
        return (teamsprojects.teamsprojectsid, teamsprojects.teamid, teamsprojects.projectid, teamsprojects.timestamp)