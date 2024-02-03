from django.db import models
from users.models import BaseModel
from django.utils.translation import gettext_lazy as _
from users.models import UserAccount, ULIDField

class Timesheet(BaseModel):

    internal_id = ULIDField(_('timesheet_ulid'), editable=False)
    project = models.CharField(_('project'), max_length=100, unique=True)
    task = models.CharField(_('task'), max_length=100, unique=True)
    date = models.DateField(_('date'), null=True)
    hours = models.FloatField(_("hours"), null=True)

    class Meta:
        verbose_name = 'Timesheet'
        verbose_name_plural = 'Timesheets'

    @classmethod
    def get_timesheet(cls, **criteria):
        return cls.objects.filter(**criteria)

class Attendance(BaseModel):

    DAYS = (
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday'),
    )

    internal_id = ULIDField(_('attendance_ulid'), editable=False)
    date = models.DateField(_('date'), null=True)
    day = models.IntegerField(_('day'), choices=DAYS)
    shift_code = models.CharField(_('shift code'), max_length=100, blank=True)
    in_time = models.TimeField(_("in_time"), auto_now_add=True, null=True)
    out_time = models.TimeField(_("out_time"), auto_now_add=True, null=True)
    total_hours = models.FloatField(_("total_hours"), null=True)
    timesheet = models.ForeignKey(Timesheet, on_delete=models.CASCADE, related_name='attendance')

    class Meta:
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'

    @classmethod
    def get_attendance(cls, **criteria):
        return cls.objects.filter(**criteria)


class Leavetype(BaseModel):

    internal_id = ULIDField(_("leave_type_ulid"), editable=False)
    name = models.CharField(_('leave_name'), max_length=100, unique=True)
    slug = models.SlugField(_('leave_slug'), max_length=100, unique=True)

    class Meta:
        verbose_name = 'Leave Type'
        verbose_name_plural = 'Leave Types'

    @classmethod
    def get_leave_type(cls, **criteria):
        return cls.objects.filter(**criteria)


class LeaveRequest(BaseModel):
    STATUS_TYPES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    internal_id = ULIDField(_("leave_request_ulid"), editable=False)
    status = models.CharField(_('status'), max_length=10, choices=STATUS_TYPES)
    start_date = models.DateTimeField(_("start_date"), null=True)
    end_date = models.DateTimeField(_("end_date"), null=True)
    leave_type = models.ForeignKey(Leavetype, on_delete=models.CASCADE, related_name='leave_requests')

    class Meta:
        verbose_name = 'Leave Request'
        verbose_name_plural = 'Leave Requests'

    @classmethod
    def get_leave_request(cls, **criteria):
        return cls.objects.filter(**criteria)


class LeaveBalance(BaseModel):

    internal_id = ULIDField(_("leave_request_ulid"), editable=False)
    balance = models.IntegerField(_('leave_balance'), blank=True)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='leave_balances')
    leave_type = models.ForeignKey(Leavetype, on_delete=models.CASCADE, related_name='leave_balances')

    class Meta:
        unique_together = ('user', 'leave_type')
        verbose_name = 'Leave Balance'
        verbose_name_plural = 'Leave Balances'

    @classmethod
    def get_leave_balance(cls, **criteria):
        return cls.objects.filter(**criteria)