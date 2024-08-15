########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db
from backend.ml_models.model01 import predict

# Creating a Blueprint for camp_counselor routes
camp_counselor = Blueprint('camp_counselor', __name__)

# 2.1 staff info lookup
@camp_counselor.route('/camp_counselor/<c_ID>', methods=['GET'])
def predict_value(c_ID):
    cursor = db.get_db().cursor()
    the_query = f'''
    SELECT s.firstName, s.lastName, s.role, s.phoneNumber, s.email
    FROM Staff s
    JOIN CampSession cs ON s.sessionID = cs.sessionID
    WHERE s.campID = {c_ID}
    ;
    '''
    cursor.execute(the_query)
    the_data = cursor.fetchall()
    the_response = make_response(the_data)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@camp_counselor.route('/camp_counselor/<campID>/<sessionID>', methods=['DELETE'])
def delete_schedule(campID, sessionID):
   cursor = db.get_db().cursor()
   the_query = f'''
   DELETE FROM DailySchedule 
   USING DailySchedule
   WHERE DailySchedule.date = 7/27/2024
				AND DailySchedule.campID = {campID}
				AND DailySchedule.sessionID = {sessionID};
                '''		
   cursor.execute(the_query (campID, sessionID))
   db.get_db.commit() # commit the deletions to the database 
   return jsonify({"message": "Daily schedule deleted successfully"}), 200


@camp_counselor.route('/camp_counselor', methods=['PUT'])
def update_activity():
    current_app.logger.info('PUT /camp_counselor route')
    camp_info = request.json
    # current_app.logger.info(cust_info)
    camp_info = camp_info['description']

    query = '''UPDATE Activity
    SET Activity.description = '%s'
    FROM Activity
    JOIN ScheduleActivity ON Activity.activityId = ScheduleActivity.activityId
    JOIN DailySchedule ON ScheduleActivity.scheduleId = DailySchedule.scheduleId
    WHERE DailySchedule.date = 8/5/2024
    AND DailySchedule.campID = 16
    AND DailySchedule.sessionID = 24;
'''
    data = (camp_info)
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    return 'activity updated!'
