from django import template

register = template.Library()

@register.filter
def int_to_word(value):
    mapping = {
        5: "FIVE",
        4: "FOUR",
        3: "THREE",
        2: "TWO",
        1: "ONE",
    }
    try:
        return mapping[int(value)]
    except (ValueError, KeyError, TypeError):
        return value

@register.filter
def dict_get(dict_obj, key):
    if not dict_obj:
        return 0
    try:
        return dict_obj.get(str(key)) or dict_obj.get(int(key), 0)
    except (ValueError, TypeError):
        return 0

@register.filter
def count_by_rating(reviews, rating):
    """Counts how many reviews have a specific rating"""
    return reviews.filter(rating=int(rating)).count()

@register.filter
def percent_by_rating(reviews, rating):
    """Calculates the percentage of reviews for a specific rating"""
    total = reviews.count()
    if total == 0:
        return 0
    count = reviews.filter(rating=int(rating)).count()
    return (count / total) * 100