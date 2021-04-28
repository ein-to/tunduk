from django.shortcuts import render
import requests
from xml.etree.ElementTree import fromstring, ElementTree
from bs4 import BeautifulSoup

# Create your views here.
def index(request):
    return render(request, 'tunduk_app/index.html')

def send_request_template(request):
    return render(request, 'tunduk_app/send_request_template.html')

def send_request(request):
    Header = {'Content-type': 'text/xml; charset=UTF-8'}
    #data = open('request.xml')
    type_request = request.GET.get('type_request')
    if type_request == '1':
        pin = request.GET.get('pin')
        phone_number = request.GET.get('phone_number')
        birth_date = request.GET.get('birth_date')
        issued_date = request.GET.get('issued_date')

        data = InitializeRequestForPermission(pin, phone_number, birth_date, issued_date)
        #data = data.encode('utf-8')
        filename = 'result.xml'
        f = open(filename, 'a')
        f.write(str(data))
        f.close()

    #data = InitializeRequestForPermission()
    #data = test_method_zags()
    #data = data.encode('utf-8')
    #response = requests.get('https://31.186.53.85', headers=Header, data=data, cert=('subsystemName.crt', 'subsystemName.key'))
    response = requests.post('http://31.186.53.85', headers=Header, data=data, verify=False)
    #response = requests.get('https://api.github.com')
    req = response.content
    #tree = ElementTree(fromstring(req))
    #root = tree.getroot()

    #message = root.find('Message')
    #message = message.text
    filename = 'response.xml'
    ff = open(filename, 'a')
    ff.write(req.decode('utf-8'))
    ff.close()

    res = BeautifulSoup(response.content, 'xml')
    servicecode = res.find('a:serviceCode').text
    message = res.find('Message').text

    return render(request, 'tunduk_app/response.html', {'response': message, 'servicecode': servicecode})

def InitializeRequestForPermission(pin, phone_number, birth_date, issued_date):
    data = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xro="http://x-road.eu/xsd/xroad.xsd" xmlns:iden="http://x-road.eu/xsd/identifiers" xmlns:prod="http://tunduk-sf.x-road.fi/producer">
   <soapenv:Header>
      <xro:userId>b59fa801-8456-4577-8b33-8b99fa52317d</xro:userId>
      <xro:service iden:objectType="SERVICE">
         <iden:xRoadInstance>central-server</iden:xRoadInstance>
         <iden:memberClass>GOV</iden:memberClass>
         <iden:memberCode>70000003</iden:memberCode>
         <iden:subsystemCode>sf-personal-data</iden:subsystemCode>
         <iden:serviceCode>InitializeRequestForPermission</iden:serviceCode>
      </xro:service>
      <xro:protocolVersion>4.0</xro:protocolVersion>
      <xro:issue>?</xro:issue>
      <xro:id>?</xro:id>
      <xro:client iden:objectType="SUBSYSTEM">
         <iden:xRoadInstance>central-server</iden:xRoadInstance>
         <iden:memberClass>COM</iden:memberClass>
         <iden:memberCode>60000006</iden:memberCode>
         <iden:subsystemCode>changan-service</iden:subsystemCode>
      </xro:client>
   </soapenv:Header>
   <soapenv:Body>
      <prod:InitializeRequestForPermission>
         <prod:Pin>%s</prod:Pin>
         <prod:PhoneNumber>%s</prod:PhoneNumber>
         <prod:LastName></prod:LastName>
         <prod:FirstName></prod:FirstName>
         <prod:Patronymic></prod:Patronymic>
         <prod:OrganizationId></prod:OrganizationId>
         <prod:EndDate>2021-06-01</prod:EndDate>
         <prod:SignedCmsAsBase64></prod:SignedCmsAsBase64>
         <prod:BirthDate>%s</prod:BirthDate>
         <prod:PassportAddress></prod:PassportAddress>
         <prod:FactAddress></prod:FactAddress>
         <prod:PassportNumberAndSeries></prod:PassportNumberAndSeries>
         <prod:PassportIssuedDate>%s</prod:PassportIssuedDate>
         <prod:PassportIssuedBy></prod:PassportIssuedBy>
         <prod:Email></prod:Email>
      </prod:InitializeRequestForPermission>
   </soapenv:Body>
</soapenv:Envelope>""" % (pin, phone_number, birth_date, issued_date)

    return data

def test_method_zags():
    data = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xro="http://x-road.eu/xsd/xroad.xsd" xmlns:iden="http://x-road.eu/xsd/identifiers">
   <soapenv:Header>
      <xro:protocolVersion>4.0</xro:protocolVersion>
      <xro:id>GUID-HERE</xro:id>
      <xro:userId>SUbsystemCheck</xro:userId>
      <xro:service iden:objectType="SERVICE">
         <iden:xRoadInstance>central-server</iden:xRoadInstance>
         <iden:memberClass>GOV</iden:memberClass>
         <iden:memberCode>70000005</iden:memberCode>
         <iden:subsystemCode>zags-service</iden:subsystemCode>
         <iden:serviceCode>listMethods</iden:serviceCode>
         <iden:serviceVersion>v1</iden:serviceVersion>
      </xro:service>
      <xro:client iden:objectType="SUBSYSTEM">
         <iden:xRoadInstance>central-server</iden:xRoadInstance>
         <iden:memberClass>COM</iden:memberClass>
         <iden:memberCode>60000006</iden:memberCode>
         <iden:subsystemCode>changan-service</iden:subsystemCode>
      </xro:client>
   </soapenv:Header>
   <soapenv:Body>
      <xro:listMethods/>
   </soapenv:Body>
</soapenv:Envelope>"""

    return data
