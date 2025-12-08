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
# from backend.ml_models import model01

john_kraft = Blueprint("Client CFO", __name__)

# Get information for the reports that have due dates in the future
@john_kraft.route('/reports', methods=['GET'])
def get_future_reports():
    try:
        cursor = db.get_db().cursor()
        
        # Get reports where dateDue is in the future
        cursor.execute("SELECT * FROM Reports WHERE dateDue > NOW()")
        reports = cursor.fetchall()

        if not reports:
            return jsonify({"error": "reports not found"}), 404

        cursor.close()
        return jsonify(reports), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@john_kraft.route('/projects', methods=['POST'])
def create_new_project():
    try:
        data = request.get_json()

        # check for required params (removed projectID - it's AUTO_INCREMENT)
        required_fields = ["managerID", "creatorID"]
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Missing required field: {field}"}), 400
            
        # optional params
        projectName = data.get("projectName") or None
        dateDue = data.get("dateDue") or None  # Fixed: was dateDUE
        description = data.get("description") or None
        dateManaged = data.get("dateManaged") or None
        dateCreated = data.get("dateCreated") or None

        cursor = db.get_db().cursor()
        query = """
        INSERT INTO Projects (projectName, dateDue, description, dateCreated, 
            creatorID, dateManaged, managerID)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (
                projectName,
                dateDue,
                description,
                dateCreated,
                data["creatorID"],
                dateManaged,
                data["managerID"]
            ),
        )
        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "project created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# see how long work has been done on each resource
@john_kraft.route("/WorkSessions/<int:resourceID>", methods=["GET"])
def get_resource_work_duration(resourceID):  # Add parameter!
    try:
        current_app.logger.info(f'Getting work duration for resource {resourceID}')
        cursor = db.get_db().cursor()

        query = """
        SELECT resourceID, SUM(TIMESTAMPDIFF(HOUR, startTime, endTime)) AS total_duration
        FROM WorkSessions
        WHERE resourceID = %s
        GROUP BY resourceID
        """
        
        cursor.execute(query, (resourceID,))
        duration = cursor.fetchone()

        if not duration:
            return jsonify({"error": "duration not found"}), 404

        cursor.close()
        return jsonify(duration), 200
    except Exception as e:
        current_app.logger.error(f'Error: {str(e)}')
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