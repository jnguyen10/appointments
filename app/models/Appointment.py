""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model
import time
import datetime
from time import strftime

class Appointment(Model):
    def __init__(self):
        super(Appointment, self).__init__()
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

    def show_all_appt(self, user_id):
        print "Showing all appointments"
        query = "SELECT * FROM appointments WHERE user_id = %s"
        data = [user_id]

        print self.db.query_db(query,data)

        return self.db.query_db(query,data)

    def show_one_appt(self, appt_id):
        print "Showing one appointment"
        query = "SELECT * FROM appointments WHERE id = %s"
        data = [appt_id]

        print self.db.query_db(query,data)
        
        return self.db.query_db(query,data)

    def create_appt(self, appt):
        print "Creating New Appointment"

        errors = []
        if str(appt['date']) < time.strftime("%Y-%m-%d"):
            errors.append("Invalid Date -- Cannot be in the past")
        elif len(str(appt['tasks'])) < 1:
            errors.append("Tasks cannot be empty")
        elif len(str(appt['time'])) < 1:
            errors.append("Time cannot be empty")
        
        if errors:
            return { "status": False, "errors": errors}
        else:
            query = "INSERT INTO appointments (date, time, tasks, status, user_id, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, NOW(),NOW())"
            data = [appt['date'], appt['time'], appt['tasks'], appt['status'], appt['user_id']]

            self.db.query_db(query,data)
            return { "status": True }

    def update_appt(self, appt):
        print "Updating the Appointment"

        query = "UPDATE appointments SET tasks = %s, time = %s, status = %s WHERE id = %s"
        data = [appt['tasks'],appt['time'],appt['status'],appt['id']]

        return self.db.query_db(query,data)

    def destroy_appt(self, id):
        print "Destroying Appointment"

        query = "DELETE FROM appointments WHERE id = %s"
        data = [id]

        return self.db.query_db(query,data)











