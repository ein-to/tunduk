from .models import Service, Request_type

def header(type_request):
    service = Service.objects.get(service_id=1)
    userid = service.userid
    membercode = service.membercode
    subsystemcode = service.subsystemcode
    type = service.type
    method = Request_type.objects.get(type_id=type_request, service_id=1)
    method_name = method.method_name
    content = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xro="http://x-road.eu/xsd/xroad.xsd" xmlns:iden="http://x-road.eu/xsd/identifiers" xmlns:prod="http://tunduk-sf.x-road.fi/producer">
<soapenv:Header>
  <xro:userId>%s</xro:userId>
  <xro:service iden:objectType="SERVICE">
     <iden:xRoadInstance>central-server</iden:xRoadInstance>
     <iden:memberClass>%s</iden:memberClass>
     <iden:memberCode>%s</iden:memberCode>
     <iden:subsystemCode>%s</iden:subsystemCode>
     <iden:serviceCode>%s</iden:serviceCode>
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
</soapenv:Header>\n""" % (userid, type, membercode, subsystemcode, method_name)
    return content

def InitializeRequestForPermission(pin, phone_number, birth_date, issued_date, end_date, type_request):
    body = """<soapenv:Body>
      <prod:InitializeRequestForPermission>
         <prod:Pin>%s</prod:Pin>
         <prod:PhoneNumber>%s</prod:PhoneNumber>
         <prod:LastName></prod:LastName>
         <prod:FirstName></prod:FirstName>
         <prod:Patronymic></prod:Patronymic>
         <prod:OrganizationId></prod:OrganizationId>
         <prod:EndDate>%s</prod:EndDate>
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
</soapenv:Envelope>""" % (pin, phone_number, end_date, birth_date, issued_date)
    data = header(type_request) + body
    return data

def GetPersonalAccountInfoWithSumInfo(pin, type_request):
    body = """<soapenv:Body>
      <prod:GetPersonalAccountInfoWithSumInfo>
         <prod:Pin>%s</prod:Pin>
      </prod:GetPersonalAccountInfoWithSumInfo>
   </soapenv:Body>
</soapenv:Envelope>""" % (pin)
    data = header(type_request) + body
    return data

def GetPensionInfoWithSum(pin, type_request):
    body = """<soapenv:Body>
      <prod:GetPensionInfoWithSum>
         <prod:Pin>%s</prod:Pin>
      </prod:GetPensionInfoWithSum>
   </soapenv:Body>
</soapenv:Envelope>""" % (pin)
    data = header(type_request) + body
    return data

def SendConfirmationCodeForPermission(requestid, code, type_request):
    body = """<soapenv:Body>
      <prod:SendConfirmationCodeForPermission>
         <prod:RequestId>%s</prod:RequestId>
         <prod:Code>%s</prod:Code>
      </prod:SendConfirmationCodeForPermission>
   </soapenv:Body>
</soapenv:Envelope>""" % (requestid, code)
    data = header(type_request) + body
    return data
