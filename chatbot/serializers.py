from rest_framework.serializers import ModelSerializer
from chatbot.models import Conversacion

class ConversacionSerializer(ModelSerializer):
    class Meta:
        model = Conversacion
        fields = '__all__'
        extra_kwargs = {
            "fecha_creacion": {"read_only": True},
            "fecha_actualizacion": {"read_only": True},
            "usuario": {"read_only": True},
            "respuesta": {"read_only": True},
        }