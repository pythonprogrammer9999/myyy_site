from django import forms


class SearchForm(forms.Form):
    q = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Поиск'}
        )
    )


class ContactForm(forms.Form):
    first_name = forms.CharField(
        min_length=2,
        max_length=30,
        widget=forms.TextInput(
            attrs={'placeholder': 'Имя', 'class': 'form-control valid', 'style':'resize:none;'
    }
        )
    )
    second_name = forms.CharField(
        min_length=2,
        max_length=30,
        widget=forms.TextInput(
            attrs={'placeholder': 'Фамилия',
                   'class': 'form-control valid', 'style': 'resize:none;'

    }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'placeholder': 'E-mail',
                   'class': 'form-control valid', 'style': 'resize:none;'

    }
        )
    )
    message = forms.CharField(
        min_length=10,
        widget=forms.Textarea(
            attrs={'placeholder': 'Сообщение',
                   'class': 'form-control valid', 'rows':6, 'cols':100, 'style':'resize:none;'
                   }

        )
    )
