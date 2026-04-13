from django.core.management.base import BaseCommand
from vaccination_app.models import Vaccine


class Command(BaseCommand):
    help = 'Seed the database with standard childhood vaccines'

    def handle(self, *args, **kwargs):
        vaccines = [
            {
                'name': 'Hepatitis B Vaccine',
                'short_name': 'HepB',
                'description': 'Protects against Hepatitis B virus infection.',
                'recommended_age_months': 0,
                'doses_required': 3,
                'interval_days': 30,
                'manufacturer': 'Various',
                'is_mandatory': True,
            },
            {
                'name': 'BCG Vaccine',
                'short_name': 'BCG',
                'description': 'Bacillus Calmette-Guérin vaccine for tuberculosis.',
                'recommended_age_months': 0,
                'doses_required': 1,
                'interval_days': 0,
                'manufacturer': 'Various',
                'is_mandatory': True,
            },
            {
                'name': 'Oral Polio Vaccine',
                'short_name': 'OPV',
                'description': 'Protects against poliomyelitis.',
                'recommended_age_months': 2,
                'doses_required': 4,
                'interval_days': 28,
                'manufacturer': 'Various',
                'is_mandatory': True,
            },
            {
                'name': 'Pentavalent Vaccine',
                'short_name': 'Penta',
                'description': 'Combination vaccine: DPT + HepB + Hib.',
                'recommended_age_months': 6,
                'doses_required': 3,
                'interval_days': 28,
                'manufacturer': 'Various',
                'is_mandatory': True,
            },
            {
                'name': 'Measles, Mumps, Rubella Vaccine',
                'short_name': 'MMR',
                'description': 'Protects against measles, mumps and rubella.',
                'recommended_age_months': 9,
                'doses_required': 2,
                'interval_days': 28,
                'manufacturer': 'Various',
                'is_mandatory': True,
            },
            {
                'name': 'Inactivated Polio Vaccine',
                'short_name': 'IPV',
                'description': 'Injected polio vaccine.',
                'recommended_age_months': 14,
                'doses_required': 2,
                'interval_days': 60,
                'manufacturer': 'Various',
                'is_mandatory': True,
            },
            {
                'name': 'Typhoid Conjugate Vaccine',
                'short_name': 'TCV',
                'description': 'Protects against typhoid fever.',
                'recommended_age_months': 9,
                'doses_required': 1,
                'interval_days': 0,
                'manufacturer': 'Various',
                'is_mandatory': True,
            },
            {
                'name': 'Varicella Vaccine',
                'short_name': 'Varicella',
                'description': 'Protects against chickenpox.',
                'recommended_age_months': 12,
                'doses_required': 2,
                'interval_days': 90,
                'manufacturer': 'Various',
                'is_mandatory': False,
            },
            {
                'name': 'Hepatitis A Vaccine',
                'short_name': 'HepA',
                'description': 'Protects against Hepatitis A virus.',
                'recommended_age_months': 12,
                'doses_required': 2,
                'interval_days': 180,
                'manufacturer': 'Various',
                'is_mandatory': False,
            },
            {
                'name': 'Rotavirus Vaccine',
                'short_name': 'Rota',
                'description': 'Protects against rotavirus diarrhea.',
                'recommended_age_months': 2,
                'doses_required': 3,
                'interval_days': 28,
                'manufacturer': 'Various',
                'is_mandatory': True,
            },
        ]

        created = 0
        for v in vaccines:
            obj, was_created = Vaccine.objects.get_or_create(
                short_name=v['short_name'],
                defaults=v
            )
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f'  Created: {obj.name}'))
            else:
                self.stdout.write(f'  Already exists: {obj.name}')

        self.stdout.write(self.style.SUCCESS(f'\nDone! {created} new vaccines added.'))
