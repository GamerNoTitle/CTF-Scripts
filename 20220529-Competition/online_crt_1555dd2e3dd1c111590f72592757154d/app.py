import datetime
import json
import os
import socket
import uuid
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(16)

def get_crt(Country, Province, City, OrganizationalName, CommonName, EmailAddress):
    root_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, Country),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, Province),
        x509.NameAttribute(NameOID.LOCALITY_NAME, City),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, OrganizationalName),
        x509.NameAttribute(NameOID.COMMON_NAME, CommonName),
        x509.NameAttribute(NameOID.EMAIL_ADDRESS, EmailAddress),
    ])
    root_cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        root_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=3650)
    ).sign(root_key, hashes.SHA256(), default_backend())
    crt_name = "static/crt/" + str(uuid.uuid4()) + ".crt"
    with open(crt_name, "wb") as f:
        f.write(root_cert.public_bytes(serialization.Encoding.PEM))
    return crt_name


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route('/getcrt', methods=['GET', 'POST'])
def upload():
    Country = request.form.get("Country", "CN")
    Province = request.form.get("Province", "a")
    City = request.form.get("City", "a")
    OrganizationalName = request.form.get("OrganizationalName", "a")
    CommonName = request.form.get("CommonName", "a")
    EmailAddress = request.form.get("EmailAddress", "a")
    return get_crt(Country, Province, City, OrganizationalName, CommonName, EmailAddress)


@app.route('/createlink', methods=['GET'])
def info():
    json_data = {"info": os.popen("c_rehash static/crt/ && ls static/crt/").read()}
    return json.dumps(json_data)


@app.route('/proxy', methods=['GET'])
def proxy():
    uri = request.form.get("uri", "/")
    client = socket.socket()
    client.connect(('localhost', 8887))
    msg = f'''GET {uri} HTTP/1.1
Host: test_api_host
User-Agent: Guest
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close

'''
    client.send(msg.encode())
    data = client.recv(2048)
    client.close()
    return data.decode()

app.run(host="0.0.0.0", port=8888)
