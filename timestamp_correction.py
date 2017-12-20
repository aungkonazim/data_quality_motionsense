# import numpy as np
# import pandas as pd
# import pickle
#
# ids = [2952]
# for i,id in enumerate(ids):
#     filename = 'C:\\Users\\aungkon\\Desktop\\jhu-pilot\\' + str(ids[i]) + '\\data_final.p'
#     data_final = pickle.load(open( filename, "rb" ))
#     time = []
#     for index,element in enumerate(data_final):
#         print(element)
from flask import Flask, render_template, request

app = Flask(__name__)

# Index page, no args
@app.route('/')
def index():
    name = request.args.get("name")
    if name == None:
        name = "Edward"
    return render_template("index.html", name=name)

# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
    app.run(port=5000, debug=True)