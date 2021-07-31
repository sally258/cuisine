from flask import Flask
from flask_cors import CORS, cross_origin
from flask import request
from Database import *

helper = DBHelper('localhost', '3306', 'root', 'password', 'cuisine')

# Khởi tạo Flask server Backend
app = Flask(__name__)

# Apply Flask CORS
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/dish', methods = ['POST', 'GET'])
@cross_origin(orgin='*')
def dish_process():
    dish_name = request.args.get('name')
    dish_name = dish_name.replace('%20', ' ')
    sql = "select content from dish where dish_name = \'" + dish_name + "\'"
    lst = helper.select(sql)

    # return {'content' : lst[0][0]}
    return lst[0][0]

@app.route('/dish_list', methods = ['POST', 'GET'])
@cross_origin(origin='*')
def dish_list_process():
    dish_list = {}
    sql = "select dish_name, content from dish"
    for dish_name in helper.select(sql):
        dish_list[dish_name[0]] = dish_name[1]
    return dish_list

# Start Backend
if __name__ == '__main__':
    app.run(host='127.0.0.1', port='3333')

