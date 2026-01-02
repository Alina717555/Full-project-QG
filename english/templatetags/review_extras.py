from django import template

register = template.Library()

@register.filter
def filter_by_rating(reviews, rating):
    return reviews.filter(rating=rating)

@register.filter
def int_to_word(value):
    return {
        '5': 'FIVE',
        '4': 'FOUR',
        '3': 'THREE',
        '2': 'TWO',
        '1': 'ONE'
    }.get(str(value), value)
