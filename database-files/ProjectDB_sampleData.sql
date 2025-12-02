#Example Insert Statements
INSERT INTO Messages (messageID, messageType, messageUrgency)
VALUES (1, 'Email', 'High');
INSERT INTO Messages (messageID, messageType, messageUrgency)
VALUES (2, 'Slack', 'Low');




INSERT INTO Users(userID, email1, email2,email3,firstName,lastName)
VALUES (1, 'john@example.com', 'john.alt@example.com', NULL, 'John', 'Doe');
INSERT INTO Users (userID, email1, email2, email3, firstName, lastName)
VALUES (2, 'jane@example.com', NULL, NULL, 'Jane', 'Smith');




INSERT INTO Projects (projectID, projectName, dateDue, description)
VALUES (1, 'Website Redesign', '2025-12-31 23:59:59', 'Complete overhaul of company website');
INSERT INTO Projects (projectID, projectName, dateDue, description)
VALUES (2, 'Mobile App', '2025-11-30 23:59:59', 'New iOS and Android application');


INSERT INTO Milestones (projectID, milestoneID, name, description, displayStyle)
VALUES (1, 1, 'Project Start', 'Initial project meeting', 'blue');


INSERT INTO Milestones (projectID, milestoneID, name, description, displayStyle)
VALUES (1, 2, 'Design Complete', 'Finalize system designs', 'green');


INSERT INTO Resources (resourceID, name, type, description, link, dateDue)
VALUES (1, 'Time Tracker', 'Tool', 'Application for logging and monitoring hours worked on project tasks', 'https://timetracker.company.com/dashboard', NULL);


INSERT INTO Resources (resourceID, name, type, description, link, dateDue)
VALUES (2, 'Weekly Timesheet', 'Document', 'Template for recording daily work hours and task breakdown', 'https://forms.company.com/timesheet-template', '2025-11-29 17:00:00');
INSERT INTO Sends (messageID, userID, timeSent)
VALUES (1, 1, '2025-11-23 09:15:00');


INSERT INTO Sends (messageID, userID, timeSent)
VALUES (2, 2, '2025-11-23 10:30:00');


INSERT INTO Receives (messageID, userID, timeRead)
VALUES (1, 2, '2025-11-23 09:20:00');


INSERT INTO Receives (messageID, userID, timeRead)
VALUES (2, 1, NULL);




INSERT INTO Creates (userID, projectID, dateCreated)
VALUES (1, 1, '2025-09-01 08:00:00');


INSERT INTO Creates (userID, projectID, dateCreated)
VALUES (2, 2, '2025-10-01 09:00:00');


INSERT INTO Manages (userID, projectID, dateManaged)
VALUES (1, 1, '2025-09-01 08:00:00');


INSERT INTO Manages (userID, projectID, dateManaged)
VALUES (1, 2, '2025-10-15 10:00:00');

INSERT INTO AssignedTo (userID, projectID, dateAssigned, dateRemoved, accessLevel)
VALUES (1, 1, '2025-09-01 08:00:00', NULL, 3);

INSERT INTO AssignedTo (userID, projectID, dateAssigned, dateRemoved, accessLevel)
VALUES (2, 1, '2025-09-05 09:00:00', NULL, 2);

INSERT INTO HaveAccessTo (userID, projectID, resourceID, lastOpenedAt)
VALUES (1, 1, 1, '2025-03-15 10:30:00');


INSERT INTO HaveAccessTo (userID, projectID, resourceID, lastOpenedAt)
VALUES (1, 1, 2, '2025-03-15 14:45:00');


INSERT INTO Reports (reportID, projectID, dateDue, type, description, dateDone)
VALUES (1, 1, '2025-12-01 17:00:00', 'Progress Report', 'Monthly Report', '2025-11-28 16:30:00');


INSERT INTO Reports (reportID, projectID, dateDue, type, description, dateDone)
VALUES (2, 1, '2025-12-15 23:59:00', 'Status Update', 'Weekly status update', NULL);


INSERT INTO Track (reportID, resourceID, resourceCount)
VALUES (1, 1, 4);


INSERT INTO Track (reportID, resourceID, resourceCount)
VALUES (1, 2, 3);


INSERT INTO WorkSessions (sessionID, resourceID, endTime, startTime, date)
VALUES (1, 1, '2025-1-2 12:00:00', '2025-1-2 09:00:00', '2025-1-2');


INSERT INTO WorkSessions (sessionID, resourceID, endTime, startTime, date)
VALUES (2, 2, '2025-11-23 16:30:00', '2025-11-23 13:00:00', '2025-11-23');
