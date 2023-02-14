
"""teamid, projectid, userid, roleid, firstname, lastname, email, username, password"""
class User:
    def __init__(self, teamid, projectid, userid, roleid, firstname, lastname, email,
                 username, password):
        self.teamid = teamid
        self.projectid = projectid
        self.userid = userid
        self.roleid = roleid
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.username = username
        self.password = password