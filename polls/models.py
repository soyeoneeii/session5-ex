from django.db import models

class Poll(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    agree = models.IntegerField(default=0)
    disagree = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def agree_rate(self):
        try:
            return self.agree / (self.agree + self.disagree)
        except ZeroDivisionError:
            return 0.0
    
    @property
    def disagree_rate(self):
        try:
            return self.disagree / (self.agree + self.disagree)
        except ZeroDivisionError:
            return 0.0
        
    def raise_agree(self):
        if not self.pk: return
        self.agree += 1
        self.save()

    def raise_disagree(self):
        if not self.pk: return
        self.disagree += 1
        self.save()

    def update(self, **kwargs):
        if not self.pk: return
        self.title, self.description = kwargs.get('title', ''), kwargs.get('description', '')
