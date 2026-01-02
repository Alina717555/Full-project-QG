from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        widget=forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
        label='Add Your Rating*'
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': 'Write here...'}),
        }