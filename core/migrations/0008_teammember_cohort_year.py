from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_teammember_profile_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="teammember",
            name="cohort_year",
            field=models.PositiveSmallIntegerField(
                blank=True,
                db_index=True,
                help_text="Ex: 2024, 2025, 2026. Permet de filtrer les participants par promotion.",
                null=True,
                verbose_name="Promotion (année)",
            ),
        ),
    ]
