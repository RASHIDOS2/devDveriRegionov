import requests
from django.conf import settings
from .models import ExchangeNode
from requests.exceptions import HTTPError
from .serializers import ExchangeNodeSerializer
from rest_framework.renderers import JSONRenderer
from celery import shared_task


@shared_task
def upload_orders():
    print('upload_orders')
    try:
        for order in ExchangeNode.objects.all():
            serializer = ExchangeNodeSerializer(order)
            json = JSONRenderer().render(serializer.data)
            response = requests.post(settings.HTTP_SERVICE,
                                     headers={'Content-Type': 'application/json'},
                                     auth=(settings.HTTP_USER, settings.HTTP_PASSWORD),
                                     data=json)
            if response.status_code == 200:
                order.delete()
    except HTTPError as err:
        print(f'HTTP error: {err}')
    except Exception as err:
        print(err)
    else:
        print('OK')

    return True
