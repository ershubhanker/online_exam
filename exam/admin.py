from django.contrib import admin
from .models import Question,Course,EmotionalIntelligenceQuestion,DecisionMakingQuestion
# Register your models here.

admin.site.register(Question)
admin.site.register(Course)
admin.site.register(DecisionMakingQuestion)
admin.site.register(EmotionalIntelligenceQuestion)