from django.db import models

# Create your models here.
class Service(models.Model):
    service_id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Request_type(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    type_id = models.IntegerField()
    name = models.CharField(max_length=120)

    class Meta:
        unique_together = ['service', 'type_id']

    def __str__(self):
        return "%s  (%s)" % (self.name, self.service.name)


class Requests(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    request_type = models.ForeignKey(Request_type, on_delete=models.CASCADE)
    employee_name = models.CharField(max_length=120)
    date = models.DateTimeField()
    inn = models.IntegerField()

    def __str__(self):
        return self.inn
