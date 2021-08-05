from django.db import models
from django.utils import timezone
from django.urls import reverse
# Create your models here.

#CREEZ UN POST -> UN BLOG POST AR TREBUI SA FIE CONECTAT CU UN MODEL DIN BD
class Post(models.Model):
    #trebuie sa punem fields(atribute)
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    #ASTEPTAM CA O PERSOANA SA VINA PE BLOG SI SA AIBA PUTERE , ADICA UPDATE, DRAFTS, COMMENTS, SA LE EDITEZE
    #DIRECT LINK AUTHOR LA UN auth.User
    #CAND CREEZ UN SUPERUSER - SA FIE CINEVA CARE POATE ADAUGA TEXTE NOI

    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now) #DE ASTA AM IMPORTAT SUS
    published_date = models.DateTimeField(blank=True,null=True)

    #CREAM NISTE METODE
    def publish(self):
        self.published_date = timezone.now()
        self.save()
        #CAND APAS PE BUTONUL PUBLISH VA CONTINE DATA/ORA CAND S-A APASAT PE BUTON SI DUPA SALVAM


    #DUPA CE UN USER CREEAZA UN POST SAU DA UN COMMENT UNDE SA FIE REDIRECTIONAT??
    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk})
        #DUPA CE CREEZ UN POST SI I DAU SUBMIT -> MERGEM LA POSTUL UNDE AM COMENTAT CU PK-UL CORESPUNZATOR

    #UN POST POATE AVEA SI COMMENTS
    def approve_comments(self):
        return self.comments.filter(approved_comment=True)
        #O SA O AM LISTA DE COMENTARII - UNELE VOR FI APROBATE ALTELE NU
        #LE IAU , LE FILTREZ SI LE AFISEZ CU POSTUL


    #PT FIECARE MODEL E OK SA AVEM O REPREZENTARE STRING PENTRU EL
    def __str__(self):
        return self.title



class Comment(models.Model):
    post = models.ForeignKey('blog.Post',related_name='comments',on_delete=models.CASCADE)
    #PRACTIC LINIA DE MAI SUS VA CONECTA FIECARE COMM LA POSTUL RESPECTIV
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now())
    approved_comment = models.BooleanField(default=False)
    #approved_comment de aici trebuie sa fie scris la fel cu cel din functia approve_comments()

    def approve(self):
        self.approved_comment = True
        self.save()

    #DUPA CE UN USER CREEAZA UN POST SAU DA UN COMMENT UNDE SA FIE REDIRECTIONAT??
    def get_absolute_url(self):
        return reserve('post_list')
        #HOMEPAGE VA FI POSTLIST UNDE VEDEM TOATE POSTURILE
        #DE CE SA RET USERUL DUPA CE POSTEAZA UN COM PE HOMEPAGE?
        #FIINDCA COMMENTARIUL LUI TRB SA FIE APROBAT DE UN SUPERUSER

    def __str__(self):
        return self.text
