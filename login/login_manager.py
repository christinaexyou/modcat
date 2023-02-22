from dbservices.user_service import UserService


class LoginManager():

    @staticmethod
    def login_validation(username, password):
        """
        Validate username/password
        :param username: Login username
        :param password: Login password
        :return: String message indicating login result.
        """
        user = UserService.get_user_by_username(username)
        if user is not None:
            if user.password == password:
                return 'ok', user
            else:
                return 'Incorrect Password', None
        else:
            return 'User ' + username + ' not found', None
