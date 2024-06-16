from flask import Flask
import sys
from src.logger import logging
from src.exceptions import CustomException

app = Flask(__name__)

@app.route("/",methods = ["GET", "POST"])

def index():
    # try:
    #     raise Exception("Testing implemented exception class")
    # except Exception as e:
    #     exc = CustomException(e, sys)
    #     logging.info("somehting")
    #     logging.info(exc.error_message)
    
    return "Print on the app"

    # logging.info("Testing...")
    

if __name__ == "__main__":
    app.run(debug = True)
    