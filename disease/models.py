import random
import time

from django.db import models, transaction
from django.utils import timezone

try:
    random = random.SystemRandom()
    using_sysrandom = True
    from user.models import User
except NotImplementedError:
    using_sysrandom = False


class Symptoms(models.Model):
    """Model definition for Symptoms."""

    class Meta:
        """Meta definition for Symptoms."""

        verbose_name = '主症'
        verbose_name_plural = '主症'

    def __str__(self):
        """Unicode representation of Symptoms."""
        return self.symptoms

    # TODO: check logs and refresh weight

    symptoms = models.CharField(verbose_name="症状", max_length=50, unique=True)


class Prescription(models.Model):
    """Model definition for Prescription."""

    class Meta:
        """Meta definition for Prescription."""

        verbose_name = '主方'
        verbose_name_plural = '主方'

    def __str__(self):
        """Unicode representation of Prescription."""
        return self.prescription

    # TODO: prescription satisfaction

    prescription = models.CharField(verbose_name='药方', max_length=50, unique=True)


class Disease(models.Model):
    """Model definition for Disease."""

    class Meta:
        """Meta definition for Disease."""

        verbose_name = '疾病'
        verbose_name_plural = '疾病'

    def __str__(self):
        """Unicode representation of Disease."""
        return self.disease_name

    disease_name = models.CharField(verbose_name="疾病名称", max_length=50)
    main_symptoms = models.ManyToManyField(Symptoms, verbose_name='主要症状')
    main_prescription = models.ManyToManyField(Prescription, verbose_name='主药方', blank=True)

    def get_compatibility(self, submitted):
        """
        Calculate the match with this based on the submitted parameters
        The submitted likes [1,2,3] and the values with symptom 's id
        """
        this_disease_symtoms = list(map(lambda x: x.id, self.main_symptoms.all()))

        matched = list(set(submitted) & set(this_disease_symtoms))
        # print logs
        print(this_disease_symtoms, submitted, matched)

        return len(matched) / len(this_disease_symtoms)

class DiseaseTypingSymptoms(models.Model):

    class Meta:
        """分型的主要症状"""

        verbose_name = 'DiseaseTypingSymptoms'
        verbose_name_plural = 'DiseaseTypingSymptomss'

    def __str__(self):
        """Unicode representation of DiseaseTypingSymptoms."""
        return self.symptoms_name

    symptoms_name = models.CharField(verbose_name='分型症状名字', max_length=30)


class DiseaseTyping(models.Model):
    """Model definition for DiseaseTyping."""

    class Meta:
        """Meta definition for DiseaseTyping."""

        verbose_name = '疾病分型'
        verbose_name_plural = '疾病分型'

    def __str__(self):
        """Unicode representation of DiseaseTyping."""
        return str(self.disease) + '/' + self.type_name

    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, verbose_name='疾病')
    type_name = models.CharField(verbose_name='分型名称', max_length=50)
    add_prescription = models.ManyToManyField(Prescription, verbose_name='处方加减')
    typing_symptoms = models.ManyToManyField(DiseaseTypingSymptoms, verbose_name='分型症状', help_text='test', blank=True)


class Case(models.Model):
    """Model definition for Case."""

    class Meta:
        """Meta definition for Case."""

        verbose_name = 'Case'
        verbose_name_plural = 'Cases'

    def __str__(self):
        """Unicode representation of Case."""
        return str(self.case_id)

    def gen_case_id(self):
        return timezone.now().strftime("%Y%m%d") + str(round(time.time() * 1000)) [-4:] + \
                str(random.randint(1000,9999))

    def save(self, *args, **kwargs):
        if not self.case_id:
            self.case_id = self.gen_case_id()
        return super().save(*args, **kwargs)

    @staticmethod
    def create(create_user, case_disease, symptoms):
        try:
            with transaction.atomic():
                case = Case.objects.create(create_user=create_user, case_disease=case_disease)
                for i in symptoms:
                    case.casesymptoms_set.create(symptoms_id=i)
        except Exception as e:
            print (str(e) + ' line 130')
            return str(e)

        return case

    def create_typing(self, typings):
        try:
            with transaction.atomic():
                # for i in DiseaseTypingSymptoms.objects.filter(id__in=typings):
                #     # self.casetyping_set.create(typing=i)
                #     if self.casetyping_set.filter(i.)
                for i in self.case_disease.diseasetyping_set.all():
                    if i.typing_symptoms.filter(id__in=typings).exists():
                        self.casetyping_set.create(typing=i)
        except Exception as e:
            print(str(e) + ' line 142')
            return str(e)

    def get_result(self):
        info = dict()
        # 主方/
        info['main_prescription'] = [i.prescription for i in self.case_disease.main_prescription.all()]
        # 
        info['typings'] = [{'typing_name': i.typing.type_name, 'prescription': [j.prescription
                            for j in i.typing.add_prescription.all()]} for i in self.casetyping_set.all()]

        return info

    case_id = models.BigIntegerField(primary_key=True)
    create_user = models.ForeignKey(User, on_delete=models.CASCADE)

    case_disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)


class CaseSymptoms(models.Model):
    """Model definition for CaseSymptoms."""

    class Meta:
        """Meta definition for CaseSymptoms."""

        verbose_name = 'CaseSymptoms'
        verbose_name_plural = 'CaseSymptomss'
        unique_together = ('case', 'symptoms')

    def __str__(self):
        """Unicode representation of CaseSymptoms."""
        return str(self.case_id) + str(self.symptoms)

    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    symptoms = models.ForeignKey(Symptoms, on_delete=models.SET_NULL, null=True)


class CaseTyping(models.Model):
    """Model definition for CaseTyping."""

    class Meta:
        """Meta definition for CaseTyping."""

        verbose_name = 'CaseTyping'
        verbose_name_plural = 'CaseTypings'
        unique_together = ('case', 'typing')

    def __str__(self):
        return str(self.case_id) + str(self.typing)

    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    typing = models.ForeignKey(DiseaseTyping, on_delete=models.SET_NULL, null=True)


class FavList(models.Model):

    class Meta:
        verbose_name = "FavList"
        verbose_name_plural = "FavList"

    fa_case = models.ForeignKey(Case, on_delete=models.CASCADE)
    fa_user = models.ForeignKey(User, on_delete=models.CASCADE)
