"""
Custom User Model module for user profile management
Inherit the abstract user model and add additional field
"""

from django.contrib.auth.models import AbstractUser
from django.db import models

from core.constants import TRAINER, TRAINEE


class User(AbstractUser):
    """Custom defined user model for the app, adding profile fields"""

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    email = models.EmailField(unique=True)
    role = models.CharField(
        choices=(
            (TRAINER, "Trainer"),
            (TRAINEE, "Trainee"),
        ),
        default=TRAINER,
        blank=True,
        null=True,
        max_length=10,
    )

    def __str__(self):
        """return a formated string"""
        return f"{self.username}"


class UserProfile(models.Model):
    """User profile class for storing aditional profile settings"""

    choices = [("male", "Male"), ("female", "Female"), ("other", "Rather Not to say")]
    gender = models.CharField(choices=choices, default="none", max_length=10)
    bio = models.TextField(max_length=500)
    profile_image = models.ImageField(default="man.png")
    user = models.OneToOneField(
        to=User, on_delete=models.CASCADE, related_name="profile"
    )

    def __str__(self):
        """return a format string representation"""
        return f"{self.user} {self.bio}"


class TrainingPlan(models.Model):
    """a training plan scehma to model the training"""

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField(default=30)
    creater = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        """return a format string representation"""
        return f"{self.name}  {self.creater}"


class Enrolment(models.Model):
    """enrolled the user to the training plan"""

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    training_plan = models.ForeignKey(to=TrainingPlan, on_delete=models.CASCADE)
    joining_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"user_Id: {self.user}"


class Invite(models.Model):
    """trainer inviting the person"""

    pending = 1
    accepted = 2
    declined = 3
    STATUS_CHOICES = (
        (pending, "pending"),
        (accepted, "accepted"),
        (declined, "declined"),
    )
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES, default=1, blank=True, null=True
    )
    email = models.EmailField(max_length=100)
    invite_date = models.DateTimeField(auto_now=True)
    training_id = models.ForeignKey(
        to=TrainingPlan, on_delete=models.CASCADE, related_name="invite"
    )
    inviter = models.ForeignKey(to=User, on_delete=models.CASCADE)
    invitee = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="invitee", null=True, blank=True
    )

    class Meta:
        """meta attribute for the invite"""

        unique_together = [("training_id", "email"), ("training_id", "invitee")]

    def __str__(self):
        """return a formated string"""
        return f"{self.invitee} {self.training_id.name}"


class Module(models.Model):
    """table to map module for course"""

    name = models.CharField(max_length=200)
    descrption = models.CharField(max_length=500)
    attactment_link = models.URLField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now=True)
    training_plan = models.ForeignKey(
        to=TrainingPlan, on_delete=models.CASCADE, related_name="modules"
    )

    class Meta:
        """meta attribute for the invite"""

        ordering = [
            "create_date",
        ]

    def __str__(self):
        """return a formated string"""
        return f"{self.name} {self.training_plan.name}"


class ModuleCompletion(models.Model):
    """to return wheather a user completed a module or not"""

    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    module = models.OneToOneField(
        to=Module,
        on_delete=models.CASCADE,
        related_name="module_complete",
    )
    completion_date = models.DateTimeField(auto_now=True)


class Task(models.Model):
    """a table that represent the tasks"""

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1500)
    attactment_link = models.URLField(null=True, blank=True)
    module = models.ForeignKey(to=Module, on_delete=models.CASCADE, related_name="task")
    create_date = models.DateTimeField(auto_now=True)
    file = models.FileField(
        null=True,
        blank=True,
    )


class TaskCompletion(models.Model):
    """to return wheather a user completed a module or not"""

    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    task = models.OneToOneField(
        to=Task,
        on_delete=models.CASCADE,
        related_name="task_complete",
    )
    completion_date = models.DateTimeField(auto_now=True)


class Feedback(models.Model):
    """trainer and trainee can share feedback"""

    message = models.CharField(max_length=400)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    task = models.ForeignKey(to=Task, on_delete=models.CASCADE, related_name="feedback")

    class Meta:
        """meta attribute for the invite"""

        ordering = [
            "-date",
        ]
