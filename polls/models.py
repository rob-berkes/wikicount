from django.db import models
import datetime
class Poll(models.Model):
	question = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	def __unicode__(self):
		return self.question
	def was_published_today(self):
		return self.pub_date.date() == datetime.date.today()
class Choice(models.Model):
	poll = models.ForeignKey(Poll)
	choice = models.CharField(max_length=200)
	votes = models.IntegerField()
	def __unicode__(self):
		return self.choice

class hits(models.Model):
	Hits = models.IntegerField()
	id = models.CharField(max_length=80,primary_key=True)
	class Meta:
		db_table='hits'
class topictext(models.Model):
	text = models.CharField(max_length=300)
	id = models.CharField(max_length=100, primary_key=True)
	class Meta:
		db_table='topictext'

class prodtop(models.Model):
	m = models.IntegerField()
	d = models.IntegerField()
	y = models.IntegerField()
	Hits = models.IntegerField()
	place = models.IntegerField()
	id = models.CharField(max_length=300, primary_key=True)
	class Meta:
		db_table='prodtop'
