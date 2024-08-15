from django.db import models
from django.utils import timezone
from user.models import CustomUser

class Proje(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='owned_projects', verbose_name="Projeyi Oluşturan")
    users = models.ManyToManyField(CustomUser, verbose_name="Üyeler", related_name='membership')
    content = models.TextField(max_length=8200, verbose_name="İçerik")
    title = models.CharField(max_length=50, verbose_name="Başlık")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Başlangıç Tarihi")
    ended_date = models.DateTimeField(blank=True, null=True, verbose_name="Bitiş Tarihi")


    def update_project_due_date(self):
        latest_due_date = self.tasks.aggregate(models.Max('due_date'))['due_date__max']
        if latest_due_date:
            self.ended_date = latest_due_date
            self.save()

    def save_without_update(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_project_due_date()
        self.save_without_update(*args, **kwargs)

    def __str__(self):
        return self.title
    

class Task(models.Model):
    STATUS_CHOICES = [
        ('Tamamlancak', 'Tamamlancak'),
        ('Devam Ediyor', 'Devam Ediyor'),
        ('Tamamlandı', 'Tamamlandı'),
        ('Gecikti', 'Gecikti'),
    ]
    proje = models.ForeignKey(Proje, on_delete=models.CASCADE, related_name='tasks', verbose_name="Bağlı Olduğu Proje")
    description = models.TextField(default='Açıklama Giriniz')
    assignee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null = True, blank = True, related_name='assigned_tasks', verbose_name="Atanan Kişi")
    start_date = models.DateTimeField(verbose_name="Başlangıç Tarihi", default=timezone.now)
    due_date = models.DateTimeField(verbose_name="Bitiş Tarihi", default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Tamamlanacak', verbose_name="Görev Durumu")

    def update_status(self, submittask=None):
        current_datetime = timezone.now()

        if self.start_date > current_datetime:
            self.status = 'Tamamlancak'
        elif self.start_date <= current_datetime and self.due_date >= current_datetime:
            self.status = 'Devam Ediyor'
        elif self.due_date < current_datetime:
            self.status = 'Gecikti'
        else:
            self.status = 'Tamamlandı'

        if submittask is not None:
            self.status = 'Tamamlandı'

        self.save()

    def __str__(self):
        return f"{self.proje.title} - {self.description}"

