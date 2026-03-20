from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group


class Command(BaseCommand):
    help = 'Cria um usuário recepcionista com acesso restrito'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Nome de usuário do recepcionista')
        parser.add_argument('--password', type=str, help='Senha do usuário (será solicitada interativamente se não informada)')
        parser.add_argument('--email', type=str, default='', help='Email do recepcionista')

    def handle(self, *args, **options):
        username = options['username']
        password = options.get('password')
        email = options.get('email', '')

        # Criar ou obter o grupo Recepcionista
        recepcionista_group, created = Group.objects.get_or_create(name='Recepcionista')
        if created:
            self.stdout.write(self.style.SUCCESS(f'Grupo "Recepcionista" criado com sucesso!'))

        # Verificar se o usuário já existe
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user.groups.add(recepcionista_group)
            self.stdout.write(self.style.WARNING(f'Usuário "{username}" já existe. Adicionado ao grupo Recepcionista.'))
        else:
            # Criar o usuário
            if not password:
                from getpass import getpass
                password = getpass('Digite a senha: ')
                password_confirm = getpass('Confirme a senha: ')
                if password != password_confirm:
                    self.stdout.write(self.style.ERROR('As senhas não conferem!'))
                    return

            user = User.objects.create_user(
                username=username,
                password=password,
                email=email if email else None
            )
            user.groups.add(recepcionista_group)
            self.stdout.write(self.style.SUCCESS(f'Usuário "{username}" criado com sucesso como Recepcionista!'))

        self.stdout.write(self.style.SUCCESS('\nPermissões do Recepcionista:'))
        self.stdout.write('  - Pode acessar: Agendamentos, Clientes, Serviços, Profissionais')
        self.stdout.write('  - NÃO pode acessar: Relatórios, Usuários (apenas admin)')

