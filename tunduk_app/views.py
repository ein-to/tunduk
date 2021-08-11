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
from datetime import datetime, date, timedelta

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
        end_date = date_time + timedelta(30)
        date_time = date_time.strftime("%Y-%m-%d")
        end_date = end_date.strftime("%Y-%m-%d")
        content = []
        if type_request == '1':
            pin = request.GET.get('pin')
            phone_number = request.GET.get('phone_number')
            birth_date = request.GET.get('birth_date')
            issued_date = request.GET.get('issued_date')
            data = InitializeRequestForPermission(pin, phone_number, birth_date, issued_date, end_date)
            response = requests.post('http://31.186.53.85', headers=Header, data=data, verify=False)
            res = BeautifulSoup(response.content, 'xml')
            operation_result = res.find('OperationResult').text
            otp_required = res.find('OneTimePasswordRequired').text
            message = res.find('Message').text
            if operation_result == 'false':
                return render(request, 'tunduk_app/InitializeRequestForPermission_response_template.html', {'message': message})
            if operation_result == 'true':
                requestid = res.find('RequestId').text
                if otp_required == 'true':
                    message_otp = 'Код отправлен по SMS'
                else:
                    message_otp = 'Код подтверждения не требуется'
                return render(request, 'tunduk_app/InitializeRequestForPermission_response_template.html', {'message': message,
                                'requestid': requestid, 'message_otp': message_otp})
        if type_request == '2':
            requestid = request.GET.get('requestid')
            code = request.GET.get('code')
            data = SendConfirmationCodeForPermission(requestid, code)
            response = requests.post('http://31.186.53.85', headers=Header, data=data, verify=False)
            res = BeautifulSoup(response.content, 'xml')
            operation_result = res.find('OperationResult').text
            message = res.find('Message').text
            if operation_result == 'false':
                return render(request, 'tunduk_app/SendConfirmationCodeForPermission_response_template.html', {'message': message})
            if operation_result == 'true':
                permissionid = res.find('PermissionId').text
                if requestid == permissionid:
                    message_new = 'RequestId совпадает с PermissionId. Разрешение получено.'
                else:
                    message_new = 'RequestId не совпадает с PermissionId. Разрешение не получено.'
                return render(request, 'tunduk_app/SendConfirmationCodeForPermission_response_template.html', {'message': message, 'message_new': message_new})
        if type_request == '3':
            pin = request.GET.get('pin')
            data = GetPersonalAccountInfoWithSumInfo(pin)
            response = requests.post('http://31.186.53.85', headers=Header, data=data, verify=False)
            employee_name = request.user
            res = BeautifulSoup(response.content, 'xml')
            pin = res.find('PIN').text
            name = res.find('FirstName').text
            last_name = res.find('LastName').text
            patronymic = res.find('Patronymic').text
            issuer = res.find('Issuer').text
            content_part = dict(head={'name': name, 'last_name': last_name, 'patronymic': patronymic, 'pin': pin, 'date_time': date_time,
                                'issuer': issuer, 'employee_name': employee_name})
            content.append(content_part)
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
            return render(request, 'tunduk_app/GetPersonalAccountInfoWithSumInfo_response_template.html', {'content': content})
        if type_request == '4':
            pin = request.GET.get('pin')
            data = GetPensionInfoWithSum(pin)


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
