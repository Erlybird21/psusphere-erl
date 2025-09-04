from django.core.management.base import BaseCommand
from faker import Faker
from psusphere_app.models import College, Program, Organization, Student, OrgMember


class Command(BaseCommand):
    help = 'Create initial data for the application'

    def handle(self, *args, **kwargs):
        if College.objects.count() == 0:
            self.stderr.write(self.style.ERROR("⚠ No colleges found. Please create Colleges first."))
            return
        
        if Program.objects.count() == 0:
            self.stderr.write(self.style.ERROR("⚠ No programs found. Please create Programs first."))
            return

        self.create_organizations(20)   # one call, 20 orgs
        self.create_students(50)
        self.create_memberships(10)

    def create_organizations(self, count):
        fake = Faker()
        for _ in range(count):
            words = [fake.word() for _ in range(2)]  # two words
            organization_name = ' '.join(words)
            Organization.objects.create(
                name=organization_name.title(),
                college=College.objects.order_by('?').first(),
                description=fake.sentence()
            )
        self.stdout.write(self.style.SUCCESS(
            f"{count} organizations created successfully."))

    def create_students(self, count):
        fake = Faker('en_PH')
        for _ in range(count):
            Student.objects.create(
                student_id=f"{fake.random_int(2020, 2025)}-{fake.random_int(1, 8)}-{fake.random_number(digits=4)}",
                lastname=fake.last_name(),
                firstname=fake.first_name(),
                middlename=fake.last_name(),
                program=Program.objects.order_by('?').first()
            )
        self.stdout.write(self.style.SUCCESS(
            f"{count} students created successfully."))

    def create_memberships(self, count):
        fake = Faker()
        for _ in range(count):
            OrgMember.objects.create(
                student=Student.objects.order_by('?').first(),
                organization=Organization.objects.order_by('?').first(),
                date_joined=fake.date_between(start_date="-2y", end_date="today")
            )
        self.stdout.write(self.style.SUCCESS(
            f"{count} org memberships created successfully."))
