# Some set up for the application 

from flask import Flask
from flaskext.mysql import MySQL

# create a MySQL object that we will use in other parts of the API
db = MySQL()

def create_app():
    app = Flask(__name__)
    
    # secret key that will be used for securely signing the session 
    # cookie and can be used for any other security related needs by 
    # extensions or your application
    app.config['SECRET_KEY'] = 'someCrazyS3cR3T!Key.!'

    # these are for the DB object to be able to connect to MySQL. 
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = open('/secrets/db_root_password.txt').readline().strip()
    app.config['MYSQL_DATABASE_HOST'] = 'db'
    app.config['MYSQL_DATABASE_PORT'] = 3306
    app.config['MYSQL_DATABASE_DB'] = 'project'  # Change this to your DB name

    # Initialize the database object with the settings above. 
    db.init_app(app)
    
    # Add the default route
    # Can be accessed from a web browser
    # http://ip_address:port/
    # Example: localhost:8001
    @app.route("/")
    def welcome():
        return "<h1>Welcome to the 3200 boilerplate app</h1>"

    # Import the various Beluprint Objects

    from src.acquisitionTarget.acquisitionTarget import acquisitionTarget
    from src.founder.founder import founder
    from src.services.services import services
    from src.tracking.tracking  import tracking
    from src.startup.startup  import startup
    from src.insights.insights import insights
    # Register the routes from each Blueprint with the app object
    # and give a url prefix to each
    app.register_blueprint(services,   url_prefix='/se')
    app.register_blueprint(tracking,    url_prefix='/t')
    app.register_blueprint(startup,    url_prefix='/s')
    app.register_blueprint(acquisitionTarget,    url_prefix='/at')
<<<<<<< HEAD
    #app.register_blueprint(insights,    url_prefix='/in')

=======
    app.register_blueprint(founder, url_prefix='/f')
    #app.register_blueprint(insights, url_prefix="/in")
>>>>>>> 5b51942ea6dfcc4182fc0ace5c11d8461801811c

    # Don't forget to return the app object
    return app