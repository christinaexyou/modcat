from dataobjects.user import User
from dbservices.user_service import UserService
import psycopg2

# Get All Users
try:
    user_list = UserService.get_all_users()
    print("All Users")
    if user_list is not None:
        for user in user_list:
            print("TeamID: {}\tProjectID: {}\tUserID: {}\tRoleID: {}\tFirstname: {}\tLastname: {} " \
                  "Email: {}\tUsername: {}\tPassword: {}\tActive: {}".format(user.teamid, user.projectid, user.userid,
                                                                 user.roleid, user.firstname, user.lastname, user.email,
                                                                 user.username, user.password, user.active))
except (Exception, psycopg2.DatabaseError) as err:
    print(err)

# Get only 'user2 by username'
try:
    print("Get annjones")
    user = UserService.get_user_by_username('annjones')
    if user is not None:
        print("TeamID: {}\tProjectID: {}\tUserID: {}\tRoleID: {}\tFirstname: {}\tLastname: {} " \
              "Email: {}\tUsername: {}\tPassword: {}".format(user.teamid, user.projectid, user.userid,
                                                             user.roleid, user.firstname, user.lastname, user.email,
                                                             user.username, user.password))
except(Exception, psycopg2.DatabaseError) as err:
    print(err)

# Get only 'user3 by userid'
try:
    print("Get user with id = 3")
    user = UserService.get_user_by_userid(3)
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
    user = UserService.get_user_by_userid(909090)
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
    print("Creating new user, John Baxter")
    # teamid, projectid, roleid, firstname, lastname, email, username, password, active
    new_user = User(200, 200, 20, 'John', 'Baxter', 'baxterj@gmail.com', 'baxterj', 'baxterpass', True)
    success_flag = UserService.create_or_update_user(new_user)
    if success_flag:
        print("Created new user")
    else:
        print("Creation of new user was Not successful")
except(Exception, psycopg2.DatabaseError) as err:
    print(err)

# Update existing user's email
try:
    print("Updating ann jones email")
    existing_user = User(100, 100, 20, 'ann', 'jones', 'jonesa@gmail.com', 'annjones', 'annjones', True, 1)
    success_flag = UserService.create_or_update_user(existing_user)
    if success_flag:
        print("Updated existing user")
    else:
        print("Update of user with id: {} Not successful".format(existing_user.userid))
except(Exception, psycopg2.DatabaseError) as err:
    print(err)

# Delete user
try:
    user_to_delete = UserService.get_user_by_username('baxterj')
    print("Attempting to delete user with username 'baxterj' with userid={}".format(user_to_delete.userid))
    success_flag = UserService.delete_user(user_to_delete.userid)
    if success_flag:
        print("Deleted user with id {}".format(user_to_delete.userid))
    else:
        print("Delete failed for username {}".format('baxterj'))
except(Exception, psycopg2.DatabaseError) as err:
    print(err)