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

# VIEW discussed and approved by prof Fontenot
DROP VIEW IF EXISTS resource_counts_view;


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

# creating VIEW for derived attribute 'resourceCounts'
CREATE VIEW resource_counts_view AS
   SELECT reportID, COUNT(*) as resourceCount
   FROM Track
   GROUP BY reportID;

USE ProjectDB;


INSERT INTO Users(email1,email2,email3,firstName,lastName) VALUES
 ('rwannell0@odnoklassniki.ru','rwannell0@livejournal.com',NULL,'Rodrique','Wannell')
,('twinskill1@e-recht24.de',NULL,NULL,'Trev','Winskill')
,('rspurrier2@virginia.edu',NULL,NULL,'Rivi','Spurrier')
,('nsantino3@moonfruit.com',NULL,NULL,'Nanny','Santino')
,('dpleming4@paypal.com',NULL,NULL,'Dorelle','Pleming')
,('akears5@independent.co.uk',NULL,NULL,'Adrian','Kears')
,('cmalter6@guardian.co.uk',NULL,NULL,'Cassie','Malter')
,('ttrever7@1und1.de','ttrever7@ehow.com',NULL,'Theresa','Trever')
,('mgander8@parallels.com','mgander8@domainmarket.com',NULL,'Maurine','Gander')
,('skarpman9@goo.gl',NULL,NULL,'Sibley','Karpman')
,('tbentincka@live.com',NULL,NULL,'Taber','Bentinck')
,('hgiovanninib@princeton.edu',NULL,NULL,'Herculie','Giovannini')
,('ljennoc@issuu.com','ljennoc@ca.gov',NULL,'Lazaro','Jenno')
,('ncantopherd@addthis.com',NULL,NULL,'Nicolis','Cantopher')
,('mbhatiae@github.io','mbhatiae@ed.gov',NULL,'Melody','Bhatia')
,('nmillyardf@macromedia.com','nmillyardf@yale.edu',NULL,'Niall','Millyard')
,('faindriug@princeton.edu',NULL,NULL,'Frans','Aindriu')
,('cdrabbleh@paypal.com','cdrabbleh@mapquest.com',NULL,'Carmella','Drabble')
,('fmargettsi@hp.com',NULL,NULL,'Fayina','Margetts')
,('nveelerj@army.mil','nveelerj@cam.ac.uk',NULL,'Normand','Veeler')
,('wfiltnessk@blogspot.com','wfiltnessk@behance.net',NULL,'Wendi','Filtness')
,('rdrakel@apache.org','rdrakel@nih.gov',NULL,'Roberta','Drake')
,('edriversm@independent.co.uk',NULL,NULL,'Enrique','Drivers')
,('nbrechn@goo.ne.jp','nbrechn@umich.edu',NULL,'Nealon','Brech')
,('lscudamoreo@va.gov',NULL,NULL,'Leyla','Scudamore')
,('dbaumanp@umn.edu','dbaumanp@slideshare.net',NULL,'Dorie','Bauman')
,('mgilbaneq@ezinearticles.com','mgilbaneq@topsy.com',NULL,'Mycah','Gilbane')
,('tclausenr@i2i.jp','tclausenr@businessinsider.com',NULL,'Theodore','Clausen')
,('ftunes@wufoo.com','ftunes@domainmarket.com',NULL,'Fanni','Tune')
,('nbarsbyt@yahoo.co.jp','nbarsbyt@newyorker.com',NULL,'Nicolais','Barsby')
,('mpooleyu@examiner.com','mpooleyu@yandex.ru',NULL,'Moss','Pooley')
,('dgounodv@bluehost.com','dgounodv@ebay.co.uk',NULL,'Devon','Gounod')
,('achristonw@photobucket.com',NULL,NULL,'Ase','Christon')
,('fhallgarthx@vistaprint.com',NULL,NULL,'Faun','Hallgarth')
,('udiviney@guardian.co.uk',NULL,NULL,'Ulrick','Divine');

UPDATE Users SET managerID = 20 WHERE userID= 1;
UPDATE Users SET managerID = 20 WHERE userID= 2;
UPDATE Users SET managerID = 21 WHERE userID= 3;
UPDATE Users SET managerID = 15 WHERE userID= 4;
UPDATE Users SET managerID = 20 WHERE userID= 5;
UPDATE Users SET managerID = 20 WHERE userID= 6;
UPDATE Users SET managerID = 20 WHERE userID= 7;
UPDATE Users SET managerID = 15 WHERE userID= 8;
UPDATE Users SET managerID = 15 WHERE userID= 9;
UPDATE Users SET managerID = 25 WHERE userID= 10;
UPDATE Users SET managerID = 20 WHERE userID= 11;
UPDATE Users SET managerID = 20 WHERE userID= 12;
UPDATE Users SET managerID = 15 WHERE userID= 13;
UPDATE Users SET managerID = 21 WHERE userID= 14;
UPDATE Users SET managerID = NULL WHERE userID= 15;
UPDATE Users SET managerID = 32 WHERE userID= 16;
UPDATE Users SET managerID = 32 WHERE userID= 17;
UPDATE Users SET managerID = 32 WHERE userID= 18;
UPDATE Users SET managerID = 32 WHERE userID= 19;
UPDATE Users SET managerID = NULL WHERE userID= 20;
UPDATE Users SET managerID = NULL WHERE userID= 21;
UPDATE Users SET managerID = 21 WHERE userID= 22;
UPDATE Users SET managerID = 20 WHERE userID= 23;
UPDATE Users SET managerID = 21 WHERE userID= 24;
UPDATE Users SET managerID = 20 WHERE userID= 25;
UPDATE Users SET managerID = 15 WHERE userID= 26;
UPDATE Users SET managerID = 15 WHERE userID= 27;
UPDATE Users SET managerID = 25 WHERE userID= 28;
UPDATE Users SET managerID = 25 WHERE userID= 29;
UPDATE Users SET managerID = 25 WHERE userID= 30;
UPDATE Users SET managerID = 20 WHERE userID= 31;
UPDATE Users SET managerID = NULL WHERE userID= 32;
UPDATE Users SET managerID = 20 WHERE userID= 33;
UPDATE Users SET managerID = 21 WHERE userID= 34;
UPDATE Users SET managerID = 21 WHERE userID= 35;


INSERT INTO Messages(messageID,messageType,messageUrgency,messageBody,timeSent,messengerID) VALUES
 (1,'Info','Medium','Persistent 3rd generation approach','2024-05-06 06:53:00',10)
,(2,'Alert','Medium','Optional contextually-based parallelism','2024-05-14 11:32:00',33)
,(3,'Info','High','Multi-layered static synergy','2024-07-09 06:04:00',30)
,(4,'Ping','Low','Centralized maximized open architecture','2024-08-06 12:47:00',2)
,(5,'Ping','Medium','Down-sized bifurcated protocol','2024-08-10 03:50:00',16)
,(6,'Ping','Low','Distributed web-enabled attitude','2024-09-18 04:51:00',3)
,(7,'Reminder','Critical','Inverse intangible interface','2024-09-27 19:43:00',7)
,(8,'Info','Low','Digitized directional matrices','2024-09-30 02:05:00',26)
,(9,'Info','High','Progressive optimal hardware','2024-10-01 07:54:00',28)
,(10,'Info','Critical','Streamlined encompassing middleware','2024-10-17 22:07:00',18)
,(11,'Update','High','Persistent context-sensitive secured line','2024-10-20 17:57:00',12)
,(12,'Info','Medium','Streamlined zero tolerance synergy','2024-10-27 02:36:00',22)
,(13,'Info','High','Front-line 3rd generation model','2024-11-30 09:58:00',23)
,(14,'Ping','Medium','Function-based systematic help-desk','2024-12-21 17:53:00',1)
,(15,'Ping','Critical','Vision-oriented local solution','2025-01-08 04:14:00',18)
,(16,'Alert','Low','Up-sized analyzing service-desk','2025-01-13 10:40:00',32)
,(17,'Alert','Medium','Stand-alone high-level matrix','2025-01-27 00:56:00',20)
,(18,'Info','Medium','Integrated logistical knowledge base','2025-02-04 05:00:00',1)
,(19,'Ping','Critical','Enhanced 3rd generation database','2025-02-14 15:51:00',5)
,(20,'Update','Critical','Cross-group background migration','2025-02-28 12:35:00',11)
,(21,'Ping','Medium','Multi-channelled methodical application','2025-03-01 01:04:00',30)
,(22,'Alert','Medium','Stand-alone background monitoring','2025-03-27 21:19:00',10)
,(23,'Update','High','Fully-configurable bi-directional focus group','2025-04-03 01:15:00',18)
,(24,'Alert','Medium','Horizontal directional emulation','2025-04-12 20:57:00',25)
,(25,'Reminder','High','Expanded radical forecast','2025-05-19 04:47:00',12)
,(26,'Alert','Low','Upgradable coherent process improvement','2025-05-31 04:00:00',27)
,(27,'Ping','Medium','Down-sized regional interface','2025-05-31 09:04:00',32)
,(28,'Update','High','Fully-configurable fault-tolerant solution','2025-07-06 05:51:00',21)
,(29,'Ping','Medium','Customizable client-server synergy','2025-08-04 08:03:00',22)
,(30,'Reminder','Medium','Enterprise-wide reciprocal projection','2025-08-16 08:13:00',32)
,(31,'Reminder','High','Persevering client-server utilisation','2025-08-21 05:34:00',35)
,(32,'Info','Critical','Mandatory motivating workforce','2025-08-27 00:50:00',8)
,(33,'Update','Medium','Fully-configurable hybrid protocol','2025-09-10 04:43:00',10)
,(34,'Ping','Critical','Cloned optimizing superstructure','2025-10-14 10:19:00',29)
,(35,'Update','High','Multi-layered coherent artificial intelligence','2025-11-21 22:50:00',20);


INSERT INTO Projects(projectID,projectName,dateDue,description,dateCreated,creatorID,dateManaged,managerID) VALUES
 (1,'nullam porttitor','2026-08-06',NULL,'2025-08-15',3,'2025-08-15',15)
,(2,'neque aenean','2026-05-04',NULL,'2025-09-26',34,'2025-10-30',4)
,(3,'posuere felis','2025-05-01',NULL,'2024-05-23',11,'2024-05-23',6)
,(4,'massa quis','2026-03-06','In quis justo. Maecenas rhoncus aliquam lacus.','2025-08-07',11,'2025-08-07',25)
,(5,'justo maecenas','2024-12-31',NULL,'2024-02-18',12,'2024-02-18',15)
,(6,'iaculis','2025-01-27','In sagittis dui vel nisl. Duis ac nibh.','2024-01-29',35,'2024-02-15',14)
,(7,'neque vestibulum','2026-09-14','Morbi non lectus. Aliquam sit amet diam in magna bibendum imperdiet. Nullam orci pede, venenatis non, sodales sed, tincidunt eu, felis.','2026-01-29',30,'2026-01-29',23)
,(8,'arcu sed','2025-10-11','Fusce lacus purus, aliquet at, feugiat non, pretium quis, lectus.','2024-11-07',11,'2024-11-07',31)
,(9,'aliquet','2025-01-05',NULL,'2024-01-14',34,'2024-01-14',31)
,(10,'ipsum primis in','2025-06-03','Nullam porttitor lacus at turpis. Donec posuere metus vitae ipsum.','2025-01-14',13,'2025-01-14',2)
,(11,'laoreet ut','2026-07-31',NULL,'2026-03-25',1,'2026-03-31',32)
,(12,'tempus','2026-11-08',NULL,'2026-06-21',20,'2026-06-21',31)
,(13,'ac','2025-10-10','Etiam vel augue. Vestibulum rutrum rutrum neque.','2024-12-17',31,'2024-12-17',21)
,(14,'quis orci','2026-05-08','Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.','2025-11-17',23,'2025-11-17',8)
,(15,'metus sapien','2025-12-13','Duis bibendum, felis sed interdum venenatis, turpis enim blandit mi, in porttitor pede justo eu massa.','2025-03-09',17,'2025-03-29',34)
,(16,'vel','2026-01-08',NULL,'2025-07-19',24,'2025-07-19',3)
,(17,'erat','2025-01-12',NULL,'2024-08-03',20,'2024-08-03',17)
,(18,'id','2025-06-27',NULL,'2025-03-30',28,'2025-03-30',32)
,(19,'est risus','2026-11-22','Sed ante.','2026-07-30',33,'2026-07-30',31)
,(20,'tellus nisi eu','2026-03-15','Nunc nisl. Duis bibendum, felis sed interdum venenatis, turpis enim blandit mi, in porttitor pede justo eu massa.','2026-01-07',11,'2026-01-31',4)
,(21,'magna','2025-04-18',NULL,'2024-10-22',6,'2024-10-22',23)
,(22,'tortor duis mattis','2025-11-12',NULL,'2025-02-07',30,'2025-02-07',14)
,(23,'a','2025-03-25',NULL,'2024-11-03',17,'2024-12-01',20)
,(24,'interdum mauris','2026-09-25','Nulla tellus. In sagittis dui vel nisl. Duis ac nibh.','2025-11-05',34,'2025-11-05',17)
,(25,'volutpat','2026-10-20','Suspendisse potenti. Nullam porttitor lacus at turpis. Donec posuere metus vitae ipsum.','2026-04-15',21,'2026-04-30',31)
,(26,'ante ipsum primis','2026-07-24','Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Duis faucibus accumsan odio. Curabitur convallis. Duis consequat dui nec nisi volutpat eleifend.','2025-08-03',11,'2025-08-03',22)
,(27,'diam','2025-06-30','Sed sagittis. Nam congue, risus semper porta volutpat, quam pede lobortis ligula, sit amet eleifend pede libero quis orci.','2025-01-23',18,'2025-01-23',28)
,(28,'amet erat nulla','2025-12-16',NULL,'2025-09-03',13,'2025-09-13',25)
,(29,'mi pede','2026-09-26','Morbi sem mauris, laoreet ut, rhoncus aliquet, pulvinar sed, nisl. Nunc rhoncus dui vel sem.','2026-02-22',7,'2026-02-22',17)
,(30,'condimentum neque','2026-06-22',NULL,'2025-07-25',24,'2025-07-25',4)
,(31,'mattis egestas','2025-11-07','Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Nulla dapibus dolor vel est.','2025-08-23',16,'2025-08-23',2)
,(32,'cursus id','2025-09-17',NULL,'2024-11-11',21,'2024-11-25',7)
,(33,'id','2025-08-21',NULL,'2025-02-28',18,'2025-02-28',17)
,(34,'risus semper','2025-12-06',NULL,'2025-07-17',22,'2025-07-17',4)
,(35,'sem mauris','2026-04-15',NULL,'2025-12-27',31,'2025-12-27',24);


INSERT INTO Milestones(projectID,milestoneID,name,description,displayStyle) VALUES
 (29,10,'nulla','Maecenas tincidunt lacus at velit.','banner')
,(4,1,'convallis','Proin leo odio, porttitor id, consequat in, consequat ut, nulla.','hidden')
,(31,10,'integer ac neque','Proin risus.',NULL)
,(31,8,'turpis a pede','Aliquam non mauris.',NULL)
,(29,4,'pede justo','Maecenas tincidunt lacus at velit.','hidden')
,(10,7,'sit','Mauris ullamcorper purus sit amet nulla.','banner')
,(5,4,'morbi a','In hac habitasse platea dictumst.','banner')
,(21,7,'justo',NULL,'card')
,(24,1,'erat','Integer a nibh.','hidden')
,(10,6,'parturient montes','Nullam varius.',NULL)
,(20,2,'luctus et',NULL,'hidden')
,(4,4,'porta volutpat','Praesent id massa id nisl venenatis lacinia.','featured')
,(10,2,'congue risus','Morbi sem mauris, laoreet ut, rhoncus aliquet, pulvinar sed, nisl.','card')
,(13,7,'vel',NULL,'banner')
,(15,10,'dignissim',NULL,'banner')
,(29,2,'posuere cubilia','Quisque id justo sit amet sapien dignissim vestibulum.','card')
,(21,4,'morbi','Integer a nibh.','banner')
,(3,2,'sem praesent','Cras in purus eu magna vulputate luctus.','featured')
,(27,4,'sapien iaculis','Mauris ullamcorper purus sit amet nulla.','hidden')
,(27,1,'nullam',NULL,'hidden')
,(33,8,'neque duis','Ut tellus.','card')
,(24,7,'aliquet ultrices erat','Mauris ullamcorper purus sit amet nulla.','banner')
,(5,1,'sit amet sapien','Aenean auctor gravida sem.',NULL)
,(11,2,'nec nisi vulputate','Morbi vel lectus in quam fringilla rhoncus.','banner')
,(23,2,'interdum','In tempor, turpis nec euismod scelerisque, quam turpis adipiscing lorem, vitae mattis nibh ligula nec sem.','card')
,(11,5,'nec','Nulla ac enim.','card')
,(16,3,'risus','In est risus, auctor sed, tristique in, tempus sit amet, sem.','featured')
,(25,8,'est','Quisque arcu libero, rutrum ac, lobortis vel, dapibus at, diam.','card')
,(25,2,'amet nunc viverra',NULL,NULL)
,(10,3,'rutrum nulla tellus','Phasellus sit amet erat.','featured')
,(17,3,'curabitur',NULL,NULL)
,(23,3,'consequat morbi a','Lorem ipsum dolor sit amet, consectetuer adipiscing elit.',NULL)
,(12,8,'pede malesuada','Lorem ipsum dolor sit amet, consectetuer adipiscing elit.','card')
,(2,5,'nunc proin at','Duis bibendum.','banner')
,(25,5,'vel ipsum','Morbi vestibulum, velit id pretium iaculis, diam erat fermentum justo, nec condimentum neque sapien placerat ante.','card')
,(3,1,'amet nunc','Vestibulum ac est lacinia nisi venenatis tristique.','banner')
,(9,7,'dapibus dolor',NULL,NULL)
,(15,1,'sem duis aliquam',NULL,'card')
,(15,5,'placerat','Suspendisse potenti.','featured')
,(10,1,'in lacus curabitur',NULL,'hidden')
,(9,6,'a ipsum integer','Aenean sit amet justo.','hidden')
,(18,6,'ultrices posuere','Fusce posuere felis sed lacus.','banner')
,(26,6,'ultrices vel','Integer non velit.','card')
,(5,10,'non','Duis mattis egestas metus.','card')
,(5,3,'sed','Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Mauris viverra diam vitae quam.',NULL)
,(10,9,'tempus vel','Mauris ullamcorper purus sit amet nulla.',NULL)
,(13,1,'erat volutpat in',NULL,'card')
,(2,10,'ut volutpat','Aliquam erat volutpat.',NULL)
,(10,10,'quam a','Donec diam neque, vestibulum eget, vulputate ut, ultrices vel, augue.','featured')
,(12,7,'aenean fermentum donec','Pellentesque ultrices mattis odio.','card')
,(18,2,'facilisi','Nullam orci pede, venenatis non, sodales sed, tincidunt eu, felis.','hidden')
,(35,7,'etiam faucibus cursus',NULL,'hidden')
,(4,5,'lacinia eget','Praesent blandit lacinia erat.','hidden')
,(26,5,'at ipsum',NULL,'banner')
,(26,4,'sapien a',NULL,'card')
,(6,8,'vitae','Maecenas rhoncus aliquam lacus.','featured')
,(2,4,'blandit ultrices enim','Nulla tellus.','hidden')
,(17,7,'proin leo','Nunc rhoncus dui vel sem.',NULL)
,(4,10,'et ultrices','Donec odio justo, sollicitudin ut, suscipit a, feugiat et, eros.','card')
,(35,6,'felis sed lacus','Mauris enim leo, rhoncus sed, vestibulum sit amet, cursus id, turpis.','hidden');


INSERT INTO Resources(name,type,description,link,dateDue) VALUES
 ('fusce','.docx',NULL,'https:///orci.html?fusce=lorem&posuere=id&felis=ligula&sed=suspendisse&lacus=ornare&morbi=consequat&','2026-04-15')
,('velit','.docx',NULL,'https:///arcu/adipiscing/molestie/hendrerit/at.jpg?quam=sapien&nec=sapien&dui=non&luctus=mi&rutrum=i','2025-09-10')
,('at','.docx',NULL,'https:///justo/morbi/ut/odio.jpg?justo=malesuada&lacinia=in&eget=imperdiet&tincidunt=et&eget=commodo','2025-03-23')
,('dolor','.xlsx',NULL,'http:///in.png?tempus=a&sit=odio&amet=in&sem=hac','2026-08-20')
,('consequat','.pdf',NULL,'http:///gravida/sem/praesent.jpg?orci=dui&eget=luctus&orci=rutrum&vehicula=nulla&condimentum=tellus&','2025-04-03')
,('dictumst','.csv',NULL,'https:///nam/ultrices/libero/non.xml?et=donec&eros=ut&vestibulum=dolor&ac=morbi&est=vel&lacinia=lect','2025-05-18')
,('massa id','.docx',NULL,'http:///purus/eu/magna/vulputate/luctus/cum/sociis.json?mi=sed&in=magna&porttitor=at&pede=nunc&justo','2025-08-28')
,('elementum pellentesque','.docx','Curabitur gravida nisi at nibh.','http:///congue/risus/semper/porta/volutpat.json?nulla=dapibus&sed=dolor&vel=vel&enim=est&sit=donec&a',NULL)
,('dapibus','.xlsx',NULL,'http:///ante/ipsum/primis.jsp?nisi=odio&nam=donec&ultrices=vitae&libero=nisi&non=nam&mattis=ultrices','2026-09-12')
,('potenti in','.pdf','Nullam molestie nibh in lectus.','https:///fusce/congue/diam.png?mauris=primis&morbi=in&non=faucibus&lectus=orci&aliquam=luctus&sit=et','2026-04-19')
,('justo','.csv','Praesent id massa id nisl venenatis lacinia.','https:///vehicula/condimentum.jsp?nec=sapien&dui=urna&luctus=pretium&rutrum=nisl&nulla=ut&tellus=vol','2025-07-02')
,('neque','.xlsx','Sed ante.','http:///dolor/morbi/vel/lectus.js?felis=luctus&donec=et&semper=ultrices&sapien=posuere&a=cubilia','2025-03-18')
,('vestibulum','.pdf',NULL,'http:///cras/in/purus/eu/magna/vulputate.png?felis=faucibus&eu=orci&sapien=luctus&cursus=et&vestibul','2025-01-20')
,('mattis nibh','.pdf',NULL,'http:///sit/amet/lobortis.jpg?sed=nibh&augue=fusce&aliquam=lacus&erat=purus&volutpat=aliquet&in=at&c','2025-08-12')
,('in','.docx',NULL,'http:///quis/lectus/suspendisse/potenti/in/eleifend/quam.png?posuere=tincidunt&felis=lacus&sed=at&la','2025-02-07')
,('nullam orci','.csv',NULL,'https:///amet.json?curae=convallis&donec=duis&pharetra=consequat&magna=dui&vestibulum=nec&aliquet=ni','2025-12-16')
,('ultrices posuere','.docx','Nunc purus.','http:///purus.json?felis=felis&donec=ut&semper=at&sapien=dolor&a=quis&libero=odio&nam=consequat&dui=','2024-12-13')
,('nibh fusce','.pdf',NULL,'http:///donec.jsp?sed=vestibulum&nisl=ante&nunc=ipsum&rhoncus=primis&dui=in&vel=faucibus&sem=orci&se','2026-03-05')
,('adipiscing elit','.docx','Donec ut dolor.','http:///libero/nullam/sit/amet/turpis/elementum/ligula.html?vulputate=nisl&luctus=aenean&cum=lectus&','2025-11-28')
,('nulla','.docx',NULL,'http:///et.json?pretium=montes&iaculis=nascetur&justo=ridiculus&in=mus&hac=vivamus&habitasse=vestibu',NULL)
,('nibh','.pdf','Nulla neque libero, convallis eget, eleifend luctus, ultricies eu, nibh.','https:///turpis/nec/euismod.jpg?et=posuere&commodo=metus&vulputate=vitae&justo=ipsum&in=aliquam&blan','2025-12-26')
,('sollicitudin ut','.pdf','Lorem ipsum dolor sit amet, consectetuer adipiscing elit.','https:///dolor/morbi/vel.json?libero=quam&convallis=sollicitudin&eget=vitae&eleifend=consectetuer&lu','2025-05-26')
,('rhoncus sed','.csv',NULL,'http:///enim.js?sit=fringilla&amet=rhoncus&lobortis=mauris&sapien=enim&sapien=leo&non=rhoncus&mi=sed','2025-06-20')
,('ligula','.pdf','Cras in purus eu magna vulputate luctus.','http:///faucibus/orci.json?ipsum=imperdiet&integer=et&a=commodo&nibh=vulputate&in=justo&quis=in&just','2026-06-04')
,('ipsum','.pdf',NULL,'https:///id/luctus/nec/molestie/sed/justo/pellentesque.json?iaculis=platea&justo=dictumst&in=maecena','2025-10-07')
,('tellus nulla','.pdf',NULL,'https:///eget/eleifend/luctus/ultricies/eu.xml?eu=non&massa=mi&donec=integer&dapibus=ac&duis=neque&a','2026-11-17')
,('sit amet','.xlsx',NULL,'http:///fermentum/donec/ut/mauris/eget/massa.png?morbi=rhoncus&quis=sed&tortor=vestibulum&id=sit&nul','2026-02-26')
,('non quam','.docx',NULL,'http:///at.jsp?eu=eu','2026-05-06')
,('sit','.xlsx',NULL,'https:///sociis/natoque/penatibus/et.html?libero=morbi&nullam=porttitor&sit=lorem&amet=id&turpis=lig','2026-01-10')
,('magnis','.csv',NULL,'http:///non/quam/nec/dui/luctus/rutrum/nulla.json?etiam=habitasse&pretium=platea&iaculis=dictumst&ju','2026-09-28')
,('nulla tempus','.pdf',NULL,'https:///sit.xml?sociis=consequat&natoque=nulla&penatibus=nisl&et=nunc&magnis=nisl&dis=duis&parturie','2025-01-29')
,('cras','.docx',NULL,'http:///nunc.js?aliquet=nulla&at=suscipit&feugiat=ligula&non=in&pretium=lacus&quis=curabitur&lectus=','2025-11-20')
,('vestibulum sit','.xlsx',NULL,'http:///posuere/felis/sed.jsp?dapibus=eu&duis=tincidunt&at=in&velit=leo&eu=maecenas&est=pulvinar&con','2025-10-09')
,('orci','.pdf','Integer ac neque.','https:///id/sapien.xml?amet=felis&eleifend=eu&pede=sapien&libero=cursus&quis=vestibulum&orci=proin&n','2026-01-05')
,('adipiscing','.xlsx',NULL,'http:///leo/pellentesque/ultrices.jsp?id=massa&justo=tempor&sit=convallis&amet=nulla&sapien=neque&di','2025-07-10');


INSERT INTO Receives(messageID,userID,timeRead) VALUES
 (1,15,'2024-05-06 13:49:00')
,(2,29,'2024-05-14 23:34:00')
,(3,15,'2024-07-09 20:48:00')
,(4,7,'2024-08-06 13:41:00')
,(5,5,'2024-08-10 19:05:00')
,(6,21,'2024-09-19 00:19:00')
,(7,17,'2024-09-28 09:41:00')
,(8,9,'2024-09-30 02:38:00')
,(9,35,'2024-10-01 17:01:00')
,(10,8,'2024-10-18 08:55:00')
,(11,18,'2024-10-20 19:30:00')
,(12,19,'2024-10-27 06:58:00')
,(13,17,'2024-12-01 08:11:00')
,(14,9,'2024-12-22 08:43:00')
,(15,27,'2025-01-08 10:17:00')
,(16,32,'2025-01-13 12:29:00')
,(17,24,'2025-01-27 23:40:00')
,(18,13,'2025-02-05 00:15:00')
,(19,29,'2025-02-15 07:17:00')
,(20,18,'2025-03-01 08:50:00')
,(21,31,'2025-03-01 12:39:00')
,(22,5,'2025-03-27 21:42:00')
,(23,11,'2025-04-03 06:59:00')
,(24,35,'2025-04-13 17:51:00')
,(25,21,'2025-05-20 00:34:00')
,(26,31,'2025-05-31 12:39:00')
,(27,26,'2025-05-31 17:01:00')
,(28,6,'2025-07-06 17:21:00')
,(29,22,'2025-08-04 15:27:00')
,(30,33,'2025-08-16 08:30:00')
,(31,14,'2025-08-21 13:41:00')
,(32,26,'2025-08-27 05:53:00')
,(33,13,'2025-09-10 12:54:00')
,(34,25,'2025-10-14 19:16:00')
,(35,30,'2025-11-22 14:42:00')
,(1,23,'2024-05-07 06:28:00')
,(2,27,'2024-05-14 22:27:00')
,(3,18,'2024-07-10 03:55:00')
,(4,14,'2024-08-07 03:58:00')
,(5,16,'2024-08-10 19:19:00')
,(6,29,'2024-09-18 08:17:00')
,(7,29,'2024-09-28 03:27:00')
,(8,27,'2024-09-30 17:45:00')
,(9,24,'2024-10-01 19:19:00')
,(10,24,'2024-10-18 04:27:00')
,(11,28,'2024-10-21 01:58:00')
,(12,26,'2024-10-28 00:00:00')
,(13,30,'2024-12-01 00:20:00')
,(14,13,'2024-12-22 16:20:00')
,(15,28,'2025-01-08 22:23:00')
,(16,14,'2025-01-14 06:19:00')
,(17,7,'2025-01-27 16:10:00')
,(18,25,'2025-02-05 04:20:00')
,(19,16,'2025-02-15 09:30:00')
,(20,14,'2025-02-28 15:35:00')
,(21,21,'2025-03-01 13:01:00')
,(22,34,'2025-03-28 00:44:00')
,(23,25,'2025-04-03 20:03:00')
,(24,16,'2025-04-13 19:52:00')
,(25,8,'2025-05-19 09:33:00')
,(26,3,'2025-06-01 00:34:00')
,(27,20,'2025-05-31 13:11:00')
,(28,17,'2025-07-06 19:05:00')
,(29,21,'2025-08-04 08:20:00')
,(30,2,'2025-08-16 20:39:00')
,(31,19,'2025-08-21 12:51:00')
,(32,21,'2025-08-27 19:07:00')
,(33,6,'2025-09-10 21:43:00')
,(34,33,'2025-10-14 13:15:00')
,(35,32,'2025-11-22 22:27:00')
,(1,34,'2024-05-07 05:36:00')
,(2,5,'2024-05-14 16:04:00')
,(3,27,'2024-07-10 02:50:00')
,(4,20,'2024-08-07 08:53:00')
,(5,15,'2024-08-10 07:48:00');


INSERT INTO AssignedTo(userID,projectID,dateAssigned,dateRemoved,accessLevel) VALUES
 (9,3,'2024-05-27',NULL,2)
,(27,13,'2025-01-12','2025-03-17',1)
,(13,17,'2024-08-15',NULL,3)
,(19,32,'2024-12-01',NULL,2)
,(31,30,'2025-08-05','2025-10-23',1)
,(2,12,'2026-07-20',NULL,1)
,(14,28,'2025-10-03',NULL,3)
,(29,22,'2025-03-04',NULL,4)
,(25,30,'2025-08-24',NULL,3)
,(34,17,'2024-09-02',NULL,3)
,(5,17,'2024-08-31',NULL,4)
,(18,11,'2026-04-15','2026-06-03',5)
,(16,23,'2024-12-03',NULL,5)
,(16,26,'2025-08-10',NULL,5)
,(15,24,'2025-11-18',NULL,1)
,(35,10,'2025-01-14','2025-02-27',3)
,(9,4,'2025-08-29',NULL,4)
,(31,33,'2025-03-14',NULL,3)
,(34,8,'2024-11-12',NULL,3)
,(29,10,'2025-01-14',NULL,5)
,(30,25,'2026-05-13',NULL,1)
,(6,15,'2025-03-27',NULL,4)
,(29,20,'2026-01-18',NULL,4)
,(3,18,'2025-04-21',NULL,3)
,(31,14,'2025-12-02',NULL,1)
,(35,31,'2025-08-24',NULL,2)
,(26,31,'2025-09-12',NULL,3)
,(12,11,'2026-03-27',NULL,4)
,(34,35,'2026-01-07',NULL,5)
,(16,32,'2024-12-04',NULL,5)
,(23,14,'2025-11-18',NULL,3)
,(34,13,'2025-01-01',NULL,5)
,(12,15,'2025-03-21',NULL,3)
,(22,31,'2025-08-27','2025-11-03',1)
,(22,9,'2024-02-01',NULL,1)
,(7,29,'2026-02-22',NULL,3)
,(19,29,'2026-02-27',NULL,3)
,(15,6,'2024-02-17','2024-03-05',5)
,(5,22,'2025-02-22','2025-04-09',2)
,(18,14,'2025-11-26',NULL,5)
,(5,19,'2026-08-06',NULL,5)
,(22,35,'2025-12-31',NULL,1)
,(18,23,'2024-11-17',NULL,1)
,(27,24,'2025-11-13','2025-12-16',2)
,(10,12,'2026-07-18',NULL,5)
,(5,7,'2024-08-15','2024-10-23',5)
,(4,5,'2024-03-08',NULL,3)
,(20,2,'2025-10-16',NULL,4)
,(6,8,'2024-11-17',NULL,3)
,(27,15,'2025-04-08',NULL,4)
,(11,20,'2026-01-20',NULL,2)
,(11,3,'2024-06-09',NULL,2)
,(19,35,'2025-12-28',NULL,4)
,(19,33,'2025-03-05',NULL,1)
,(6,5,'2024-03-02',NULL,3)
,(33,4,'2025-08-29',NULL,4)
,(22,1,'2025-09-02',NULL,2)
,(8,19,'2026-08-06','2026-10-25',3)
,(1,24,'2025-11-29',NULL,5)
,(14,7,'2026-02-04','2026-03-02',1)
,(9,25,'2026-05-15',NULL,1)
,(6,29,'2026-03-09',NULL,1)
,(35,24,'2025-11-09',NULL,4)
,(18,21,'2024-11-04',NULL,1)
,(17,12,'2026-07-08',NULL,3)
,(16,27,'2025-08-14','2025-10-28',4)
,(8,25,'2026-05-13',NULL,5)
,(14,1,'2025-09-08',NULL,1)
,(6,18,'2026-05-12',NULL,3)
,(7,32,'2024-11-12',NULL,5)
,(4,13,'2025-01-16',NULL,5)
,(5,32,'2024-11-22',NULL,3)
,(19,16,'2024-08-23',NULL,1)
,(1,18,'2025-04-11','2025-05-21',1)
,(8,20,'2026-01-27','2026-02-28',4)
,(10,27,'2025-02-02','2025-04-16',5)
,(15,22,'2025-02-18',NULL,2)
,(21,25,'2026-04-17',NULL,4)
,(11,30,'2025-08-21',NULL,1)
,(11,34,'2025-07-27',NULL,4)
,(17,19,'2026-08-12',NULL,5)
,(7,24,'2025-11-27',NULL,3)
,(33,31,'2025-09-10',NULL,5)
,(21,2,'2025-10-05',NULL,4)
,(13,16,'2025-07-26',NULL,1)
,(3,3,'2024-06-04',NULL,1)
,(5,9,'2026-07-18','2026-09-07',5)
,(7,10,'2025-02-07',NULL,3)
,(23,13,'2024-12-26','2025-01-21',5)
,(7,6,'2025-01-05',NULL,1)
,(8,28,'2025-01-28','2025-03-22',5)
,(26,19,'2026-08-28',NULL,1)
,(19,11,'2026-04-18','2026-05-09',1)
,(10,4,'2025-09-05',NULL,4)
,(2,34,'2025-08-01',NULL,3)
,(6,2,'2026-08-20',NULL,1)
,(11,5,'2025-01-31',NULL,1)
,(28,13,'2024-12-31','2025-03-02',1)
,(6,23,'2024-11-27',NULL,5)
,(4,21,'2026-08-16',NULL,1)
,(6,4,'2025-08-27','2025-09-26',2)
,(25,8,'2024-11-07',NULL,1)
,(14,21,'2024-10-27',NULL,3)
,(30,14,'2025-11-17',NULL,4)
,(31,35,'2026-01-10',NULL,4)
,(30,34,'2025-08-16','2025-08-20',2)
,(25,9,'2024-01-23','2024-03-05',5)
,(4,17,'2024-08-06',NULL,3)
,(17,28,'2025-09-15','2025-11-11',4)
,(8,8,'2024-12-05',NULL,5)
,(4,29,'2026-03-12',NULL,3)
,(18,4,'2025-08-14','2025-10-27',1)
,(16,5,'2024-02-18',NULL,2)
,(27,4,'2025-09-05',NULL,1)
,(25,33,'2025-03-28',NULL,2)
,(6,14,'2025-12-04','2026-01-16',4)
,(34,16,'2025-07-22',NULL,3)
,(9,2,'2025-10-07','2025-10-30',4)
,(18,3,'2024-05-31',NULL,4)
,(21,33,'2025-03-26',NULL,4)
,(8,1,'2025-09-07',NULL,4)
,(19,2,'2025-10-17',NULL,1)
,(33,8,'2024-11-22',NULL,1)
,(25,2,'2025-10-22',NULL,5)
,(20,4,'2025-09-03',NULL,5);


INSERT INTO Reports(reportID,projectID,dateDue,type,description,dateDone,resourceCount) VALUES
 (1,23,'2025-03-06','Financial',NULL,'2025-03-01',2)
,(2,16,'2026-01-04','Process','Donec posuere metus vitae ipsum.',NULL,1)
,(3,14,'2026-05-19','Financial','Ut at dolor quis odio consequat varius.',NULL,2)
,(4,14,'2026-05-23','Financial',NULL,NULL,3)
,(5,12,'2026-11-27','Process','Vivamus vel nulla eget eros elementum pellentesque.',NULL,3)
,(6,22,'2025-11-04','Process',NULL,'2025-10-26',2)
,(7,20,'2026-02-24','Technical','Integer aliquet, massa id lobortis convallis, tortor risus dapibus augue, vel accumsan tellus nisi eu orci.',NULL,3)
,(8,24,'2026-09-07','Process',NULL,NULL,8)
,(9,28,'2025-12-24','Process','Nam congue, risus semper porta volutpat, quam pede lobortis ligula, sit amet eleifend pede libero quis orci.',NULL,3)
,(10,29,'2026-09-08','Technical',NULL,NULL,3)
,(11,27,'2025-06-10','Update',NULL,'2025-06-02',0)
,(12,31,'2025-10-25','Financial',NULL,'2025-10-20',2)
,(13,12,'2026-11-08','Update',NULL,NULL,3)
,(14,5,'2024-12-22','Technical',NULL,'2024-12-21',2)
,(15,10,'2026-05-19','Financial',NULL,NULL,3)
,(16,19,'2026-11-20','Technical','Nulla facilisi.',NULL,1)
,(17,32,'2025-08-30','Technical','Nulla suscipit ligula in lacus.','2025-08-22',4)
,(18,33,'2025-08-11','Process','Etiam faucibus cursus urna.','2025-08-13',0)
,(19,15,'2025-12-22','Process','Morbi sem mauris, laoreet ut, rhoncus aliquet, pulvinar sed, nisl.',NULL,4)
,(20,13,'2025-09-24','Financial',NULL,'2025-09-26',2)
,(21,31,'2025-11-17','Financial',NULL,'2025-11-09',0)
,(22,18,'2025-07-03','Financial','Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.','2025-07-03',2)
,(23,6,'2025-01-31','Update',NULL,'2025-01-26',1)
,(24,2,'2026-04-22','Process','Nunc rhoncus dui vel sem.',NULL,4)
,(25,35,'2026-04-17','Update','Donec quis orci eget orci vehicula condimentum.',NULL,4)
,(26,30,'2026-06-03','Technical','Morbi porttitor lorem id ligula.',NULL,6)
,(27,8,'2025-12-30','Update',NULL,NULL,3)
,(28,11,'2026-08-06','Update','Curabitur at ipsum ac tellus semper interdum.',NULL,3)
,(29,25,'2025-10-22','Update',NULL,'2025-10-23',1)
,(30,32,'2025-09-23','Process','Proin interdum mauris non ligula pellentesque ultrices.','2025-09-23',1)
,(31,17,'2024-12-31','Financial','Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Duis faucibus accumsan odio.','2024-12-27',3)
,(32,34,'2025-11-17','Process','Donec odio justo, sollicitudin ut, suscipit a, feugiat et, eros.','2025-11-12',1)
,(33,21,'2026-11-11','Financial',NULL,NULL,4)
,(34,7,'2026-09-01','Update','Etiam pretium iaculis justo.',NULL,5)
,(35,4,'2025-06-21','Technical','Mauris sit amet eros.','2025-06-19',3)
,(36,9,'2025-06-22','Technical',NULL,'2025-06-16',1)
,(37,1,'2026-08-22','Process','Vestibulum sed magna at nunc commodo placerat.',NULL,3)
,(38,26,'2025-10-10','Process','Praesent blandit lacinia erat.','2025-10-13',3)
,(39,3,'2026-02-28','Update','Maecenas tristique, est et tempus semper, est quam pharetra magna, ac consequat metus sapien ut nunc.',NULL,1)
,(40,4,'2026-02-20','Technical',NULL,NULL,2)
,(41,6,'2025-01-10','Process',NULL,'2024-12-31',7)
,(42,24,'2025-01-07','Financial',NULL,'2024-12-29',4)
,(43,3,'2025-05-17','Technical',NULL,'2025-05-14',1)
,(44,22,'2025-04-28','Update','Vestibulum rutrum rutrum neque.','2025-04-19',1)
,(45,23,'2026-07-26','Financial',NULL,NULL,3)
,(46,11,'2026-08-19','Process','Lorem ipsum dolor sit amet, consectetuer adipiscing elit.',NULL,1)
,(47,19,'2026-01-03','Update','Phasellus sit amet erat.',NULL,3)
,(48,5,'2024-12-25','Financial',NULL,'2024-12-23',1)
,(49,9,'2024-12-19','Technical','Pellentesque at nulla.','2024-12-11',1)
,(50,20,'2026-03-20','Update','Curabitur at ipsum ac tellus semper interdum.',NULL,2)
,(51,28,'2025-12-25','Financial','Nulla ut erat id mauris vulputate elementum.',NULL,2)
,(52,10,'2026-11-07','Update',NULL,NULL,6)
,(53,15,'2025-12-17','Update',NULL,NULL,0)
,(54,2,'2026-05-15','Financial','Morbi vel lectus in quam fringilla rhoncus.',NULL,3)
,(55,26,'2026-07-24','Financial',NULL,NULL,4)
,(56,14,'2025-11-21','Update',NULL,'2025-11-15',3)
,(57,27,'2025-10-20','Process','Maecenas rhoncus aliquam lacus.','2025-10-11',0)
,(58,16,'2025-01-07','Update','Etiam vel augue.','2025-01-02',3)
,(59,29,'2026-07-21','Financial','Quisque ut erat.',NULL,2)
,(60,30,'2026-06-15','Process','Quisque arcu libero, rutrum ac, lobortis vel, dapibus at, diam.',NULL,1);


INSERT INTO HaveAccessTo(userID,projectID,resourceID,lastOpenedAt) VALUES
 (9,3,19,'2025-04-11')
,(27,13,18,'2025-08-01')
,(13,17,7,'2024-06-04')
,(19,32,31,'2024-12-01')
,(31,30,14,'2025-08-05')
,(2,12,2,'2026-07-20')
,(14,28,31,'2025-10-03')
,(29,22,21,'2025-03-04')
,(25,30,20,'2025-08-24')
,(34,17,30,'2024-09-02')
,(5,17,31,'2024-08-31')
,(18,11,29,'2026-04-15')
,(16,23,13,'2024-12-03')
,(16,26,33,'2025-08-10')
,(15,24,33,'2025-11-18')
,(35,10,28,'2025-01-14')
,(9,4,1,'2025-08-29')
,(31,33,22,'2025-03-14')
,(34,8,24,'2024-11-12')
,(29,10,30,'2025-01-14')
,(30,25,26,'2026-05-13')
,(6,15,13,'2025-03-27')
,(29,20,34,NULL)
,(3,18,11,'2025-04-21')
,(31,14,3,'2025-12-02')
,(35,31,34,'2025-08-24')
,(26,31,3,'2025-09-12')
,(12,11,34,'2026-03-27')
,(34,35,28,'2026-01-07')
,(16,32,10,'2024-12-04')
,(23,14,15,'2025-11-18')
,(34,13,19,'2025-01-01')
,(12,15,23,'2025-03-21')
,(22,31,26,'2025-08-27')
,(22,9,16,'2024-02-01')
,(7,29,27,'2026-02-22')
,(19,29,22,'2026-02-27')
,(15,6,16,'2024-02-17')
,(5,22,25,'2025-02-22')
,(18,14,17,'2025-11-26')
,(5,19,19,'2026-08-06')
,(22,35,23,'2025-12-31')
,(18,23,28,'2024-11-17')
,(27,24,31,'2025-11-13')
,(10,12,21,'2026-07-18')
,(5,7,21,'2024-08-15')
,(4,5,4,'2024-03-08')
,(20,2,5,'2025-10-16')
,(6,8,18,'2024-11-17')
,(27,15,12,'2025-04-08')
,(11,20,14,'2026-01-20')
,(11,3,26,'2024-06-09')
,(19,35,19,NULL)
,(19,33,5,'2025-03-05')
,(6,5,23,'2024-03-02')
,(33,4,8,'2025-08-29')
,(22,1,30,'2025-09-02')
,(8,19,13,NULL)
,(1,24,8,'2025-11-29')
,(14,7,30,'2026-02-04')
,(9,25,13,'2026-05-15')
,(6,29,1,'2026-03-09')
,(35,24,3,'2025-11-09')
,(18,21,28,'2024-11-04')
,(17,12,29,'2026-07-08')
,(16,27,26,'2025-08-14')
,(8,25,28,'2026-05-13')
,(14,1,31,'2025-09-08')
,(6,18,28,'2026-05-12')
,(7,32,24,'2024-11-12')
,(4,13,12,'2025-01-16')
,(5,32,14,'2024-11-22')
,(19,16,11,'2024-08-23')
,(1,18,33,'2025-04-11')
,(8,20,22,'2026-01-27')
,(10,27,25,'2025-02-02')
,(15,22,28,'2025-02-18')
,(21,25,25,'2026-04-17')
,(11,30,7,'2025-08-21')
,(11,34,25,'2025-07-27')
,(17,19,5,'2026-08-12')
,(7,24,23,'2025-11-27')
,(33,31,31,'2025-09-10')
,(21,2,22,'2025-10-05')
,(13,16,25,'2025-07-26')
,(3,3,35,'2024-06-04')
,(5,9,5,'2026-07-18')
,(7,10,21,'2025-02-07')
,(23,13,28,'2024-12-26')
,(7,6,29,'2025-01-05')
,(8,28,1,'2025-01-28')
,(26,19,4,'2026-08-28')
,(19,11,29,'2026-04-18')
,(10,4,26,NULL)
,(2,34,1,'2025-08-01')
,(6,2,29,'2026-08-20')
,(11,5,12,'2025-01-31')
,(28,13,26,NULL)
,(6,23,29,'2024-11-27')
,(4,21,12,'2026-08-16')
,(6,4,19,'2025-08-27')
,(25,8,35,'2024-11-07')
,(14,21,6,'2024-10-27')
,(30,14,8,'2025-11-17')
,(31,35,19,'2026-01-10')
,(30,34,14,'2025-08-16')
,(25,9,21,'2024-01-23')
,(4,17,11,'2024-08-06')
,(17,28,6,'2025-09-15')
,(8,8,28,'2024-12-05')
,(4,29,33,'2026-03-12')
,(18,4,21,'2025-08-14')
,(16,5,26,'2024-02-18')
,(27,4,35,'2025-09-05')
,(25,33,28,'2025-03-28')
,(6,14,29,'2025-12-04')
,(34,16,6,'2025-07-22')
,(9,2,33,'2025-10-07')
,(18,3,30,'2024-05-31')
,(21,33,26,'2025-03-26')
,(8,1,4,'2025-09-07')
,(19,2,17,'2025-10-17')
,(33,8,1,'2024-11-22')
,(25,2,23,'2025-10-22')
,(20,4,12,'2025-09-03');


INSERT INTO Track(resourceID,reportID) VALUES
(23,34)
,(8,13)
,(11,26)
,(9,17)
,(1,58)
,(14,42)
,(5,33)
,(8,8)
,(33,5)
,(32,7)
,(23,52)
,(2,51)
,(6,34)
,(32,8)
,(3,47)
,(18,1)
,(21,28)
,(6,4)
,(35,54)
,(16,55)
,(1,13)
,(7,52)
,(13,12)
,(13,28)
,(21,26)
,(7,49)
,(11,52)
,(28,52)
,(3,31)
,(24,60)
,(22,19)
,(8,15)
,(30,32)
,(17,42)
,(29,41)
,(16,23)
,(8,3)
,(35,20)
,(5,7)
,(26,35)
,(23,27)
,(3,10)
,(31,51)
,(20,41)
,(13,56)
,(26,45)
,(23,45)
,(21,6)
,(29,10)
,(32,40)
,(24,16)
,(11,8)
,(26,27)
,(9,18)
,(5,59)
,(24,24)
,(19,58)
,(5,38)
,(18,7)
,(10,42)
,(26,8)
,(14,12)
,(28,38)
,(27,35)
,(33,37)
,(27,54)
,(25,25)
,(8,56)
,(7,47)
,(6,25)
,(25,6)
,(10,34)
,(16,5)
,(9,4)
,(8,50)
,(7,54)
,(14,34)
,(30,55)
,(24,19)
,(2,55)
,(15,8)
,(35,58)
,(19,26)
,(29,37)
,(2,25)
,(3,8)
,(25,33)
,(27,33)
,(12,3)
,(2,19)
,(12,50)
,(21,4)
,(5,45)
,(4,24)
,(22,52)
,(18,2)
,(23,17)
,(26,37)
,(7,30)
,(5,39)
,(10,40)
,(27,20)
,(27,9)
,(6,42)
,(31,22)
,(30,44)
,(28,41)
,(32,10)
,(30,35)
,(34,52)
,(22,48)
,(13,26)
,(7,43)
,(8,11)
,(10,46)
,(30,9)
,(18,41)
,(1,14)
,(16,2)
,(33,14)
,(14,56)
,(10,15)
,(8,55)
,(24,34)
,(6,29)
,(22,22)
,(22,28)
,(34,31)
,(12,33)
,(4,21)
,(10,47)
,(22,24)
,(16,36)
,(4,17)
,(31,25)
,(3,41)
,(6,59)
,(19,8)
,(15,41)
,(1,9)
,(17,27)
,(16,31)
,(20,5)
,(30,19)
,(6,41)
,(10,38)
,(30,26)
,(23,13)
,(14,15)
,(30,27);


INSERT INTO WorkSessions(sessionID,resourceID,startTime,endTime) VALUES
 (1,32,'2025-05-04 15:54:00','2025-05-04 16:54:00')
,(2,24,'2026-05-07 02:36:00','2026-05-07 14:36:00')
,(3,14,'2024-12-19 12:36:00','2024-12-19 23:36:00')
,(4,23,'2025-02-01 05:50:00','2025-02-01 07:50:00')
,(5,26,'2026-05-17 05:48:00','2026-05-17 14:48:00')
,(6,13,'2024-05-30 07:38:00','2024-05-30 18:38:00')
,(7,19,'2024-12-28 03:16:00','2024-12-28 11:16:00')
,(8,26,'2026-04-16 21:45:00','2026-04-17 05:45:00')
,(9,22,'2024-11-13 03:03:00','2024-11-13 15:03:00')
,(10,24,'2026-06-03 03:00:00','2026-06-03 15:00:00')
,(11,27,'2025-06-14 15:12:00','2025-06-15 03:12:00')
,(12,1,'2026-03-08 08:27:00','2026-03-08 11:27:00')
,(13,18,'2025-10-26 09:20:00','2025-10-26 17:20:00')
,(14,23,'2024-07-07 02:01:00','2024-07-07 03:01:00')
,(15,32,'2025-03-26 06:08:00','2025-03-26 08:08:00')
,(16,29,'2025-08-16 04:22:00','2025-08-16 14:22:00')
,(17,25,'2025-02-05 17:20:00','2025-02-05 21:20:00')
,(18,8,'2024-12-15 08:14:00','2024-12-15 13:14:00')
,(19,23,'2024-12-16 19:06:00','2024-12-16 21:06:00')
,(20,4,'2025-12-24 06:17:00','2025-12-24 09:17:00')
,(21,11,'2024-07-08 05:02:00','2024-07-08 15:02:00')
,(22,9,'2026-02-27 21:57:00','2026-02-27 22:57:00')
,(23,7,'2025-04-22 03:29:00','2025-04-22 15:29:00')
,(24,9,'2026-04-10 09:34:00','2026-04-10 12:34:00')
,(25,15,'2024-10-08 03:11:00','2024-10-08 04:11:00')
,(26,15,'2024-11-13 09:47:00','2024-11-13 10:47:00')
,(27,31,'2024-12-23 12:49:00','2024-12-23 16:49:00')
,(28,34,'2025-01-14 14:28:00','2025-01-15 02:28:00')
,(29,12,'2024-12-06 02:51:00','2024-12-06 07:51:00')
,(30,4,'2025-09-11 06:45:00','2025-09-11 10:45:00')
,(31,35,'2024-11-16 04:52:00','2024-11-16 06:52:00')
,(32,12,'2024-11-04 22:01:00','2024-11-05 06:01:00')
,(33,14,'2025-07-28 00:15:00','2025-07-28 07:15:00')
,(34,33,'2025-06-11 07:14:00','2025-06-11 17:14:00')
,(35,21,'2025-08-27 21:44:00','2025-08-27 22:44:00')
,(36,16,'2025-03-03 22:26:00','2025-03-04 02:26:00')
,(37,4,'2026-02-02 22:29:00','2026-02-03 04:29:00')
,(38,5,'2024-12-29 21:58:00','2024-12-29 23:58:00')
,(39,25,'2025-04-09 12:07:00','2025-04-09 16:07:00')
,(40,11,'2024-08-13 17:39:00','2024-08-14 01:39:00')
,(41,31,'2024-04-23 00:52:00','2024-04-23 09:52:00')
,(42,31,'2024-07-04 16:22:00','2024-07-04 18:22:00')
,(43,32,'2025-04-22 03:55:00','2025-04-22 05:55:00')
,(44,15,'2024-07-25 20:55:00','2024-07-26 05:55:00')
,(45,30,'2026-01-23 18:36:00','2026-01-24 05:36:00')
,(46,4,'2026-05-07 04:29:00','2026-05-07 15:29:00')
,(47,33,'2024-12-18 14:53:00','2024-12-18 18:53:00')
,(48,6,'2025-02-16 07:19:00','2025-02-16 17:19:00')
,(49,19,'2024-12-24 20:22:00','2024-12-25 08:22:00')
,(50,28,'2025-09-26 23:47:00','2025-09-27 08:47:00')

