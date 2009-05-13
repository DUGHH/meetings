from pyamf.remoting.gateway.django import DjangoGateway
from models import Content
import pyamf
from pyamf.flex import ArrayCollection, ObjectProxy

pyamf.register_class (Content, 'django_amf.flexremoting.Content')

def echo(data):
    return data

def getContents():
    all = Content.objects.all()
    return ArrayCollection(all)

def update(content):
    if content.contentId == 0:
        content.contentId = None
    content.save();
    return content

def delete(content):
    content.delete()

services = {
    'myservice.echo': echo,
    'content.getContents': getContents,
    'content.update': update,
    'content.deleteContent': delete,
}

echoGateway = DjangoGateway(services, expose_request=False)

