from django.db import models

# Create your models here.
class Student(models.Model):
    roll = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    city = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    dob = models.DateField()

    def __str__(self):
        return f"{self.roll} - {self.name}"
    
# from django.core.mail import send_mail
# from django.http import JsonResponse
# from rest_framework.views import APIView
# from app.models import Student
# import openpyxl
# from datetime import datetime

# class Parser(APIView):
#     def post(self,request):
#         data = request.FILES['file']
#         workbook = openpyxl.load_workbook(data)
#         sheet = workbook.active

#         stored_count = 0
#         not_stored_count = 0
#         error_data = []

#         for row in sheet.iter_rows(min_row=2, values_only=True):
#             roll, name, age, city, email, dob = row
#             try:
#                 if all([roll, name, age, city, email, dob]):
#                     if not isinstance(roll, str):
#                         raise ValueError("Roll must be a string")
                    
#                     if not isinstance(name, str):
#                         raise ValueError("Name must be a string")

#                     if not isinstance(age, int):
#                         raise ValueError("Age must be an integer")

#                     if not isinstance(email, str) or "@" not in email:
#                         raise ValueError("Invalid email")

#                     try:
#                         dob = datetime.strptime(dob, "%Y-%m-%d")
#                     except ValueError:
#                         raise ValueError("Invalid date format for DOB. Use YYYY-MM-DD")

#                     Student.objects.create(roll=roll, name=name, age=age, city=city, email=email, dob=dob)
#                     stored_count += 1
#                 else:
#                     error_data.append(f"Missing data: Roll: {roll}, Name: {name}, Age: {age}, City: {city}, Email: {email}, DOB: {dob}")
#                     not_stored_count += 1
#             except Exception as e:
#                 error_data.append(f"Error saving data: {str(e)}")
#                 not_stored_count += 1

#         send_email_notification(stored_count, not_stored_count)

#         return JsonResponse({
#             'stored_count': stored_count,
#             'not_stored_count': not_stored_count,
#             'error_data': error_data
#         })

# def send_email_notification(stored_count, not_stored_count):
#     subject = "Excel File Processing Summary"
#     message = f"Data stored in database: {stored_count}\nData not stored: {not_stored_count}"
#     recipient_list = ['xyz@gmail.com'] 
#     send_mail(subject, message, None, recipient_list)
