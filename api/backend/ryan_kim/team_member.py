from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

#Create a Blueprint for Ryan Kim routes
ryan_kim = Blueprint("Team Member", __name__)

# wants to see other people time worked
@ryan_kim.route('/worksessions/<int:resourceID>', methods=['GET'])
def see_time_worked(resourceID)
    try:
        current_app.logger.info('Starting see_time_worked request')
        cursor = db.get_db().cursor()

   # Prepare the base query
        query = """
            SELECT resourceID, SUM(endTime - startTime) AS total_duration
            FROM WorkSessions
            WHERE 1=1
        """
        params = []

        # Add filters if provided
        if resource_id:
            query += " AND resourceID = %s"
            params.append(resource_id)

        query += " GROUP BY resourceID"

        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query, params)
        activity_logs = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f'Successfully retrieved {len(activity_logs)} activity logs')
        return jsonify(activity_logs), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_activity_logs: {str(e)}')
        return jsonify({"error": str(e)}), 500

#Get all projects associated with a specific user
@ryan_kim.route("/users/<int:userId>/projects", methods=["GET"])
def get_user_projects(userId):
    try:
        cursor = db.get_db().cursor()

        # Check if user exists
        cursor.execute("SELECT * FROM Users WHERE userID = %s", (userId,))
        if not cursor.fetchone():
            return jsonify({"error": "User not found"}), 404

        # Get all projects for the user
        query = """
            SELECT *
            FROM Projects P
            JOIN AssignedTo a ON p.ProjectID = a.ProjectID
            WHERE a.UserID = %s AND a.DateRemoved IS NULL
            ORDER BY p.DateDue
        """
        cursor.execute(query, (userId,))
        projects = cursor.fetchall()
        cursor.close()

        return jsonify(projects), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

# Get all upcoming deadlines for reports in a specific project

@ryan_kim.route("/projects/<int:projectID>/deadlines", methods=["GET"])
def get_project_deadlines(projectID):
    try:
        current_app.logger.info(f'Starting get_project_deadlines request for projectID: {projectID}')
        cursor = db.get_db().cursor()

      

        # Get query parameters for filtering
        user_id = request.args.get("userID")

        current_app.logger.debug(f'Query parameters - userID: {user_id}')

        # Prepare the Base query
        query = """
            SELECT p.ProjectName, rep.Description, rep.DateDue, rep.DateDone, 
                   DATEDIFF(rep.DateDue, CURRENT_DATE) as DaysUntilDue
            FROM Reports rep
            JOIN Projects p ON rep.ProjectID = p.ProjectID
            WHERE p.ProjectID = %s
        """
        params = [projectID]

        # Add filters if provided
        if user_id:
            query += " AND rep.userID = %s"
            params.append(user_id)

        query += " ORDER BY rep.DateDue"

        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query, params)
        deadlines = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f'Successfully retrieved {len(deadlines)} deadlines')
        return jsonify(deadlines), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_project_deadlines: {str(e)}')
        return jsonify({"error": str(e)}), 500

# Remove access to a resource for a specific user
@ryan_kim.route("/haveaccessto/<int:userId>/<int:resourceId>", methods=["DELETE"])
def remove_resource_access(userId, resourceId):
    try:
        current_app.logger.info(f'Starting remove_resource_access request for userId: {userId}, resourceId: {resourceId}')
        
        cursor = db.get_db().cursor()
        
        # Check if access record exists
        cursor.execute("SELECT * FROM HaveAccessTo WHERE userID = %s AND resourceID = %s", (userId, resourceId))
        if not cursor.fetchone():
            cursor.close()
            return jsonify({"error": "Access record not found"}), 404

        # Delete the access record
        query = "DELETE FROM HaveAccessTo WHERE userID = %s AND resourceID = %s"
        params = [userId, resourceId]
        
        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()

        current_app.logger.info(f'Successfully removed access for userId: {userId}, resourceId: {resourceId}')
        return jsonify({"message": "Resource access removed successfully"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in remove_resource_access: {str(e)}')
        return jsonify({"error": str(e)}), 500

# Get all resources associated with a specific project for export/documentation

@ryan_kim.route("/projects/<int:projectID>/resources", methods=["GET"])
def get_project_resources(projectID):
    try:
        current_app.logger.info(f'Starting get_project_resources request for projectID: {projectID}')
        cursor = db.get_db().cursor()

        # Get project details
        cursor.execute("SELECT * FROM Projects WHERE projectID = %s", (projectID,))
        project = cursor.fetchone()

        if not project:
            return jsonify({"error": "Project not found"}), 404

        # Get associated resources
        query = """
            SELECT r.*
            FROM Resources r
            JOIN Track t ON r.ResourceID = t.ResourceID
            WHERE t.ProjectID = %s
        """
        cursor.execute(query, (projectID,))
        resources = cursor.fetchall()

        # Combine data from multiple related queries into one object to return (after jsonify)
        project["resources"] = resources

        cursor.close()
        
        current_app.logger.info(f'Successfully retrieved project and resources for projectID: {projectID}')
        return jsonify(project), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_project_resources: {str(e)}')
        return jsonify({"error": str(e)}), 500

        
