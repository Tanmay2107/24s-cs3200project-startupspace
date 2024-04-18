# StartupSpace

90% of startups fail, many simply because of a lack of cash on hand to fund growth. Startup founders rely heavily on bootstrapping their companies or building industry connections to find stabile funding, which is never easy to do. StartupSpace helps ease the pains of fundraising through a comprehensive platform that helps connect startups to investors. On the platform, startups can provide financial and strategic information to investors, creating awareness about their company. Investors can use this information to scout their next target and build an in house tracker to monitor their deal flow. The platform is also open to university researchers who can view closed deals, read public information on investors and startups, and publish insights to the platform for others to read. The platform's user personas are summarized below:

  1. Founder: The founder of a given startup. 
  2. Venture Capitalist: An venture investor looking for a new strategic partnership with a startup to add to their portfolio.
  3. Acquirer: A large corporate investor looking to buy out startups for mergers & acquisitions.
  4. General Researcher: An individual interested in understanding and staying updated on the private investments market.


# Database
Below includes the primary tables and attributes utilized in our database:
  * Startup: StartupID, AcqID, Industry, GrowthStage, City, Name
  * Founder: FounderID, CredibilityRating, NumberOfCompanies, PhoneNumber, Name
  * TeamMembers: MemberID, StartupID, Email, PhoneNumber, Name
  * FinancialMetrics: MetricID, StartupID, MetricTitle, MetricValue
  * Document: DocID, StartupID, CharacterCount, PageCount, WordCount, FileSize, DocumentType
  * Acquirers: AcqID, Name, Sector
  * AcquisitionTarget: TargetID, AcqID, StartupID, DateIdentified, Interested, Status
  * VentureCapitalist: VCID, PortfolioSize, Industry_Preference, Name
  * InvestmentOpportunities: OppID, StartupID, Terms, Description, FundingRound
  * InvestmentAnalytics: AnalyticsID, VCID, PerformanceMetric, PortfolioDiversity, TotalInvested, NumberOfDeals
  * Insights: InsightID, GeneralResearcher, Likes, Content, DateCreated
  * InsightComments: CommentID, GeneralResearcher, ViewCount, Likes, Content, InsightID

The database also includes the following tables that store lists of values or solve M:M relationships:
  * GrowthStageList: GrowthStage
  * IndustryList: Industry
  * GeneralResearcherFollowing: StartupID, ResearcherID, DateCreated
  * StartupFounder: FounderID, StartupID
  * FollowedDeals: FollowedID, OppID, FollowerCount
  * InvestmentOpportunitiesToVC: VCID, OppID

# Features

Our Flask API contains routes for four different personas: The founder, venture capitalist, acquirer, and general researcher. They each have the following features:
 * Founder: *
  * sefsdf

* Venture Capitalist: *
  * sesdfsdf

* Acquirer: *
  * sdfsdf
 
* General Researcher: *
  * sdfsdfs
 
# Docker Compose

To start the application: build the images with docker compose build. Start the containers with docker compose up. To run in detached mode, run docker compose up -d.

# AppSmith
Appsmith functions as our front end. It takes in the data from the personas, which grabs our information from our VS Code and Datagrip to display in the front end.

# Link to Walkthrough

