from django import forms

from apps.shop.models import Review

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(required=False)
    text = forms.CharField(
        max_length=200,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": "5", "placeholder": "Enter your review"}),
    )

    class Meta:
        model = Review
        fields = ["rating", "text"]