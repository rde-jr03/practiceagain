from flask import Flask, make_response, jsonify, request, abort
from flask_mysqldb import MySQL
from flask_httpauth import HTTPBasicAuth
import dicttoxml
from xml.dom.minidom import parseString

app = Flask(__name__)
auth = HTTPBasicAuth()

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "classicmodels"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@auth.verify_password
def verify_password(username, password):
    return username == "ron" and password == "110"

def convert_to_xml(data):
    xml = dicttoxml.dicttoxml(data, custom_root='response', attr_type=False)
    dom = parseString(xml)
    return dom.toprettyxml()

def format_response(data):
    response_format = request.args.get('format', 'json').lower()
    if response_format == 'xml':
        xml_data = convert_to_xml(data)
        return make_response(xml_data, 200, {'Content-Type': 'application/xml'})
    else:
        return make_response(jsonify(data), 200)
    
@app.route("/protected")
@auth.login_required
def protected_resource():
    return jsonify({"message": "You are authorized to acces this resource."})


@app.route("/")
@auth.login_required
def hello_world():
    return "<p>Hello, World!</p>"


def data_fetch(query):
    cur - mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data



if __name__ == "__main__":
    app.run(debug=True)