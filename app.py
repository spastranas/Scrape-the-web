


from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

 
# Create connection variable. this one will connecto to my own computer.
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect/Create database. 
db = client.MarsDB

# Drops collection if it already exists
db.MarsFactsCollection.drop()

db.MarsFactsCollection.insert_many(
                    [   
                    {"Current Weather":"", "Latest News":""}
                    ]
    )

# Set Home route
@app.route('/')
def index():
    # Store the entire team collection in a list. so the dictionaries will be passed as a list.
    MyVariableToPass = list(db.MarsFactsCollection.find())

 
    

    # Return the template with the teams list passed in
    return render_template('index.html', FlaskVariableName=MyVariableToPass)



@app.route("/scrape")
def scraper():

    # Run scrape py script and save the dictionary it returns into a variable.
    Mars_data = scrape_mars.scrape()
    # Drops collection if it already exists
    db.MarsFactsCollection.drop()

    db.MarsFactsCollection.insert_many(
                    [   
                    Mars_data
                    ]
    )

    
    return redirect("/", code=302) # this pice of code redirects to the home route, which in ture renders index.html with the updated parameter.




if __name__ == "__main__":
    app.run(debug=True)
