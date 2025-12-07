CREATE DATABASE IF NOT EXISTS ProjectDB;
USE ProjectDB;
#Need to Drop FK tables if they exist first or cannot be dropped
DROP TABLE IF EXISTS HaveAccessTo;
DROP TABLE IF EXISTS Receives;
DROP TABLE IF EXISTS AssignedTo;
DROP TABLE IF EXISTS Track;
DROP TABLE IF EXISTS Reports;
DROP TABLE IF EXISTS WorkSessions;
DROP TABLE IF EXISTS Milestones;
DROP TABLE IF EXISTS Resources;
DROP TABLE IF EXISTS Messages;
DROP TABLE IF EXISTS Projects;
DROP TABLE IF EXISTS Users;




CREATE TABLE IF NOT EXISTS Users
(
   userID    INTEGER AUTO_INCREMENT PRIMARY KEY,
   email1    VARCHAR(50) NOT NULL,
   email2    VARCHAR(50),
   email3    VARCHAR(50),
   firstName VARCHAR(50) NOT NULL,
   lastName  VARCHAR(50) NOT NULL,
   managerID INTEGER,
   FOREIGN KEY (managerID) REFERENCES Users(userID)
       ON UPDATE CASCADE
       ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS Messages
(
   messageID INTEGER PRIMARY KEY,
   messageType VARCHAR(50),
   messageUrgency VARCHAR(50),
   timeSent DATETIME,
   messageBody VARCHAR(255),
   messengerID INTEGER,
   FOREIGN KEY (messengerID) REFERENCES Users(userID)
       ON UPDATE CASCADE
       ON DELETE CASCADE
);



CREATE TABLE IF NOT EXISTS Projects
(
 projectID INTEGER PRIMARY KEY ,
 projectName VARCHAR(50),
 dateDue DATETIME,
 description VARCHAR(250),
 dateManaged DATETIME,
 managerID INTEGER,
 dateCreated DATETIME,
 creatorID INTEGER,
 FOREIGN KEY (managerID) REFERENCES Users(userID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
 FOREIGN KEY (creatorID) REFERENCES Users(userID)
       ON UPDATE CASCADE
       ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS Milestones(
 projectID INTEGER,
 milestoneID INTEGER,
 name VARCHAR(100),
 description VARCHAR(250),
 displayStyle VARCHAR(250),
 PRIMARY KEY (projectID,milestoneID),
 FOREIGN KEY (projectID) REFERENCES  Projects(projectID)
                                  ON UPDATE CASCADE
                                  ON DELETE CASCADE
);




CREATE TABLE IF NOT EXISTS Resources(
 resourceID INTEGER AUTO_INCREMENT PRIMARY KEY,
 name VARCHAR(50) NOT NULL,
 type VARCHAR(50) NOT NULL,
 description VARCHAR(250),
 link VARCHAR(250) NOT NULL,
 dateDue DATETIME
);




CREATE TABLE IF NOT EXISTS Receives(
 messageID INTEGER,
 userID INTEGER,
 timeRead DATETIME,
 PRIMARY KEY (messageID,userID),
 FOREIGN KEY (messageID) REFERENCES Messages(messageID)
                             ON UPDATE CASCADE
                             ON DELETE RESTRICT,
 FOREIGN KEY (userID) REFERENCES Users(userID)
                             ON UPDATE CASCADE
                             ON DELETE RESTRICT
);




CREATE TABLE IF NOT EXISTS AssignedTo(
 userID INTEGER,
 projectID INTEGER,
 dateAssigned DATETIME,
 dateRemoved DATETIME,
 accessLevel INTEGER,
 PRIMARY KEY(userID,projectID),
 FOREIGN KEY (userID) REFERENCES Users(userID)
                                  ON UPDATE CASCADE
                                  ON DELETE CASCADE,
 FOREIGN KEY (projectID) REFERENCES Projects(projectID)
                                  ON UPDATE CASCADE
                                  ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS Reports(
 reportID INTEGER PRIMARY KEY,
 projectID INTEGER NOT NULL,
 dateDue DATETIME,
 type VARCHAR(50),
 description VARCHAR(250),
 dateDone DATETIME,
 resourceCount INTEGER,
 FOREIGN KEY (projectID) REFERENCES Projects(projectID)
                                  ON UPDATE CASCADE
                                  ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS HaveAccessTo(
 userID INTEGER,
 projectID INTEGER,
 resourceID INTEGER,
 lastOpenedAt DATETIME,
 PRIMARY KEY (userID,projectID,resourceID),
 FOREIGN KEY (userID,projectID) REFERENCES AssignedTo(userID,projectID)
                                    ON UPDATE CASCADE
                                    ON DELETE CASCADE,
 FOREIGN KEY (resourceID) REFERENCES Resources(resourceID)
                                    ON UPDATE CASCADE
                                    ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS Track(
 reportID INTEGER,
 resourceID INTEGER,
 PRIMARY KEY (reportID, resourceID),
 FOREIGN KEY (reportID) REFERENCES Reports(reportID)
                                  ON UPDATE CASCADE
                                  ON DELETE CASCADE,
 FOREIGN KEY (resourceID) REFERENCES Resources(resourceID)
                                  ON UPDATE CASCADE
                                  ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS WorkSessions(
 sessionID INTEGER PRIMARY KEY,
 resourceID INTEGER NOT NULL,
 endTime DATETIME,
 startTime DATETIME,
 FOREIGN KEY (resourceID) REFERENCES Resources(resourceID)
                                    ON UPDATE CASCADE
                                    ON DELETE CASCADE
);



