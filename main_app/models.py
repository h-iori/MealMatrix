from django.db import models
from django.contrib.auth.models import User

class DietPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    age = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()
    diet_goal = models.CharField(max_length=50)
    diet_time_period = models.CharField(max_length=20)
    diet_plan_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.diet_goal}"

# Create your models here.
