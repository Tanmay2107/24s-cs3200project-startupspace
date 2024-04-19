CREATE DATABASE project;

USE project;

CREATE TABLE VentureCapitalist (
  VCID INT AUTO_INCREMENT PRIMARY KEY,
  Name VARCHAR(255),
  Industry_Preference VARCHAR(255),
  PortfolioSize INT
);

CREATE TABLE industryList (
    Industry VARCHAR(255),
    PRIMARY KEY (Industry)
);

CREATE TABLE Acquirers (
  acqID INT AUTO_INCREMENT PRIMARY KEY,
  Name VARCHAR(255),
  Sector VARCHAR(255)
);

CREATE TABLE GrowthStageList ( -- What is this column for?
    GrowthStage VARCHAR(255),
    PRIMARY KEY (GrowthStage)
);

CREATE TABLE Startup (
  StartupID INT AUTO_INCREMENT PRIMARY KEY,
  Name VARCHAR(255),
  City VARCHAR(255),
  GrowthStage VARCHAR(255),
  Industry VARCHAR(255),
  acqID INT,
  FOREIGN KEY (acqID) REFERENCES Acquirers(acqID) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (GrowthStage) REFERENCES GrowthStageList(GrowthStage),
  FOREIGN KEY (Industry) REFERENCES  industryList(Industry)
);

CREATE TABLE Founder (
  FounderID INT AUTO_INCREMENT PRIMARY KEY,
  Name VARCHAR(255),
  PhoneNumber VARCHAR(20),
  NumberOfCompanies INT,
  CredibilityRanking DECIMAL(19, 2)

);

CREATE TABLE Document (
  docID INT AUTO_INCREMENT PRIMARY KEY,
  documentType VARCHAR(255),
  fileSize INT,
  pageCount INT,
  wordCount INT,
  characterCount INT,
  StartupID INT,
  FounderID INT,
  FOREIGN KEY (StartupID) REFERENCES Startup(StartupID) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (FounderID) REFERENCES Founder(FounderID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE InvestmentOpportunities (
  OppID INT AUTO_INCREMENT PRIMARY KEY,
  FundingRound VARCHAR(255),
  Description TEXT,
  Terms TEXT,
  StartupID INT,
  FOREIGN KEY (StartupID) REFERENCES Startup(StartupID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE InvestmentOpportunityToVC (
    VCID  INT,
    OppID INT,
    PRIMARY KEY (VCID, OppID),
    FOREIGN KEY (VCID) REFERENCES VentureCapitalist (VCID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (OppID) REFERENCES InvestmentOpportunities (OppID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE InvestmentAnalytics (
  AnalyticsID INT AUTO_INCREMENT PRIMARY KEY,
  NumberofDeals INT,
  TotalInvested DECIMAL(19, 2),
  PortfolioDiversity DECIMAL(19, 2),
  PerformanceMetric DECIMAL(19, 2),
  VCID INT,
  FOREIGN KEY (VCID) REFERENCES VentureCapitalist(VCID) ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE FinancialMetrics (
  MetricID INT AUTO_INCREMENT PRIMARY KEY,
  MetricTitle VARCHAR(255),
  MetricValue DECIMAL(19, 2),
  StartupID INT,
  FOREIGN KEY (StartupID) REFERENCES Startup(StartupID) ON UPDATE CASCADE ON DELETE CASCADE
);



CREATE TABLE TeamMembers (
  MemberID INT AUTO_INCREMENT PRIMARY KEY,
  Name VARCHAR(255),
  PhoneNumber VARCHAR(20),
  Email VARCHAR(255),
  StartupID INT,
  FOREIGN KEY (StartupID) REFERENCES Startup(StartupID) ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE StartupFounder (
  StartupID INT,
  FounderID INT,
  PRIMARY KEY(StartupID, FounderID),
  FOREIGN KEY (FounderID) REFERENCES Founder(FounderID) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (StartupID) REFERENCES Startup(StartupID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE AcquisitionTarget (
  targetID INT AUTO_INCREMENT PRIMARY KEY,
  status VARCHAR(255),
  interested BOOLEAN,
  DateIdentified DATETIME DEFAULT CURRENT_TIMESTAMP,
  StartupID INT,
  acqID INT,
  FOREIGN KEY (StartupID) REFERENCES Startup(StartupID) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (acqID) REFERENCES Acquirers(acqID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE GeneralResearcher (
  researcherID INT AUTO_INCREMENT PRIMARY KEY,
  University VARCHAR(255),
  Name VARCHAR(255),
  Interests VARCHAR(255),
  FieldOfStudy VARCHAR(255)
);

CREATE TABLE GeneralResearcherFollowing (
  researcherID INT,
  StartupID INT,
  DateCreated DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (researcherID, StartupID),
  FOREIGN KEY (researcherID) REFERENCES GeneralResearcher(researcherID) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (StartupID) REFERENCES Startup(StartupID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Insights (
  InsightID INT AUTO_INCREMENT PRIMARY KEY,
  DateCreated DATETIME DEFAULT CURRENT_TIMESTAMP,
  Content TEXT,
  Likes INT,
  GeneralResearcher INT,
  FOREIGN KEY (GeneralResearcher) REFERENCES GeneralResearcher(researcherID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE InsightComments (
  commentID INT AUTO_INCREMENT PRIMARY KEY,
  InsightID INT,
  Content TEXT,
  Likes INT,
  ViewCount INT,
  GeneralResearcher INT,
  FOREIGN KEY (InsightID) REFERENCES Insights(InsightID) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (GeneralResearcher) REFERENCES GeneralResearcher(researcherID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE FollowedDeals (
  followedID INT AUTO_INCREMENT PRIMARY KEY,
  FollowerCount INT,
  OppID INT,
  researcherID INT,
  FOREIGN KEY (OppID) REFERENCES InvestmentOpportunities(OppID) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (researcherID) REFERENCES GeneralResearcher(researcherID) ON UPDATE CASCADE ON DELETE CASCADE
);

-- INSERT STATEMENTS BELOW

