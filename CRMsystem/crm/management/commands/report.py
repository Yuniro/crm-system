from django.core.management.base import BaseCommand, CommandError
from crm.models import Report, Employer, Container
from django.utils import timezone


class Command(BaseCommand):
    help = 'just help'

    def handle(self, *args, **options):
        time = timezone.now().strftime('%X')
    if str(Report.objects.all()) == '<QuerySet []>':
        usr = Employer.objects.all()
        num = 0
        while num != len(usr):
            Report(changes='No changed ' + str(usr[num].username), time=time).save()
            num = num + 1
    counteiner_objects = Container.objects.all()
    employer_objects = Employer.objects.all()
    if str(counteiner_objects) not in '<QuerySet []>':
        i = 0
        while i != len(employer_objects) - 1:
            if counteiner_objects[i].information != employer_objects[i].username:
                check_objects = Container.objects.all()
                new_objects = Employer.objects.all()
                count = 0
                while count != len(check_objects):
                    if check_objects[count].information != new_objects[count].username:
                        send_mail('Изменение пользователя',
                                  'You changed username ' + str(check_objects[count].information) + 'to ' + str(
                                      new_objects[count].username),
                                  settings.EMAIL_HOST_USER,
                                  [str(new_objects[count].email)],
                                  fail_silently=False)
                        Report(changes='Changed username to ' + str(new_objects[count]), time=time).save()
                    count = count + 1
                Container.objects.all().delete()
            i = i + 1
    else:
        emp = Employer.objects.all()
        number = 0
        while number != len(emp):
            Container(information=emp[number].username).save()
            number = number + 1
