from dataobjects.user import User
from dbservices.user_service import User_service
import psycopg2

# Get All Users
try:
    user_list = User_service.get_all_users()
    print("All Users")
    if user_list is not None:
        for user in user_list:
            print("TeamID: {}\tProjectID: {}\tUserID: {}\tRoleID: {}\tFirstname: {}\tLastname: {} " \
                  "Email: {}\tUsername: {}\tPassword: {}".format(user.teamid, user.projectid, user.userid,
                                                                 user.roleid, user.firstname, user.lastname, user.email,
                                                                 user.username, user.password))
except (Exception, psycopg2.DatabaseError) as err:
    print(err)

# Get only 'user2 by username'
try:
    print("Get user2")
    user = User_service.get_user_by_username('user2')
    if user is not None:
        print("TeamID: {}\tProjectID: {}\tUserID: {}\tRoleID: {}\tFirstname: {}\tLastname: {} " \
              "Email: {}\tUsername: {}\tPassword: {}".format(user.teamid, user.projectid, user.userid,
                                                             user.roleid, user.firstname, user.lastname, user.email,
                                                             user.username, user.password))
except(Exception, psycopg2.DatabaseError) as err:
    print(err)

# Get only 'user3 by userid'
try:
    print("Get user with id = 220")
    user = User_service.get_user_by_userid(220)
    if user is not None:
        print("TeamID: {}\tProjectID: {}\tUserID: {}\tRoleID: {}\tFirstname: {}\tLastname: {} " \
              "Email: {}\tUsername: {}\tPassword: {}".format(user.teamid, user.projectid, user.userid,
                                                             user.roleid, user.firstname, user.lastname, user.email,
                                                             user.username, user.password))
except(Exception, psycopg2.DatabaseError) as err:
    print(err)

# Get user that does not exist
try:
    print("Get user with id = 909090")
    user = User_service.get_user_by_userid(909090)
    if user is not None:
        print("TeamID: {}\tProjectID: {}\tUserID: {}\tRoleID: {}\tFirstname: {}\tLastname: {} " \
            "Email: {}\tUsername: {}\tPassword: {}".format(user.teamid, user.projectid, user.userid,
                                                         user.roleid, user.firstname, user.lastname, user.email,
                                                         user.username, user.password))
    else:
        print("User with id {} does not exist.".format(909090))
except(Exception, psycopg2.DatabaseError) as err:
    print(err)

# Create new user
try:
    new_user = User(2, 4, 1110909, 20, 'John', 'Baxter', 'baxterj@gmail.com', 'baxterj', 'baxterpass')
    success_flag = User_service.create_or_update_user(new_user)
    if success_flag:
        print("Created new user")
    else:
        print("Creation of new user was Not successful")
except(Exception, psycopg2.DatabaseError) as err:
    print(err)

# Update existing user
try:
    existing_user = User(2, 4, 1110909, 20, 'John', 'Baxter', 'baxternewemail@gmail.com', 'baxterj', 'baxterpass')
    success_flag = User_service.create_or_update_user(existing_user)
    if success_flag:
        print("Updated existing user")
    else:
        print("Update of user with id: {} Not successful".format(existing_user.userid))
except(Exception, psycopg2.DatabaseError) as err:
    print(err)

# Delete user
try:
    success_flag = User_service.delete_user(1110909)
    if success_flag:
        print("Deleted user with id {}".format(1110909))
    else:
        print("Delete failed for userid {}".format(1110909))
except(Exception, psycopg2.DatabaseError) as err:
    print(err)