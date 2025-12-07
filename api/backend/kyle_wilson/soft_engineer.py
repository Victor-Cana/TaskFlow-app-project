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
from backend.simple.playlist import sample_playlist_data
from backend.ml_models import model01

kyle_wilson = Blueprint("Software Engineer", __name__)

# Update data/links 
@kyle_wilson.route('/resources/<string:link>', methods=['PUT'])
def update_resources(link):
    try:
        data = request.get_json()


        cursor = db.get_db().cursor()
        
        # Check if resource exists
        cursor.execute("SELECT * FROM Resources WHERE link = %s", (link,))
        if not cursor.fetchone():
            return jsonify({"error": "link not found"}), 404

        # Get the new link from request body
        if "link" not in data:
            return jsonify({"error": "No new link provided"}), 400

        new_link = data["link"]
        
        # Update the link
        query = "UPDATE Resources SET link = %s WHERE link = %s"
        cursor.execute(query, (new_link, link))
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Resource updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# have to be able to delete certain resources
@kyle_wilson.route('/resources/<int:resourceID>', methods=['DELETE'])
def delete_resource(resourceID):
    try:
        cursor = db.get_db().cursor()

        # check if resource exists
        cursor.execute("SELECT * FROM Resources where resourceID = %s", (resourceID,))
        if not cursor.fetchone():
            return jsonify({"error": "link not found"}), 404

        # delete the resource
        query = "DELETE FROM Resources WHERE resourceID = %s"
        cursor.execute(query, (resourceID,))
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Resource deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# create new resources
@kyle_wilson.route('/resources', methods=['POST'])
def create_resource():
    try:
        data = request.get_json()

        # check for required params
        required_fields = ["name", "type", "link"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": "No valid fields to update"}), 400
        
        #optional params
        description = data.get("description") 
        dateDue = data.get("dateDue")   

        cursor = db.get_db().cursor()
        query = """
        INSERT INTO Resources (name, type, description, link, dateDue)
        VALUES (%s, %s, %s, %s, %s )
        """
        cursor.execute(
            query,
            (
                data["name"],
                data["type"],
                description,
                data["link"],
                dateDue
            ),
        )
        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "Resource created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# creating a new user
@kyle_wilson.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()

        # check for required params
        required_fields = ["email1", "firstName", "lastName"]
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Missing required field: {field}"}), 400
            
        #optional params
        email2 = data.get("email2") or None
        email3 = data.get("email3") or None
        managerID = data.get("managerID") or None  

        cursor = db.get_db().cursor()
        query = """
        INSERT INTO Users (email1, email2, email3, firstName, lastName, managerID)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (
                data["email1"],
                email2,
                email3,
                data["firstName"],
                data["lastName"],
                managerID,
            ),
        )
        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "user created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# update a name and type resource by the resourceID
@kyle_wilson.route('/resources/<int:resourceID>', methods=['PUT'])
def update_resource_name(resourceID):
    try:
        data = request.get_json()

        cursor = db.get_db().cursor()
        
        # Check if resource exists
        cursor.execute("SELECT * FROM Resources WHERE resourceID = %s", (resourceID,))
        if not cursor.fetchone():
            return jsonify({"error": "resourceID not found"}), 404
        
        # Update the attributes for the given resourceID
        query = """
            UPDATE Resources 
            SET name = %s, type = %s, description = %s, link = %s, dateDue = %s 
            WHERE resourceID = %s
        """
        cursor.execute(query, (
            data.get("name"),
            data.get("type"),
            data.get("description"),
            data.get("link"),
            data.get("dateDue"),
            resourceID
        ))

        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Resource updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500




