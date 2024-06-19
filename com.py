from OpenSSL import crypto
import os
import sys
import datetime
import whois  # pip install whois

if len(sys.argv) > 1:
    data = sys.argv[1].split("-")  # Разбиваем переданные данные по разделителю "-"
    dom = data[0]
    org = data[1]
    town = data[3]
    city = data[4]
    code = data[2]

# Variables
TYPE_RSA = crypto.TYPE_RSA
HOME = os.path.join(os.path.expanduser("~"), "Desktop", "проект")
now = datetime.datetime.now()
d = now.date()

# Pull these out of scope
cn = data[0]
key = crypto.PKey()
keypath = os.path.join(HOME, "cert_key", cn + '-' + str(d) + '.key')
csrpath = os.path.join(HOME, "cert_key", cn + '-' + str(d) + '.csr')
crtpath = os.path.join(HOME, "cert_key", cn + '-' + str(d) + '.crt')

#Generate the key
def generatekey():
    if os.path.exists(keypath):
        sys.exit(1)
    else:
        key.generate_key(TYPE_RSA, 4096)
        with open(keypath, "wb") as f:  # Открываем файл в бинарном режиме
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
    

generatekey()

#Generate CSR
def generatecsr():
    c = data[2]
    st = data[3]
    l = data[4]
    o = data[1]
    ou = 'IT'

    req = crypto.X509Req()
    req.get_subject().CN = cn
    req.get_subject().countryName = c[:2]
    req.get_subject().ST = st
    req.get_subject().L = l
    req.get_subject().O = o
    req.get_subject().OU = ou
    req.set_pubkey(key)
    req.sign(key, "sha256")

    with open(csrpath, "wb") as f:
        f.write(crypto.dump_certificate_request(crypto.FILETYPE_PEM, req))
            
    #Generate the certificate

    cert = crypto.X509()
    cert.get_subject().CN = cn
    cert.get_subject().countryName = c[:2]
    cert.get_subject().ST = st
    cert.get_subject().L = l
    cert.get_subject().O = o
    cert.get_subject().OU = ou
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(315360000)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(key)
    cert.sign(key, "sha256")
    
    with open(crtpath, "wb") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

generatecsr()