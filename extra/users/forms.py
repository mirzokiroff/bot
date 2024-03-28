from django import forms

from .models import Contact_us


class Contact_usForm(forms.ModelForm):
    phone_numbers = forms.CharField(max_length=500, required=False, widget=forms.Textarea(attrs={'rows': 3}))
    telegram_admins = forms.CharField(max_length=500, required=False, widget=forms.Textarea(attrs={'rows': 3}))
    telegram_chanels = forms.CharField(max_length=500, required=False, widget=forms.Textarea(attrs={'rows': 3}))
    instagrams = forms.CharField(max_length=500, required=False, widget=forms.Textarea(attrs={'rows': 3}))
    you_tubes = forms.CharField(max_length=500, required=False, widget=forms.Textarea(attrs={'rows': 3}))
    emails = forms.CharField(max_length=500, required=False, widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = Contact_us
        fields = ('phone_number', 'telegram_admin', 'telegram_chanel', 'instagram', 'you_tube', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            if self.instance.phone_number:
                self.fields['phone_number'].initial = "\n".join(self.instance.phone_number.split(','))
            if self.instance.telegram_admin:
                self.fields['telegram_admin'].initial = "\n".join(self.instance.telegram_admin.split(','))
            if self.instance.telegram_chanel:
                self.fields['telegram_chanel'].initial = "\n".join(self.instance.telegram_chanel.split(','))
            if self.instance.instagram:
                self.fields['instagram'].initial = "\n".join(self.instance.instagram.split(','))
            if self.instance.you_tube:
                self.fields['you_tube'].initial = "\n".join(self.instance.you_tube.split(','))
            if self.instance.email:
                self.fields['email'].initial = "\n".join(self.instance.email.split(','))
