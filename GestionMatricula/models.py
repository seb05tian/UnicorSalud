from django.db import models
from django.contrib.auth.models import AbstractUser

# Usuario personalizado con roles
class usuarios(AbstractUser):
    ROL_CHOICES = [
        ('estudiante', 'Estudiante'),
        ('docente', 'Docente'),
        ('admin', 'Administrador'),
    ]
    identificacion = models.CharField(max_length=20, unique=True)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)
    programa = models.ForeignKey('Programa', on_delete=models.CASCADE, null=True, blank=True)
    nivel = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"


class Programa(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']
        verbose_name = "Programa"
        verbose_name_plural = "Programas"


class Asignatura(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True, null=True)
    nivel = models.PositiveIntegerField()

    docentes = models.ManyToManyField(
        'usuarios',
        through='AsignaturaDocente',
        limit_choices_to={'rol': 'docente'}
    )

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    class Meta:
        ordering = ['codigo']
        verbose_name = "Asignatura"
        verbose_name_plural = "Asignaturas"


class AsignaturaDocente(models.Model):
    docente = models.ForeignKey(
        'usuarios',
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'docente'}
    )
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.docente.get_full_name()} - {self.asignatura.nombre}"

    class Meta:
        unique_together = ('docente', 'asignatura')
        verbose_name = "Asignatura Docente"
        verbose_name_plural = "Asignaturas Docentes"


class Prerrequisito(models.Model):
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE, related_name='asignatura_principal')
    prerequisito = models.ForeignKey(Asignatura, on_delete=models.CASCADE, related_name='asignatura_requerida')

    def __str__(self):
        return f"{self.asignatura.codigo} requiere {self.prerequisito.codigo}"

    class Meta:
        unique_together = ('asignatura', 'prerequisito')
        verbose_name = "Prerequisito"
        verbose_name_plural = "Prerequisitos"


class AsignaturaAprobada(models.Model):
    estudiante = models.ForeignKey('usuarios', on_delete=models.CASCADE, limit_choices_to={'rol': 'estudiante'})
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    fecha_aprobacion = models.DateField()

    def __str__(self):
        return f"{self.estudiante.get_full_name()} aprobó {self.asignatura.nombre}"

    class Meta:
        unique_together = ('estudiante', 'asignatura')
        verbose_name = "Asignatura Aprobada"
        verbose_name_plural = "Asignaturas Aprobadas"


class Matricula(models.Model):
    estudiante = models.ForeignKey('usuarios', on_delete=models.CASCADE, limit_choices_to={'rol': 'estudiante'})
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    fecha_matricula = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.estudiante.get_full_name()} matriculado en {self.asignatura.nombre}"

    class Meta:
        unique_together = ('estudiante', 'asignatura')
        verbose_name = "Matrícula"
        verbose_name_plural = "Matrículas"


class Reporte(models.Model):
    estudiante = models.ForeignKey('usuarios', on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_generacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reporte de {self.estudiante.get_full_name()} - {self.fecha_generacion.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-fecha_generacion']
        verbose_name = "Reporte"
        verbose_name_plural = "Reportes"
