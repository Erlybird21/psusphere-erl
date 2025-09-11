from django.core.management.base import BaseCommand
from faker import Faker
from studentorg.models import College, Program, Organization, Student, OrgMember


class Command(BaseCommand):
    help = 'Create initial fake data for the application'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # ✅ Create Colleges if none exist
        if College.objects.count() == 0:
            colleges = ["College of Science", "College of Arts", "College of Engineering", "College of Education"]
            for c in colleges:
                College.objects.create(college_name=c)
            self.stdout.write(self.style.SUCCESS(f"{len(colleges)} colleges created successfully."))

        # ✅ Create Programs if none exist
        if Program.objects.count() == 0:
            sample_programs = [
                ("BS Computer Science", "College of Science"),
                ("BS Information Technology", "College of Science"),
                ("BA English", "College of Arts"),
                ("BSEd Mathematics", "College of Education"),
                ("BS Civil Engineering", "College of Engineering"),
            ]
            for prog_name, college_name in sample_programs:
                college = College.objects.filter(college_name=college_name).first()
                if college:
                    Program.objects.create(prog_name=prog_name, college=college)
            self.stdout.write(self.style.SUCCESS(f"{len(sample_programs)} programs created successfully."))

        # ✅ Now create fake orgs, students, memberships
        self.create_organizations(20)
        self.create_students(50)
        self.create_memberships(30)  # increased memberships

    def create_organizations(self, count):
        fake = Faker()
        for _ in range(count):
            words = [fake.word() for _ in range(2)]
            organization_name = ' '.join(words).title()
            Organization.objects.create(
                name=organization_name,
                college=College.objects.order_by('?').first(),
                description=fake.sentence()
            )
        self.stdout.write(self.style.SUCCESS(f"{count} organizations created successfully."))

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
        self.stdout.write(self.style.SUCCESS(f"{count} students created successfully."))

    def create_memberships(self, count):
        fake = Faker()
        for _ in range(count):
            OrgMember.objects.create(
                student=Student.objects.order_by('?').first(),
                organization=Organization.objects.order_by('?').first(),
                date_joined=fake.date_between(start_date="-2y", end_date="today")
            )
        self.stdout.write(self.style.SUCCESS(f"{count} org memberships created successfully."))
