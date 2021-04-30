from django.shortcuts import render, redirect
import requests
from xml.etree.ElementTree import fromstring, ElementTree
from bs4 import BeautifulSoup
from django.template.loader import render_to_string, get_template
import html
import pdfkit
from django.http import HttpResponse
import os
from .forms import LoginForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from datetime import datetime, date

# Create your views here.
@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    request.session.set_expiry(2400)
                    login(request, user)
                    return render(request, 'tunduk_app/index.html')
                else:
                    return HttpResponse('Disabled account')
            else:
                message = 'Неверный логин или пароль'
                return render(request, 'tunduk_app/login.html', {'form': form, 'message': message})
    else:
        form = LoginForm()
    return render(request, 'tunduk_app/login.html', {'form': form})

def logout_request(request):
    logout(request)
    return redirect('user_login')


def index(request):
    if request.user.is_authenticated:
        return render(request, 'tunduk_app/index.html')
    else:
        return user_login(request)

def send_request_template(request):
    if request.user.is_authenticated:
        return render(request, 'tunduk_app/send_request_template.html')
    else:
        return user_login(request)

def send_request(request):
    if request.user.is_authenticated:
        Header = {'Content-type': 'text/xml; charset=UTF-8'}
        type_request = request.GET.get('type_request')
        date_time = datetime.now()
        date_time = date_time.strftime("%Y-%m-%d")
        if type_request == '1':
            pin = request.GET.get('pin')
            phone_number = request.GET.get('phone_number')
            birth_date = request.GET.get('birth_date')
            issued_date = request.GET.get('issued_date')
            data = InitializeRequestForPermission(pin, phone_number, birth_date, issued_date)
        if type_request == '3':
            pin = request.GET.get('pin')
            data = GetPersonalAccountInfoWithSumInfo(pin)
        if type_request == '4':
            pin = request.GET.get('pin')
            data = GetPensionInfoWithSum(pin)

        response = requests.post('http://31.186.53.85', headers=Header, data=data, verify=False)

        content = []
        employee_name = request.user
        res = BeautifulSoup(response.content, 'xml')
        servicecode = res.find('a:serviceCode').text
        pin = res.find('PIN').text
        name = res.find('FirstName').text
        last_name = res.find('LastName').text
        patronymic = res.find('Patronymic').text
        issuer = res.find('Issuer').text
        cont1 = dict(head={'name': name, 'last_name': last_name, 'patronymic': patronymic, 'pin': pin, 'date_time': date_time,
                            'issuer': issuer, 'servicecode': servicecode, 'employee_name': employee_name})
        content.append(cont1)
        operation_result = res.find('OperationResult').text
        if operation_result == 'false':
             message = res.find('Message').text
             cont = {'message': message}
             content.append(cont)
        if operation_result == 'true':
            name = res.find('FirstName').text
            for i in res.find_all('WorkPeriodWithSumDto'):
                cont = {'payer': i.Payer.string, 'salary': i.Salary.string, 'inn': i.INN.string,
                        'numsf': i.NumSF.string, 'date_begin': i.DateBegin.string, 'date_end': i.DateEnd.string}
                content.append(cont)

        global pdf_content
        pdf_content = content

        return render(request, 'tunduk_app/response.html', {'content': content})
    else:
        return user_login(request)

def pdf(request):
    if request.user.is_authenticated:
        content = pdf_content
        template = get_template('tunduk_app/pdf_template.html')
        html = template.render({'content': content})
        path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        options = {
                    "enable-local-file-access": None
                    }
        pdfkit.from_string(str(html), 'out.pdf', configuration=config, options=options)
        pdf = open("out.pdf", 'rb')
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=SF.pdf'
        os.remove('out.pdf')
        pdf.close()
    else:
        return user_login(request)

    return response



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
