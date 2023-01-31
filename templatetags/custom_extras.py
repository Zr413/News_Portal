# import datetime
#
# from django import template
#
# register = template.Library()
#
# forbidden_words = ['Wdfsdfsdfsdfsdf']
#
# @register.filter
# def hide_forbidden(value):
#     words = value.split()
#     result = []
#     for word in words:
#         if word in forbidden_words:
#             result.append(word[0] + "*"*(len(word)-2) + word[-1])
#         else:
#             result.append(word)
#     return " ".join(result)
#
# @register.simple_tag
# def current_time(format_string):
#     return datetime.datetime.now().strftime(format_string)