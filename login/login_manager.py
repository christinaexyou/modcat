from dbservices.user_service import User_service
class LoginManager():

    @staticmethod
    def login_validation(username, password):
        user = User_service.get_user_by_username(username)
        if(user is not None):
            if user.password == password:
                return 'ok'
            else:
                return 'Incorrect Password'
        else:
            return 'User ' + username + ' not found'
