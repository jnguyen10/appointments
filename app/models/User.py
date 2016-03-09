""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

# Check to see if there is a number in the name
def numName(name):
        for x in name:
            if str(x).isdigit():
                return True
            else:
                pass

        return False


class User(Model):
    def __init__(self):
        super(User, self).__init__()
    """
    Below is an example of a model method that queries the database for all users in a fictitious application

    def get_all_users(self):
        print self.db.query_db("SELECT * FROM users")

    Every model has access to the "self.db.query_db" method which allows you to interact with the database
    """

    """
    If you have enabled the ORM you have access to typical ORM style methods.
    See the SQLAlchemy Documentation for more information on what types of commands you can run.
    """

    def create_user(self, info):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

        errors = []
        # IF statements for validation
        if len(info['name']) < 2:
            errors.append('Name should be at least 2 characters long')
        elif numName(info['name']) == True:
            errors.append('Cannot have numbers in the name')
        
        # Check to see if email has already been registered
        email_check = True
        query = "SELECT email FROM users"
        email_query = self.db.query_db(query)

        for x in email_query:
            print "This is X:", x
            for key, value in x.items():
                print key
                print value
                if value == info['email']:
                    email_check = False
                    break
                else:
                    continue

        if len(info['email']) < 1:
            errors.append('Email field cannot be left blank')
        elif email_check == False:
            errors.append('Email has already been registered')
        elif not EMAIL_REGEX.match(info['email']):
            errors.append('Email is not in the correct format.  Please try again')
        
        if len(info['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif info['password'] != info['confirm_pw']:
            errors.append('Passwords do not match.  Please try again')
        else:
            pw_hash = self.bcrypt.generate_password_hash(info['password'])
        
        # Check for errors to return status
        if errors:
            return { "status": False, "errors": errors }
        else:
            # If no errors are found, create the user
            add_user_query = "INSERT INTO users (name, email, pw_hash, birthdate, created_at, updated_at) VALUES (%s, %s, %s, %s, NOW(), NOW())"
            add_user_data = [info['name'],info['email'],pw_hash,info['birthdate']]

            self.db.query_db(add_user_query, add_user_data)

            query = "SELECT id FROM users WHERE email = %s"
            data = [info['email']]

            id_list = self.db.query_db(query,data)

            return { "status": True , "id": id_list[0]['id']}

    def login_user(self, info):
        errors = []

        # Check to see if user exists by doing a check for email in DB
        email_check = False
        query = "SELECT * FROM users"
        email_query = self.db.query_db(query)

        for x in email_query:
            print "X:", x
            for key, value in x.items():
                print "key:", key
                print "value:", value
                if value == info['email']:
                    email_check = True
                    name = x['name']
                    email = x['email']
                    id = x['id']
                    break
                else:
                    continue

        # Check to see password matches
        pw_check = False
        query = "SELECT pw_hash FROM users WHERE email = %s"
        data = [info['email']]
        pw_query = self.db.query_db(query, data)

        for x in pw_query:
            for key, value in x.items():
                if self.bcrypt.check_password_hash(value, info['password']):
                    pw_check = True
                    break
                else:
                    continue


        # Username validation
        if len(info['email']) < 1:
            errors.append('Email field cannot be blank')
        elif not EMAIL_REGEX.match(info['email']):
            errors.append('Please enter a valid email address!')
        elif email_check == False:
            errors.append('User and/or password does not match')

        # Password validation
        if len(info['password']) < 8:
            errors.append('Password must contain at least 8 characters')
        elif pw_check == False:
            errors.append('User and/or password does not match')


        # Check for errors to return status
        if errors:
            return { "status": False, "errors": errors }
        else:
            # If no errors are found, return true to the controller
            # Pass any key-value pairs that you may want to leverage later on
            return { "status": True, "name": name, "email": email , "id": id}

