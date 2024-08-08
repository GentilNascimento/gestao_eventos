Lucas
NÃO FIZ COMMIT DESSE README; COLEI DIRETO AQUI.

1-(no ambiente virtual)
pip install celery django-celery-beat


2-(Criar o Arquivo celery.py)
# gestao_eventos/app/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Define o módulo de configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

# Cria a instância do Celery
app = Celery('gestao_eventos')

# Carrega as configurações do Celery do Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carrega tarefas de todos os aplicativos registrados
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task():
    print('Request: {0!r}'.format(self.request))


3-(Configurar o settings.py)
# gestao_eventos/app/settings.py

# Configuração do Celery
CELERY_BROKER_URL = 'amqp://localhost'  # URL do RabbitMQ
CELERY_RESULT_BACKEND = 'django-db'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

INSTALLED_APPS = [
    'django_celery_beat',
]

4-(arquivo __init__.py, da pasta app)
# gestao_eventos/app/__init__.py

from __future__ import absolute_import, unicode_literals

from .celery import app as celery_app

__all__ = ('celery_app',)


5-(API e as Tarefas), em Artistas.
# gestao_eventos/artistas/api.py

from rest_framework import viewsets
from rest_framework.response import Response
from django_celery_beat.models import PeriodicTask
from celery.schedules import crontab
from .models import Artista
from .serializers import ArtistaSerializer
from .tasks import send_message
import json

class ArtistaViewSet(viewsets.ViewSet):
    def create(self, request):
        # Lógica para criar artista
        serializer = ArtistaSerializer(data=request.data)
        if serializer.is_valid():
            artista = serializer.save()
            # Agendar uma mensagem (exemplo)
            schedule_message(artista)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

def schedule_message(artista):
    # Criação de uma tarefa periódica
    PeriodicTask.objects.create(
        name=f'Envio de mensagem para {artista.nome}',
        task='artistas.tasks.send_message',
        schedule=crontab(minute='0', hour='0'),   # Ajuste conforme necessário
        args=json.dumps([artista.id]),
    )


#(Criar as Tarefas), Artistas.
 # gestao_eventos/artistas/tasks.py

from celery import shared_task
from datetime import datetime
from .models import Mensagem, Artista

@shared_task
def send_message(artista_id):
    try:
        artista = Artista.objects.get(id=artista_id)
        mensagens = Mensagem.objects.filter(artista=artista, agendada_para__lte=datetime.now())
        for mensagem in mensagens:
            # Lógica para enviar a mensagem via WhatsApp
            print(f"Enviando mensagem para {artista.nome}: {mensagem.conteudo}")
            mensagem.enviada = True
            mensagem.save()
    except Artista.DoesNotExist:
        print(f"Artista com ID {artista_id} não encontrado.")

@shared_task
def periodic_message_check():
    mensagens = Mensagem.objects.filter(agendada_para__lte=datetime.now(), enviada=False)
    for mensagem in mensagens:
        # Lógica para enviar a mensagem via WhatsApp
        print(f"Enviando mensagem: {mensagem.conteudo}")
        mensagem.enviada = True
        mensagem.save()



6-#(urls.py da sua aplicação artistas), conferir.
# gestao_eventos/artistas/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import ArtistaViewSet

router = DefaultRouter()
router.register(r'artistas', ArtistaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

7-#(criar serializers.py na pasta artistas)
# gestao_eventos/artistas/serializers.py

from rest_framework import serializers
from .models import Artista

class ArtistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artista
        fields = ['id', 'nome', 'celular']



8-#(Iniciar o Celery e depois o Beat)
celery -A app worker --loglevel=info
celery -A app beat --loglevel=info


#(DAQUI PRA FRENTE RODA O PROJETO)
-Antes de rodar, acessa o RabbitMQ, como no vídeo que vc me mandou, pra( pegar a URL do
RabbitMQ),  e add no 'settings.py'. Tenta fazer os testes junto com ele

