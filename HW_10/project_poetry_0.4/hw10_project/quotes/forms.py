from django import forms

from .models import Quote, Author, Tag

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['quote', 'author', 'tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].widget.attrs['size'] = 5  # Розмір вікна для вибору автора
        self.fields['tags'].widget.attrs['size'] = 10  # Розмір вікна для вибору тега

    def clean(self):
        cleaned_data = super().clean()
        author_name = cleaned_data.get("author")
        tags = cleaned_data.get("tags")
        quote = cleaned_data.get("quote")
        
        # Перевірка наявності автора в базі даних
        if not Author.objects.filter(fullname=author_name).exists():
            raise forms.ValidationError("Введений автор не існує")

        # Перевірка наявності тексту цитати
        if not quote:
            raise forms.ValidationError("Введіть текст цитати")
        
        return cleaned_data
