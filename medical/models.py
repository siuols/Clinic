from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

STATUS_CHOICES = (
    ('Single', 'Single'),
    ('Married', 'Married'),
    ('Separeted', 'Separeted'),
    ('Widow', 'Widow'),
)

class Department(models.Model):
    user                    = models.ForeignKey(User, on_delete=models.CASCADE)
    code                    = models.CharField(max_length=255)
    description             = models.TextField()
    date_created            = models.DateTimeField(auto_now_add=True)
    date_modified           = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.code)

class Course(models.Model):
    user                    = models.ForeignKey(User, on_delete=models.CASCADE)
    dept_code               = models.ForeignKey('Department', on_delete=models.CASCADE)
    code                    = models.CharField(max_length=255)
    description             = models.TextField()
    date_created            = models.DateTimeField(auto_now_add=True)
    date_modified           = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.code)

class Stock(models.Model):
    user                    = models.ForeignKey(User, on_delete=models.CASCADE)
    barcode                 = models.ImageField(upload_to='media')
    number                  = models.CharField(max_length=255)
    description             = models.TextField()
    quantity                = models.IntegerField()
    actual_used             = models.IntegerField()
    date_created            = models.DateTimeField(auto_now_add=True)
    date_modified           = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.number)

class Patient(models.Model):
    user                    = models.ForeignKey(User, on_delete=models.CASCADE)
    id_number               = models.CharField(max_length=255)
    last_name               = models.CharField(max_length=255)
    first_name              = models.CharField(max_length=255)
    middle_name             = models.CharField(max_length=255)
    course                  = models.ForeignKey('Course', on_delete=models.CASCADE)
    status                  = models.CharField(
                                                max_length=9,
                                                choices=STATUS_CHOICES,
                                                default='single'
                                            )
    date_created            = models.DateTimeField(auto_now_add=True)
    date_modified           = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.id_number)

class History(models.Model):
    user                    = models.ForeignKey(User, on_delete=models.CASCADE)
    id_number               = models.ForeignKey('Patient', on_delete=models.CASCADE)
    item_code               = models.ForeignKey('Course', on_delete=models.CASCADE)
    quantity                = models.CharField(max_length=255)
    complaints              = models.TextField()
    medication              = models.TextField()
    date_created            = models.DateTimeField(auto_now_add=True)
    date_modified           = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.id_number)