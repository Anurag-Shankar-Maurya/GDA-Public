from modeltranslation.translator import register, TranslationOptions
from .models import Project, NewsEvent, SuccessStory, FAQ

@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = ('title', 'teaser', 'background_objectives', 'tasks_eligibility', 'country', 'theme')

@register(NewsEvent)
class NewsEventTranslationOptions(TranslationOptions):
    fields = ('title', 'body')

@register(SuccessStory)
class SuccessStoryTranslationOptions(TranslationOptions):
    fields = ('title', 'body')

@register(FAQ)
class FAQTranslationOptions(TranslationOptions):
    fields = ('question', 'answer')
