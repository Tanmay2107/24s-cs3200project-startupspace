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

**Founder:**
  * View the startups that have been founded by the founder.
  * Update any details regarding any of the startups
  * Delete a startup made by the founder
  * Add an new startup
  * Add documents and financial metrics for any of their startups

**Venture Capitalist:**
  * View venture capitalist profile
  * View investment analytics
  * View view startup information including financial metrics, uploaded documents, team members etc.
  * View & edit current investment opportunities

**Acquirer:**
  * Track startups
  * Update deal status details for a selected tracked startup
  * Explore acquisition targets (startups) and add new targets to the tracked deal table
  * View company details for selected startups for further research
 
**General Researcher:**
  * View all general researchers
  * View all insights
  * View insights made by a specific researcher through a dropdown
  * View a specific deal a researcher is following
  * View the comments of a specific insight (through row selection)
  * Create, update, delete insights
  * Create comments for a specific insight

# IMPORTANT
We had some serious issues merging/pulling on appsmith so in the end we had to redo all our work on one computer. **We've included a link to the json file in our submission pdf which can be loaded in appsmith once the docker containers are running.** Thanks!

