import datetime 

from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.question_text    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
    def get_total_votes(self):
        """Retourne le nombre total de votes pour cette question"""
        return sum(choice.votes for choice in self.choice_set.all())


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text