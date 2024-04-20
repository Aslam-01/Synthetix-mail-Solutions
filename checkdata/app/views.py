from django.core.mail import send_mail
from django.http import JsonResponse
from app.models import Student
import openpyxl
from datetime import datetime
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class Parser(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self,request):
        data = request.FILES['file']
        workbook = openpyxl.load_workbook(data)
        sheet = workbook.active

        error_details = []
        existing_roll = [student['roll'] for student in Student.objects.values('roll')]

        for index, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
            error = {}

            if row[0] is None:
                error['line'] = index
                error['column'] = 'roll'
                error['message'] = 'Roll number cannot be null'
                error_details.append(error)
            elif not str(row[0]).isdigit():
                error['line'] = index
                error['column'] = 'roll'
                error['message'] = 'Roll number should be a number'
                error_details.append(error)

            if row[2] is None:
                error = {}
                error['line'] = index
                error['column'] = 'age'
                error['message'] = 'Age cannot be null'
                error_details.append(error)
            elif not isinstance(row[2], int):
                error = {}
                error['line'] = index
                error['column'] = 'age'
                error['message'] = 'Age must be a valid number'
                error_details.append(error)

            if row[1] is None:
                error = {}
                error['line'] = index
                error['column'] = 'name'
                error['message'] = 'Name cannot be null'
                error_details.append(error)
            elif str(row[1]).isdigit():
                error = {}
                error['line'] = index
                error['column'] = 'name'
                error['message'] = 'Name cannot be a number'
                error_details.append(error)

            if row[3] is None:
                error = {}
                error['line'] = index
                error['column'] = 'city'
                error['message'] = 'City cannot be null'
                error_details.append(error)
            elif str(row[3]).isdigit():
                error = {}
                error['line'] = index
                error['column'] = 'city'
                error['message'] = 'City cannot be a number'
                error_details.append(error)

            if row[4] is None:
                error = {}
                error['line'] = index
                error['column'] = 'email'
                error['message'] = 'Email cannot be null'
                error_details.append(error)
            elif not isinstance(row[4], str) or '@' not in row[4] or '.' not in row[4]:
                error = {}
                error['line'] = index
                error['column'] = 'email'
                error['message'] = 'Email must be a valid email address'
                error_details.append(error)

            if row[5] is None:
                error = {}
                error['line'] = index
                error['column'] = 'dob'
                error['message'] = 'Date of Birth (DOB) cannot be null'
                error_details.append(error)
            else:
                try:
                    dob = datetime.strptime(str(row[5]), '%d-%m-%Y').date()
                except ValueError:
                    error = {}
                    error['line'] = index
                    error['column'] = 'dob'
                    error['message'] = 'Invalid date format for DOB. Use DD-MM-YYYY'
                    error_details.append(error)

            if not error:
                try:
                    if row[0] in existing_roll:
                        student = Student.objects.filter(roll=row[0]).first()
                        student.name = row[1]
                        student.age = row[2]
                        student.city = row[3]
                        student.dob = dob
                        student.email = row[4]
                        student.save()
                        self.stdout.write(self.style.WARNING(f'Student with roll {row[0]} already exists. Data updated.'))
                    else:
                        Student.objects.create(
                            roll=row[0],
                            name=row[1],
                            age=row[2],
                            city=row[3],
                            dob=dob,
                            email=row[4]
                        )
                except Exception as e:
                    error = {}
                    error['line'] = index
                    error['column'] = 'all'
                    error['message'] = str(e)
                    error_details.append(error)

        if error_details:
            subject = 'Errors Encountered During Data Import'
            html_message = render_to_string('email_template.html', {'error_details': error_details})
            plain_message = strip_tags(html_message)  # Strip HTML tags for plain text email
            sender_email = 'mohdshahid5413@gmail.com'
            receiver_email = ['drxaslam7890@gmail.com']
            
            send_mail(subject, plain_message, sender_email, receiver_email, html_message=html_message)

        return JsonResponse({
            'error_details': error_details
        })

    # def send_email_notification(stored_count, not_stored_count):
    #     subject = "Excel File Processing Summary"
    #     message = f"Data stored in database: {stored_count}\nData not stored: {not_stored_count}"
    #     recipient_list = ['shaikhaslam@gmail.com']  # Add your recipient email address here
    #     send_mail(subject, message, None, recipient_list)
