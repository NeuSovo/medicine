import random
from django.db import models
from user.models import User

# Create your models here.


class NeiJingRaw(models.Model):
    """Model definition for NeiJingRaw."""

    class Meta:
        """Meta definition for NeiJingRaw."""

        verbose_name = '内经原文'
        verbose_name_plural = '内经原文'

    def __str__(self):
        """Unicode representation of NeiJingRaw."""
        return self.title

    title = models.CharField(verbose_name="文章标题", max_length=225)
    raw = models.TextField(verbose_name="原文")
    blank_count = models.IntegerField(verbose_name="设置几个填空", default=10)

    def get_all_blank_count(self):
        count = 0
        blanks = []
        all_answers = []
        paragraph = self.paragraph.all()
        for val in paragraph:
            count += len(val.blanks)
            for j in val.blanks:
                all_answers.append(eval(val.content)[j-1])
                blanks.append(str(val.id)+'-'+str(j-1))
        if self.blank_count > count:
            count = count
        else:
            count = self.blank_count
        blanks = sorted(random.sample(blanks, count),
                        key=lambda x: int(x.split('-')[0]))
        exam_b = NeiJingRaw.get_exam_b(paragraph, blanks, all_answers)
        return exam_b, blanks

    @staticmethod
    def get_exam_b(paragraphs, blanks, all_answers):
        exam_b = []

        def get_options(val):
            count = 3
            res = []
            if count > len(all_answers):
                count = len(all_answers) - 1
            while count:
                a = random.choice(all_answers)
                if a != val and a not in res:
                    res.append(a)
                    count -= 1
            res.append(val)
            random.shuffle(res)
            return res
        for i in paragraphs:
            content = []
            for idx, val in enumerate(eval(i.content)):
                if str(i.id)+'-'+str(idx) in blanks:
                    content.append({
                        'text': '____',
                        'is_blank': True,
                        'options': get_options(val),
                        'answer': val
                    })
                else:
                    content.append({
                        'text': val,
                        'is_blank': False
                    })
            exam_b.append(content)
        return exam_b


class NeiJingParaGraph(models.Model):
    class Meta:
        verbose_name = '段落'
        verbose_name_plural = '段落'

    raw = models.ForeignKey(
        NeiJingRaw, on_delete=models.CASCADE, related_name='paragraph')
    content = models.TextField(
        verbose_name='内容', help_text='点击标记或取消标记，红色为填空内容')
    blank_index = models.CharField(max_length=255, default='')

    @property
    def as_list(self):
        return [{'content': val, 'match': idx+1 in self.blanks} for idx, val in enumerate(eval(self.content))]

    @property
    def blanks(self):
        return sorted([
            int(i) for i in self.blank_index.split(',') if i != ''
        ])


class NeiJingExam(models.Model):
    class Meta:
        verbose_name = '测试'
        verbose_name_plural = '测试'
        ordering = ['-id']

    begin_time = models.DateTimeField(
        verbose_name='开始时间', auto_now=False, auto_now_add=True)
    create_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    exam_raw = models.ForeignKey(NeiJingRaw, on_delete=models.CASCADE)
    blanks = models.CharField(max_length=250, default='')
    right_answer_count = models.IntegerField(default=0)
    u_answers = models.CharField(max_length=250, default='')

    def get_res(self):
        u_answers = eval(str(self.u_answers))
        blanks = eval(self.blanks)
        # blank
        count = 0
        right_answer_count = 0
        res = []
        for i in self.exam_raw.paragraph.all():
            content = []
            for idx, val in enumerate(eval(i.content)):
                if str(i.id)+'-'+str(idx) in blanks:
                    content.append({
                        'text': '____',
                        'is_blank': True,
                        'answer': val,
                        'u_answer': u_answers[count],
                        'is_right': val == u_answers[count]
                    })
                    if val == u_answers[count]:
                        right_answer_count += 1
                    count += 1
                else:
                    content.append({
                        'text': val,
                        'is_blank': False
                    })
            res.append(content)
        self.right_answer_count = right_answer_count
        self.save()
        return res
