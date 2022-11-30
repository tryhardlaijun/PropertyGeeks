-- use project DB
use project;
CREATE TABLE Region(
	RID INT NOT NULL AUTO_INCREMENT,
	town VARCHAR(50) NOT NULL,
    PRIMARY KEY (RID)
);
DESCRIBE Region;

CREATE TABLE FlatType(
	FID INT NOT NULL AUTO_INCREMENT,
    room_type VARCHAR(25) NOT NULL,
    PRIMARY KEY (FID)
);
DESCRIBE FlatType;

CREATE TABLE Quarter(
	QuarterID INT NOT NULL AUTO_INCREMENT,
    year CHAR(4) NOT NULL, 
    quarter CHAR(2) NOT NULL,
    PRIMARY KEY (QuarterID),
    CHECK (quarter = 'Q1' OR quarter = 'Q2' OR quarter = 'Q3' OR quarter = 'Q4')
);
DESCRIBE Quarter;

CREATE TABLE FlatDetails(
	FD_ID INT NOT NULL AUTO_INCREMENT,
	lease_commence_date CHAR(4) NULL,
    block VARCHAR(10) NOT NULL,
    model VARCHAR(50) NULL,
    floor_area_sqm float NULL,
    RID INT NOT NULL,
    FID INT NOT NULL,
    PRIMARY KEY (FD_ID),
    FOREIGN KEY (RID) REFERENCES region(RID),
	FOREIGN KEY (FID) REFERENCES flattype(FID)
);
DESCRIBE FlatDetails;

CREATE TABLE ResaleFlat(
	RS_ID INT NOT NULL AUTO_INCREMENT,
	price FLOAT NOT NULL,
    FD_ID INT NOT NULL,
    QuarterID INT NOT NULL,
    PRIMARY KEY (RS_ID),
    FOREIGN KEY (FD_ID) REFERENCES flatdetails(FD_ID)
    ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (QuarterID) REFERENCES quarter(QuarterID)
	ON UPDATE CASCADE ON DELETE CASCADE
);
DESCRIBE ResaleFlat;

CREATE TABLE RentalFlat(
	RT_ID INT NOT NULL AUTO_INCREMENT,
	median_rent FLOAT NOT NULL,
    FD_ID INT NOT NULL,
    QuarterID INT NOT NULL,
    PRIMARY KEY (RT_ID),
    FOREIGN KEY (FD_ID) REFERENCES flatdetails(FD_ID)
    ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (QuarterID) REFERENCES quarter(QuarterID)
	ON UPDATE CASCADE ON DELETE CASCADE
);
DESCRIBE RentalFlat;






