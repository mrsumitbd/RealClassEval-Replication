from django.core.management.base import BaseCommand, CommandError
from django_tenants.utils import get_tenant_model, get_public_schema_name, get_tenant_domain_model

class InteractiveTenantOption:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument('-s', '--schema', '--schema_name', dest='schema_name', help='specify tenant schema')

    def get_tenant_from_options_or_interactive(self, **options):
        TenantModel = get_tenant_model()
        all_tenants = TenantModel.objects.all()
        if not all_tenants:
            raise CommandError('There are no tenants in the system.\nTo learn how create a tenant, see:\nhttps://django-tenants.readthedocs.org/en/latest/use.html#creating-a-tenant')
        if options.get('schema_name'):
            tenant_schema = options['schema_name']
        else:
            while True:
                tenant_schema = input("Enter Tenant Schema ('?' to list schemas): ")
                if tenant_schema == '?':
                    print('\n'.join([f'{i}) {t.schema_name} - {t.get_primary_domain()}' for i, t in enumerate(all_tenants)]))
                else:
                    break
        try:
            selected_tenant = all_tenants[int(tenant_schema)]
            self.stdout.write(self.style.SUCCESS(f'Selected Tenant: {selected_tenant.schema_name}'))
            return selected_tenant
        except (ValueError, IndexError):
            pass
        if tenant_schema not in [t.schema_name for t in all_tenants]:
            raise CommandError(f"Invalid tenant schema, '{tenant_schema}'")
        return TenantModel.objects.get(schema_name=tenant_schema)