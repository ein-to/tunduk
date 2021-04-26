from django.shortcuts import render
import requests
from xml.etree.ElementTree import fromstring, ElementTree

# Create your views here.
def index(request):
    return render(request, 'tunduk_app/index.html')

def test_request(request):
    Header = {'Content-type': 'application/xml; charset=UTF-8'}
    #data = open('request.xml')
    #data = InitializeRequestForPermission()
    data = test_method_zags()
    data = data.encode('utf-8')
    #response = requests.get('https://31.186.53.85', headers=Header, data=data, cert=('subsystemName.crt', 'subsystemName.key'))
    response = requests.post('http://31.186.53.85', headers=Header, data=data, verify=False)
    #response = requests.get('https://api.github.com')
    req = response.content
    tree = ElementTree(fromstring(req))
    root = tree.getroot()

    message = root.find('faultcode')
    #message = message.text
    filename = 'response.xml'
    ff = open(filename, 'a')
    ff.write(req.decode("utf-8"))
    ff.close()

    return render(request, 'tunduk_app/response.html', {'response': message})

def InitializeRequestForPermission():
    data = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xro="http://x-road.eu/xsd/xroad.xsd" xmlns:iden="http://x-road.eu/xsd/identifiers" xmlns:prod="http://tunduk-sf.x-road.fi/producer">
   <soapenv:Header>
      <xro:userId> fc12b8d1-dc09-49f1-95f7-911bb2f97cc0</xro:userId>
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
         <prod:Pin>11111111111111</prod:Pin>
         <prod:PhoneNumber>+996700856315</prod:PhoneNumber>
         <prod:LastName>Тестов</prod:LastName>
         <prod:FirstName>Тест</prod:FirstName>
         <prod:Patronymic>Тестович</prod:Patronymic>
         <prod:OrganizationId> fc12b8d1-dc09-49f1-95f7-911bb2f97cc0</prod:OrganizationId>
         <prod:EndDate>2021-06-01</prod:EndDate>
         <prod:SignedCmsAsBase64></prod:SignedCmsAsBase64>
         <prod:BirthDate>1999-12-21</prod:BirthDate>
         <prod:PassportAddress>тест</prod:PassportAddress>
         <prod:FactAddress>тест</prod:FactAddress>
         <prod:PassportNumberAndSeries>ID123321</prod:PassportNumberAndSeries>
         <prod:PassportIssuedDate>2015-01-01</prod:PassportIssuedDate>
         <prod:PassportIssuedBy>asdwa</prod:PassportIssuedBy>
         <prod:Email>doolotbekuulu00@gmail.com</prod:Email>
      </prod:InitializeRequestForPermission>
   </soapenv:Body>
</soapenv:Envelope>"""

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
