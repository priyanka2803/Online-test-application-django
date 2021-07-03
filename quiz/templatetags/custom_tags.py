from django import template

register = template.Library()

@register.simple_tag
def getAnswer(answer):
    print("answer = ",answer)
    return 1

