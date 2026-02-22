from django.db import models

# Create your models here.
class interface_data(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, primary_key=True)
    goal = models.CharField(max_length=122,default='N/A')
    language = models.CharField(max_length=122,default='N/A')
    level_of_understanding = models.CharField(max_length=122,default="N/A")
    platform = models.CharField(max_length=122,default="N/A")
    content_type = models.CharField(max_length=122,default="N/A")
    content_stay_gfg = models.IntegerField(default=0)
    content_visit_gfg = models.IntegerField(default=0)
    content_stay_w3school = models.IntegerField(default=0)
    content_visit_w3school = models.IntegerField(default=0)
    video_play = models.IntegerField(default=0)
    video_visit = models.IntegerField(default=0)
    question_remember = models.IntegerField(default=0)
    question_understanding = models.IntegerField(default=0)
    question_application = models.IntegerField(default=0)
    question_analysis = models.IntegerField(default=0)
    question_evaluation = models.IntegerField(default=0)
    self_assess_stay =models.IntegerField(default=0)
    self_assess_visit =models.IntegerField(default=0)
    total_interactions = models.IntegerField(default=0)
    preference_gfg  = models.FloatField(default=0)
    preference_w3school = models.FloatField(default=0)
    preference_youtube = models.FloatField(default=0)


    def __str__(self):
        return self.goal
