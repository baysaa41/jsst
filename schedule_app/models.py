from datetime import timezone

from django.db import models

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    priority = models.IntegerField(default=0)
    busy_periods = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name

    def check_date(self, check_date):
        """
        Check if the teacher is available on the given date.

        :param check_date: date to check (type: datetime.date)
        :return: True if available, False otherwise
        """
        # 1. Check if the date falls within the teacher's availability range
        is_available = self.availabilities.filter(
            start_date__lte=check_date,
            end_date__gte=check_date
        ).exists()

        return is_available

    def check_period(self, check_period):
        """
        Check if the teacher is available during the given period.
        :param check_period: Period object to check availability
        :return: True if the teacher is available, False otherwise
        """
        # Fetch the Period objects that are marked as busy for this teacher
        busy_periods = Period.objects.filter(id__in=self.busy_periods)

        for period in busy_periods:
            # Check if the day of the week matches
            if period.id == check_period.id:
                return False  # Teacher is busy during this period

        return True  # Teacher is available during this period

    def is_teacher_available(self, check_date, check_period):
        date_available = self.check_date(check_date)
        period_available = self.check_period(check_period)
        return date_available and period_available



class TeacherAvailableDates(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='availabilities')
    start_date = models.DateField()
    end_date = models.DateField()
    # Optional: Define specific days and times within the date range
    # For simplicity, this example uses full availability within the date range

    class Meta:
        ordering = ['start_date']
        verbose_name = 'Teacher Availability'
        verbose_name_plural = 'Teacher Availabilities'

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError('End date cannot be earlier than start date.')

    def __str__(self):
        return f"{self.teacher.name}: {self.start_date} to {self.end_date}"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=100,default='D1 анги')
    total_hours = models.IntegerField(default=33)
    remaining_hours = models.IntegerField(default=33)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    priority = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class Period(models.Model):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    WEEKDAYS = [MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY]

    day_of_week = models.IntegerField(default=MONDAY)
    start_time = models.CharField(default='08:00', max_length=10)
    end_time = models.CharField(default='08:40', max_length=10)

    def clean(self):
        if self.day_of_week not in self.WEEKDAYS:
            raise ValidationError('Periods can only be created for Monday to Friday.')

    def __str__(self):
        return f"{self.get_day_of_week_display()}: {self.start_time} - {self.end_time}"

    def get_day_of_week_display(self):
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        return day_names[self.day_of_week]


class Classroom(models.Model):
    name = models.CharField(max_length=100, default='')
    room_number = models.CharField(max_length=10)
    capacity = models.IntegerField()

    def __str__(self):
        return self.room_number

class Schedule(models.Model):
    week = models.IntegerField(default=1)
    day = models.IntegerField(default=0)
    date = models.DateField(blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    period = models.ForeignKey(Period, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.classroom.name}: {self.subject} - {self.day} {self.period.start_time}-аас {self.period.end_time}, {self.subject.teacher.name}"