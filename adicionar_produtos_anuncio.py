import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from portfolio.models import Projeto

novos_projetos = [
    {
        'titulo': 'ZapConfirm — Automação & Confirmações via WhatsApp',
        'slug': 'zapconfirm',
        'categoria': 'automacao',
        'tipo': 'pessoal',
        'descricao_curta': 'Plataforma inteligente para automação de confirmações de agendamentos, lembretes e redução drástica de no-show via WhatsApp.',
        'descricao_completa': 'O ZapConfirm é uma solução SaaS completa projetada para reduzir o absenteísmo (no-show) em consultas e serviços. A plataforma conecta agendas com a API do WhatsApp para disparar lembretes automáticos, confirmações interativas com 1-clique, relatórios de conversão e integração com sistemas de pagamento.',
        'tecnologias': 'Python,Django,WhatsApp API,Redis,Celery,MySQL,WebSockets',
        'link_demo': 'https://makisjeanty.com/portfolio/zapconfirm/',
        'link_github': 'https://github.com/makisjeanty/makis',
        'destaque': True,
        'publico': True,
    },
    {
        'titulo': 'RenuSilencieux — Plataforma Digital & Design de Alta Performance',
        'slug': 'renusilencieux',
        'categoria': 'web',
        'tipo': 'pessoal',
        'descricao_curta': 'Plataforma web minimalista de alta performance desenvolvida com foco em experiência de usuário sofisticada e SEO de alta conversão.',
        'descricao_completa': 'O RenuSilencieux é um empreendimento focado em soluções sofisticadas e produtos digitais. Construído com arquitetura moderna, design refinado e otimização extrema para motores de busca (SEO Specialist), unindo estética elegante e eficiência técnica.',
        'tecnologias': 'Python,Django,JavaScript,TailwindCSS,Docker,Cloudflare',
        'link_demo': 'https://makisjeanty.com/portfolio/renusilencieux/',
        'link_github': 'https://github.com/makisjeanty/makis',
        'destaque': True,
        'publico': True,
    }
]

for item in novos_projetos:
    proj, created = Projeto.objects.update_or_create(
        slug=item['slug'],
        defaults=item
    )
    status_str = "Criado" if created else "Atualizado"
    print(f"✅ Anúncio de Produto: {proj.titulo} ({status_str})")

print("\n🚀 ZapConfirm e RenuSilencieux anunciados com sucesso!")
