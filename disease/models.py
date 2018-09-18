from django.db import models

# Create your models here.

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
        The submitted likes [1,2,3] and the values with symptoms 'id
        """
        this_disease_symtoms = list(map(lambda x: x.id, self.main_symptoms.all()))

        matched = list(set(submitted) & set(this_disease_symtoms))
        # print logs
        print(this_disease_symtoms, submitted, matched)

        return len(matched) / len(this_disease_symtoms)


class DiseaseType(models.Model):
    """Model definition for DiseaseType."""

    class Meta:
        """Meta definition for DiseaseType."""

        verbose_name = '疾病分型'
        verbose_name_plural = '疾病分型'

    def __str__(self):
        """Unicode representation of DiseaseType."""
        return str(self.disease) + '/' + self.type_name

    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, verbose_name='疾病')
    type_name = models.CharField(verbose_name='分型名称', max_length=50)
    type_symptoms = models.CharField(verbose_name='分型症状', max_length=200)
    add_prescription = models.ManyToManyField(Prescription, verbose_name='处方加减')
