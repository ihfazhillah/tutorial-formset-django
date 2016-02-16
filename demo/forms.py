from django import forms

class KelasForm(forms.Form):
    nama = forms.CharField(max_length=100)

class MuridForm(forms.Form):
    namadepan = forms.CharField(max_length=100)
    namabelakang = forms.CharField(max_length=100)

class BaseMuridFormSet(forms.formsets.BaseFormSet):


    def clean(self):
        
        if any(self.errors):
            return

        namadepans = []
        namabelakangs = []
        duplikat = False

        for form in self.forms:
            if form.cleaned_data:
                namadepan = form.cleaned_data['namadepan']
                namabelakang = form.cleaned_data['namabelakang']

                if namadepan:
                    if namadepan in namadepans:
                        duplikat = True
                    namadepans.append(namadepan) #ingat, namadepan untuk satu objek, 
                                                                             # namadepans untuk list
                    if namabelakang in namabelakangs:
                        duplikat = True
                    namabelakangs.append(namabelakang)

                if duplikat:
                    raise forms.ValidationError("Nama depan atau belakang terduplikasi",
                                                code="duplikat")

MuridFormSet = forms.formset_factory(MuridForm, 
                                     formset  = BaseMuridFormSet)