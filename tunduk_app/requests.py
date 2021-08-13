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

    return data

def GetPersonalAccountInfoWithSumInfo(pin):
    data = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xro="http://x-road.eu/xsd/xroad.xsd" xmlns:iden="http://x-road.eu/xsd/identifiers" xmlns:prod="http://tunduk-sf.x-road.fi/producer">
   <soapenv:Header>
      <xro:userId>b59fa801-8456-4577-8b33-8b99fa52317d</xro:userId>
      <xro:service iden:objectType="SERVICE">
         <iden:xRoadInstance>central-server</iden:xRoadInstance>
         <iden:memberClass>GOV</iden:memberClass>
         <iden:memberCode>70000003</iden:memberCode>
         <iden:subsystemCode>sf-personal-data</iden:subsystemCode>
         <iden:serviceCode>GetPersonalAccountInfoWithSumInfo</iden:serviceCode>
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
      <prod:GetPersonalAccountInfoWithSumInfo>
         <prod:Pin>%s</prod:Pin>
      </prod:GetPersonalAccountInfoWithSumInfo>
   </soapenv:Body>
</soapenv:Envelope>""" % (pin)
    return data

def GetPensionInfoWithSum(pin):
    data = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xro="http://x-road.eu/xsd/xroad.xsd" xmlns:iden="http://x-road.eu/xsd/identifiers" xmlns:prod="http://tunduk-sf.x-road.fi/producer">
   <soapenv:Header>
      <xro:userId>b59fa801-8456-4577-8b33-8b99fa52317d</xro:userId>
      <xro:service iden:objectType="SERVICE">
         <iden:xRoadInstance>central-server</iden:xRoadInstance>
         <iden:memberClass>GOV</iden:memberClass>
         <iden:memberCode>70000003</iden:memberCode>
         <iden:subsystemCode>sf-personal-data</iden:subsystemCode>
         <iden:serviceCode>GetPensionInfoWithSum</iden:serviceCode>
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
      <prod:GetPensionInfoWithSum>
         <prod:Pin>%s</prod:Pin>
      </prod:GetPensionInfoWithSum>
   </soapenv:Body>
</soapenv:Envelope>""" % (pin)
    return data

def SendConfirmationCodeForPermission(requestid, code):
    data = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xro="http://x-road.eu/xsd/xroad.xsd" xmlns:iden="http://x-road.eu/xsd/identifiers" xmlns:prod="http://tunduk-sf.x-road.fi/producer">
   <soapenv:Header>
      <xro:userId>b59fa801-8456-4577-8b33-8b99fa52317d</xro:userId>
      <xro:service iden:objectType="SERVICE">
         <iden:xRoadInstance>central-server</iden:xRoadInstance>
         <iden:memberClass>GOV</iden:memberClass>
         <iden:memberCode>70000003</iden:memberCode>
         <iden:subsystemCode>sf-personal-data</iden:subsystemCode>
         <iden:serviceCode>SendConfirmationCodeForPermission</iden:serviceCode>
      </xro:service>
      <xro:protocolVersion>4.0</xro:protocolVersion>
      <xro:issue>?</xro:issue>
      <xro:id>?</xro:id>
      <xro:client iden:objectType="SUBSYSTEM">
         <iden:xRoadInstance>central-server</iden:xRoadInstance>
         <iden:memberClass># COM: </iden:memberClass>
         <iden:memberCode>60000006</iden:memberCode>
         <iden:subsystemCode>changan-service</iden:subsystemCode>
      </xro:client>
   </soapenv:Header>
   <soapenv:Body>
      <prod:SendConfirmationCodeForPermission>
         <prod:RequestId>%s</prod:RequestId>
         <prod:Code>%s</prod:Code>
      </prod:SendConfirmationCodeForPermission>
   </soapenv:Body>
</soapenv:Envelope>""" % (requestid, code)
    return data
