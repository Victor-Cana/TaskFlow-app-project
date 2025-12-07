from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for project management routes
projects = Blueprint("projects", __name__)


# Get all resources for a specific project
# Example: /project/projects/1/resources
@projects.route("/projects/<int:project_id>/resources", methods=["GET"])
def get_project_resources(project_id):
    
    try:
        current_app.logger.info('Starting get_project_resources request')
        cursor = db.get_db().cursor()

        query = """
        SELECT DISTINCT r.*
        FROM Resources r
        JOIN Track t ON r.resourceID = t.resourceID
        JOIN Reports rep ON t.reportID = rep.reportID
        WHERE rep.projectID = %s
        """
        
        cursor.execute(query, (project_id,))
        resources = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f'Successfully retrieved {len(resources)} resources')
        return jsonify(resources), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_project_resources: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Get total work duration for each resource
# Example: /project/resources/work-duration
@projects.route("/resources/work-duration", methods=["GET"])
def get_resource_work_duration():
    try:
        current_app.logger.info('Starting get_resource_work_duration request')
        cursor = db.get_db().cursor()

        query = """
        SELECT resourceID, SUM(endTime - startTime) AS total_duration
        FROM WorkSessions
        GROUP BY resourceID
        """
        
        cursor.execute(query)
        durations = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f'Successfully retrieved durations for {len(durations)} resources')
        return jsonify(durations), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_resource_work_duration: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Create a new report with task deadlines
# Required fields: projectID, type, description, dateDue
# Example: POST /project/reports with JSON body
@projects.route("/reports", methods=["POST"])
def create_report():
    try:
        current_app.logger.info('Starting create_report request')

        data = request.get_json()

        # Validate required fields (using actual schema column names)
        required_fields = ["projectID", "type", "description", "dateDue"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
        INSERT INTO Reports (projectID, type, description, dateDue)
        VALUES (%s, %s, %s, %s)
        """
        
        cursor.execute(
            query,
            (
                data["projectID"],
                data["type"],
                data["description"],
                data["dateDue"]
            )
        )

        db.get_db().commit()
        new_report_id = cursor.lastrowid
        cursor.close()

        return jsonify({
            "message": "Report created successfully",
            "reportID": new_report_id
        }), 201
    except Error as e:
        current_app.logger.error(f'Database error in create_report: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Grant user access to a resource
# Example: POST /project/access
@projects.route("/access", methods=["POST"])
def grant_resource_access():
    try:
        current_app.logger.info('Starting grant_resource_access request')

        data = request.get_json()

        # Validate required fields (using actual schema column names)
        required_fields = ["userID", "projectID", "resourceID"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        cursor.execute(
            "SELECT * FROM AssignedTo WHERE userID = %s AND projectID = %s",
            (data["userID"], data["projectID"])
        )
        if not cursor.fetchone():
            return jsonify({"error": "User must be assigned to project first"}), 400

        query = """
        INSERT INTO HaveAccessTo (userID, projectID, resourceID, lastOpenedAt)
        VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
        """
        
        cursor.execute(
            query,
            (
                data["userID"],
                data["projectID"],
                data["resourceID"]
            )
        )

        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Access granted successfully"}), 201
    except Error as e:
        current_app.logger.error(f'Database error in grant_resource_access: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Revoke user access to a resource
# Example: DELETE /project/access
@projects.route("/access", methods=["DELETE"])
def revoke_resource_access():
    try:
        current_app.logger.info('Starting revoke_resource_access request')
        data = request.get_json()

        # Validate required fields
        required_fields = ["userID", "projectID", "resourceID"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
        DELETE FROM HaveAccessTo
        WHERE userID = %s AND projectID = %s AND resourceID = %s
        """
        
        cursor.execute(query, (data["userID"], data["projectID"], data["resourceID"]))
        
        if cursor.rowcount == 0:
            return jsonify({"error": "Access record not found"}), 404

        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Access revoked successfully"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in revoke_resource_access: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Assign user to a project
# Example: POST /project/assignments
@projects.route("/assignments", methods=["POST"])
def assign_user_to_project():

    try:
        current_app.logger.info('Starting assign_user_to_project request')
        data = request.get_json()

        # Validate required fields
        required_fields = ["projectID", "userID", "accessLevel"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
        INSERT INTO AssignedTo (userID, projectID, dateAssigned, dateRemoved, accessLevel)
        VALUES (%s, %s, CURRENT_TIMESTAMP, NULL, %s)
        """
        
        cursor.execute(
            query,
            (
                data["userID"],
                data["projectID"],
                data["accessLevel"]
            )
        )

        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "User assigned to project successfully"}), 201
    except Error as e:
        current_app.logger.error(f'Database error in assign_user_to_project: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Remove user from a project
# Example: DELETE /project/assignments
@projects.route("/assignments", methods=["DELETE"])
def remove_user_from_project():

    try:
        current_app.logger.info('Starting remove_user_from_project request')
        data = request.get_json()

        # Validate required fields
        required_fields = ["projectID", "userID"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
        DELETE FROM AssignedTo
        WHERE projectID = %s AND userID = %s
        """
        
        cursor.execute(query, (data["projectID"], data["userID"]))
        
        if cursor.rowcount == 0:
            return jsonify({"error": "Assignment record not found"}), 404

        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "User removed from project successfully"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in remove_user_from_project: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Send message to all users assigned to a project
# Example: POST /project/projects/1/messages
@projects.route("/projects/<int:project_id>/messages", methods=["POST"])
def send_project_message(project_id):
    try:
        current_app.logger.info('Starting send_project_message request')

        data = request.get_json()

        # Validate required fields
        required_fields = ["messageType", "messageUrgency", "messageBody", "messengerID"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        # Insert the message
        message_query = """
        INSERT INTO Messages (messageType, messageUrgency, messageBody, timeSent, messengerID)
        VALUES (%s, %s, %s, CURRENT_TIMESTAMP, %s)
        """
        
        cursor.execute(
            message_query,
            (
                data["messageType"],
                data["messageUrgency"],
                data["messageBody"],
                data["messengerID"]
            )
        )

        # Get the newly created message ID
        message_id = cursor.lastrowid

        # Send to all assigned users who haven't been removed
        receive_query = """
        INSERT INTO Receives (userID, messageID, timeRead)
        SELECT at.userID, %s, NULL
        FROM AssignedTo at
        WHERE at.projectID = %s AND at.dateRemoved IS NULL
        """
        
        cursor.execute(receive_query, (message_id, project_id))

        db.get_db().commit()
        affected_users = cursor.rowcount
        cursor.close()

        return jsonify({
            "message": "Message sent successfully",
            "messageID": message_id,
            "users_notified": affected_users
        }), 201
    except Error as e:
        current_app.logger.error(f'Database error in send_project_message: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Update an existing message
# Example: PUT /project/messages/1
@projects.route("/messages/<int:message_id>", methods=["PUT"])
def update_message(message_id):
    try:
        current_app.logger.info('Starting update_message request')
        data = request.get_json()

        if "messageBody" not in data:
            return jsonify({"error": "Missing required field: messageBody"}), 400

        cursor = db.get_db().cursor()

        # Check if message exists
        cursor.execute("SELECT * FROM Messages WHERE messageID = %s", (message_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Message not found"}), 404

        query = """
        UPDATE Messages
        SET messageBody = %s
        WHERE messageID = %s
        """
        
        cursor.execute(query, (data["messageBody"], message_id))

        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Message updated successfully"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in update_message: {str(e)}')
        return jsonify({"error": str(e)}), 500