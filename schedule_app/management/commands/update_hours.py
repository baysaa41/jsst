#schedule_app/generate_schedule.py
from django.core.management.base import BaseCommand, CommandError
from schedule_app.models import Subject, Classroom, Schedule
from django.utils import timezone
from datetime import datetime, timedelta, time
import calendar

class Command(BaseCommand):
    help = 'Generate Schedule objects for all school weeks within a date interval (Monday to Friday).'

    def add_arguments(self, parser):
        parser.add_argument('start_date', type=str, help='Start date in YYYY-MM-DD format')
        parser.add_argument('end_date', type=str, help='End date in YYYY-MM-DD format')

    def handle(self, *args, **kwargs):
        start_date_str = kwargs['start_date']
        end_date_str = kwargs['end_date']

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            raise CommandError('Dates must be in YYYY-MM-DD format.')

        if start_date > end_date:
            raise CommandError('Start date must be before end date.')

        # Find the first Monday on or after the start_date
        start_weekday = start_date.weekday()  # Monday=0, Sunday=6
        if start_weekday != 0:
            start_date += timedelta(days=(7 - start_weekday))

        current_date = start_date
        week_number = 1  # Starting week number

        while current_date <= end_date:
            self.stdout.write(f'Processing Week {week_number}: {current_date}')

            for i in range(5):  # Monday to Friday
                day = current_date + timedelta(days=i)
                if day > end_date:
                    break  # Exit if beyond end_date

                day_name = calendar.day_name[day.weekday()]

                # Example: Assigning subjects and classrooms
                # You might want to customize this part based on your requirements
                # For demonstration, we'll assign all subjects to all classrooms at fixed times

                subjects = Subject.objects.all()
                classrooms = Classroom.objects.all()

                for subject in subjects:
                    for classroom in classrooms:
                        # Define start and end times
                        # Example: 9:00 AM to 10:00 AM
                        start_time = time(9, 0)
                        end_time = time(10, 0)

                        # Create Schedule object
                        schedule, created = Schedule.objects.get_or_create(
                            week=week_number,
                            subject=subject,
                            classroom=classroom,
                            day=day_name,
                            start_time=start_time,
                            end_time=end_time
                        )
                        if created:
                            self.stdout.write(self.style.SUCCESS(
                                f'Created Schedule: {schedule}'
                            ))
                        else:
                            self.stdout.write(self.style.WARNING(
                                f'Schedule already exists: {schedule}'
                            ))

            # Move to the next week
            current_date += timedelta(weeks=1)
            week_number += 1

        self.stdout.write(self.style.SUCCESS('Schedule generation completed.'))
