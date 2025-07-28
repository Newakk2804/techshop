from django import forms
from reviews.models import Review


class ReviewForm(forms.Form):
    rating = forms.ChoiceField(
        choices=[(str(i), "") for i in range(5, 0, -1)],
        widget=forms.RadioSelect,
        label="",
    )
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "input", "placeholder": "Ваш комментарий", "rows": 4}
        ),
        label="",
    )

    def __init__(self, *args, user=None, product=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.product = product

    def clean(self):
        cleaned_data = super().clean()

        if self.user and self.product:
            if Review.objects.filter(user=self.user, product=self.product).exists():
                raise forms.ValidationError("Вы уже оставили отзыв для этого товара.")
            
        return cleaned_data

    def save(self, commit=True):
        review = Review(
            user=self.user,
            product=self.product,
            rating=int(self.cleaned_data["rating"]),
            comment=self.cleaned_data["comment"],
        )

        if commit:
            review.save()
        return review
