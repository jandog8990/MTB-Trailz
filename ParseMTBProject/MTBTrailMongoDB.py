from pymongo import MongoClient
from pymongo import TEXT
from pymongo.server_api import ServerApi
from dotenv import dotenv_values
from pandas import DataFrame
import json

# -----------------------------------------------------
# ---- PyMongo DB INSERT/GET/DELETE ----
# -----------------------------------------------------
class MTBTrailMongoDB:

    # -----------------------------------------------------
    # --------- PyMongo DB Connection -----------
    # -----------------------------------------------------
    # This is the main MTB Trail MongoDB class that
    # accesses the stored tables as well as inserts
    # new data from the parsing of trail json lines
    # -----------------------------------------------------

    # get the database 
    def get_database(self):
        config = dotenv_values(".env")
        URL_STRING = config["ATLAS_URI"]
        DB_NAME = config["DB_NAME"]
        print("URL_STRING = " + URL_STRING) 
        print("DB_NAME = " + DB_NAME)
        
        # connect to MongoDB client
        client = MongoClient(URL_STRING, server_api=ServerApi('1'))
        mtb_db = client[DB_NAME]
        return mtb_db

    # ------------------------------------------------
    # ----- CREATE INDEXES MTB Trail Route/Descs -----
    # ------------------------------------------------
    def create_indexes(self, db):
        print("--- OLD ROUTE INDEX ---") 
        #db.mtb_trail_routes.drop_index('_id') 
        print(db.mtb_trail_routes.index_information())
        db.mtb_trail_routes.drop_indexes() 
        # db.mtb_trail_routes.create_index('route_name')
        print("--- NEW ROUTE INDEX ---") 
        print(db.mtb_trail_routes.index_information())
        
        print("--- OLD DESC INDEX ---") 
        #db.mtb_trail_route_descriptions.drop_index('_id') 
        print(db.mtb_trail_route_descriptions.index_information())
        print(db.mtb_trail_route_descriptions.drop_indexes())
        # db.mtb_trail_route_descriptions.create_index('mtb_trail_route_id')
        print("--- NEW DESC INDEX ---") 
        print(db.mtb_trail_route_descriptions.index_information())

    # -----------------------------------------------------
    # ---------- INSERT MTB Trail Route Tables ------------ 
    # -----------------------------------------------------
    
    def serialize_mtb_trail_route_data(self, mtbTrailRoutes):
        
        print("MTB Trail Route:")
        '''
        stateArea = mtbTrailRoute["trail_area"]["state"]
        stateAreaJson = json.dumps(stateArea.__dict__)
        print(stateAreaJson)
        print("\n")
        ''' 
      
        # loop through the mtb trail routes and serialize the trail area 
        for mtbTrailRoute in mtbTrailRoutes: 
            trailAreaDict = mtbTrailRoute["trail_area"]
            '''
            for k,v in trailAreaDict.items():
                print(f"{k} : {v}")
            print("\n")
            ''' 
            serializedTrailArea = dict((k, json.dumps(v.__dict__)) for k, v in trailAreaDict.items())

            # TODO: Need to figure out how to serialize the json strings back to object space
            mtbTrailRoute["trail_area"] = serializedTrailArea
        return mtbTrailRoutes        
    
    def insert_mtb_trail_routes(self, db, mtbTrailRoutes):

        """
        MTB Trails Insertion into the PyMongo DB
        """
        # let's insert sample mtb trail route 
        db.mtb_trail_routes.insert_many(mtbTrailRoutes)

    def insert_mtb_trail_route_descriptions(self, db, mtbTrailRouteDescriptions):
        # # insert the sample mtb trail descriptions
        # loop through list of lists and insert 
        description_collection = db["mtb_trail_route_descriptions"]
        description_collection.insert_many(mtbTrailRouteDescriptions) 

    def find_mtb_data(self, db):
        # get the tables 
        trail_routes = db["mtb_trail_routes"]
        # trail_descriptions = db["mtb_trail_route_descriptions"]

        # query the table info
        routeItems = trail_routes.find()
        # descItems = trail_descriptions.find()

        # convert the collections to data frames
        routeDF = DataFrame(routeItems)
        # descDF = DataFrame(descItems)

        print("--- Route DF ---")
        print(routeDF)
        print("\n")

        # print("--- Desc DF ---")
        # print(descDF)
        # print("\n")