"""
    Sample Controller File

    A Controller should be in charge of responding to a request.
    Load models to interact with the database and load views to render them to the client.

    Create a controller using this template
"""
from system.core.controller import *
import time
import datetime
from time import strftime


class Appointments(Controller):
    def __init__(self, action):
        super(Appointments, self).__init__(action)
        """
            This is an example of loading a model.
            Every controller has access to the load_model method.

            self.load_model('WelcomeModel')
        """
        self.load_model('Appointment')

    """ This is an example of a controller method that will load a view for the client """
    def index(self):
        """ 
        A loaded model is accessible through the models attribute 
        self.models['WelcomeModel'].get_all_users()
        """
        ## Session ID is the User ID
        # print "session id:", session['id']

        appts = self.models['Appointment'].show_all_appt(session['id'])
        # print "all appts:", appts

        current_date = strftime("%B %d, %Y")

        current_appts = []
        future_appts = []

        for index in appts:
            print "index:", index
            if str(index['date']) == time.strftime("%Y-%m-%d"):
                current_appts.append(index)
            elif str(index['date']) > time.strftime("%Y-%m-%d"):
                future_appts.append(index)
            else:
                continue


        # print "CURRENT", current_appts
        # print "FUTURE", future_appts

        # print "DATE:", appts[0]['date']
        # print "DATE TYPE:", type(appts[0]['date'])
        # print "TIME:", appts[0]['time']
        # print "TIME TYPE:", type(appts[0]['time'])
        # print "CURRENT DATE:", time.strftime("%Y-%m-%d")
        # print "CURRENT DATE TYPE:", type(time.strftime("%d/%m/%Y"))
        # print "CURRENT TIME:", time.strftime("%H:%M:%S")
        # print "CURRENT TIME TYPE:", type(time.strftime("%H:%M:%S"))
        

        return self.load_view('/appointments/index.html', current_appts=current_appts, future_appts=future_appts, current_date=current_date)




    def new(self):
        print "Proceeding to Add a New Appointment"

        appt = {
                'date': request.form['date'],
                'time': request.form['time'],
                'tasks': request.form['tasks'],
                'status': 'Pending',
                'user_id': session['id']
            }


        check = self.models['Appointment'].create_appt(appt)

        if check['status'] == False:
            for message in check['errors']:
                flash(message)
            return redirect('/appointments')
        else:
            return redirect('/appointments')

    def edit(self, id):
        print "Preparing to Edit the Appointment"
        single_appt = self.models['Appointment'].show_one_appt(id)
        print "single_appt:", single_appt

        return self.load_view('/appointments/edit.html', single_appt=single_appt)

    def update(self, id):
        print "Starting the Update Process"

        appt = {
            "tasks": request.form['tasks'],
            "time": request.form['time'],
            "status": request.form['status'],
            "id": id
        }
        print "UPDATE APPT", appt

        self.models['Appointment'].update_appt(appt)

        return redirect('/appointments')

    def destroy(self, id):

        self.models['Appointment'].destroy_appt(id)

        return redirect('/appointments')





