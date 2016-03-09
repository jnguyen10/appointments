"""
    Sample Controller File

    A Controller should be in charge of responding to a request.
    Load models to interact with the database and load views to render them to the client.

    Create a controller using this template
"""
from system.core.controller import *
from time import strftime
import datetime

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        """
            This is an example of loading a model.
            Every controller has access to the load_model method.

            self.load_model('WelcomeModel')
        """
        self.load_model('User')
        self.load_model('Appointment')

    """ This is an example of a controller method that will load a view for the client """
    def index(self):
        """ 
        A loaded model is accessible through the models attribute 
        self.models['WelcomeModel'].get_all_users()
        """

        return self.load_view('/users/index.html')

    def login(self):
        print "Proceeding to Log In"

        user_info = {
            'email': request.form['email'],
            'password': request.form['password']
        }

        print "USER INFO:", user_info

        check_user = self.models['User'].login_user(user_info)

        if check_user['status'] == False:
            for message in check_user['errors']:
                flash(message)
            return redirect('/')
        else:
            session['name'] = check_user['name']
            session['email'] = user_info['email']
            session['id'] = check_user['id']


            return redirect('/appointments')


    def registration(self):
        print "Proceeding to Register"

        user_info = {
            'name': request.form['name'],
            'email': request.form['email'],
            'password': request.form['password'],
            'confirm_pw': request.form['confirm_pw'],
            'birthdate': request.form['birthdate']
            }

        print user_info

        check_user = self.models['User'].create_user(user_info)
        print "Check user in controller:", check_user
        if check_user['status'] == False:
            for message in check_user['errors']:
                flash(message)
            return redirect('/')
        else:
            session['name'] = user_info['name']
            session['birthdate'] = user_info['birthdate']
            session['email'] = user_info['email']
            session['id'] = check_user['id']
            current_date = strftime("%B %d, %Y")

            return self.load_view('/appointments/index.html', current_date=current_date)

    def logout(self):
        session['name'] = ''
        session['email'] = ''
        session['password'] = ''
        session['id'] = ''

        return redirect('/')


