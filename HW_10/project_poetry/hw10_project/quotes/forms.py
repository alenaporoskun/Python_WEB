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
        #author_name = cleaned_data.get("author")
        author_name = cleaned_data.get("new_author")
        tags = cleaned_data.get("tags")
        quote = cleaned_data.get("quote")

        if author_name:
            # Якщо введено нове ім'я автора, створіть нового автора
            author, created = Author.objects.get_or_create(fullname=author_name)
            cleaned_data['author'] = author
        else:
            # Якщо автор вибраний з існуючих, використовуйте його
            author_name = cleaned_data.get("author")
            if not Author.objects.filter(fullname=author_name).exists():
                raise forms.ValidationError("The entered author does not exist.")

        # Перевірка наявності тексту цитати
        if not quote:
            raise forms.ValidationError("Enter the text of the quote.")
        
        return cleaned_data

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']