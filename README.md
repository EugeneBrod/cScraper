# About

This is a Craigslist scraper that you can use to get the jump on the best deals on Craigslist.

# Setup

1. cd into the server directory

> cd server

2. make sure you have flask, flask_cors, and numpy installed, preferably in a virtual environment.

> pip install flask
>
> pip install flask_cors
>
> pip install numpy

3. Open config.ini and input your stmp server credentials.

4. launch the server

> python app.py

5. open a new terminal window at the project root and head over to the client directory

> cd client

6. make sure you have all the node dependencies installed

> npm install

7. start up the front-end server

> npm run serve

At this point the you should be able to open your brower and direct it to http://localhost:8080/ and see the running web app.

# Usage

From there it should be pretty self explainatory. Feed the web app the intended recipients for the scraper, and then feed it a comma separated list of craigslist URLs to scrape. Make sure that you have sufficient filters on your CL search as to not spam yourself.

# Thank you

Thank you for using my scraper. Hope you can get a nice car with it!
