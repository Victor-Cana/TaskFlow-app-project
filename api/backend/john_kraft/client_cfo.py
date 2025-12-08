from flask import (
    Blueprint,
    request,
    jsonify,
    make_response,
    current_app,
    redirect,
    url_for,
)
import json
from backend.db_connection import db
# from backend.simple.playlist import sample_playlist_data
from backend.ml_models import model01

john_kraft = Blueprint("Client CFO", __name__)

# Get information for the reports that have due dates in the future
@john_kraft.route('/reports/<datetime:dateDue>', methods=['GET'])
def get_future_reports(link):
    try:
        cursor = db.get_db().cursor()
        
        # Get Report information
        cursor.execute("SELECT * FROM Reports WHERE %s > NOW()", (dateDue,))
        reports = cursor.fetchall()

        if not reports:
            return jsonify({"error": "reports not found"}), 404

        cursor.close()
        return jsonify(reports), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Create a new project
@john_kraft.route('/projects', methods=['POST'])
def create_new_project():
    try:
        data = request.get_json()

        # check for required params
        required_fields = ["projectID", "managerID", "creatorID"]
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Missing required field: {field}"}), 400
            
        #optional params
        projectName = data.get("projectName") or None
        dateDUE = data.get("dateDUE") or None
        description = data.get("description") or None
        dateManaged = data.get("dateManaged") or None
        dateCreated = data.get("dateCreated") or None

        cursor = db.get_db().cursor()
        query = """
        INSERT INTO Projects (projectID, managerID, creatorID,
            projectName, dateDUE, description, dateManaged, dateCreated)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (
                data["projectID"],
                projectName,
                dateDUE,
                data["managerID"],
                data["creatorID"],
                description,
                dateManaged,
                dateCreated
            ),
        )
        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "project created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# see how long work has been done on each resource
@john_kraft.route("/WorkSessions/<int:resourceID>", methods=["GET"])
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

        if not durations:
            return jsonify({"error": "duration not found"}), 404

        cursor.close()

        current_app.logger.info(f'Successfully retrieved durations for {len(durations)} resources')
        return jsonify(durations), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_resource_work_duration: {str(e)}')
        return jsonify({"error": str(e)}), 500

# Create a new milestone
@john_kraft.route('/milestones', methods=['POST'])
def create_new_milestone():
    try:
        data = request.get_json()

        # check for required params
        required_fields = ["projectID", "milestoneID"]
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Missing required field: {field}"}), 400
            
        #optional params
        name = data.get("name") or None
        description = data.get("description") or None
        displayStyle = data.get("displayStyle") or None

        cursor = db.get_db().cursor()
        query = """
        INSERT INTO Milestones (projectID, milestoneID, name,
            description, displayStyle)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (
                data["projectID"],
                data['milestoneID'],
                name,
                description,
                displayStyle
            ),
        )
        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "milestone created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# see how many projects a user has been assigned to
@john_kraft.route("/assignedto/<int:userID>", methods=["GET"])
def get_project_count():
    try:
        cursor = db.get_db().cursor()

        query = """
        SELECT userID, COUNT(DISTINCT projectID) AS total_project_count
        FROM AssignedTo
        GROUP BY userID
        """
        
        cursor.execute(query)
        project_counts = cursor.fetchall()

        if not project_counts:
            return jsonify({"error": "project count not found"}), 404

        cursor.close()

        return jsonify(project_counts), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

# pull reports with a specific type
@john_kraft.route("/reports/<string:type>", methods=["GET"])
def get_specific_report(type):
    try:
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT * FROM Reports WHERE type = %s", (type,))
        report = cursor.fetchall()

        if not report:
            return jsonify({"error": "report(s) not found"}), 404

        cursor.close()

        return jsonify(report), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500