from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from chatbot.models import Conversacion
from chatbot.serializers import ConversacionSerializer
from chatbot.rag import generar_respuesta
from inventario.models import Producto


class ChatbotView(APIView):
    serializer_class = ConversacionSerializer
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        engine = request.query_params.get('engine', "groq").lower()
        pregunta = serializer.validated_data["pregunta"].lower()

        productos = Producto.objects.all()
        contexto = "\n".join(
            [f"Producto: {p.nombre.lower()} | Descripcion: {p.descripcion.lower()} | Precio: {p.precio} | Cantidad: {p.cantidad} | Categoria: {p.categoria.nombre.lower()}" for p in productos])
        
        if not contexto:
            return Response({"error":"no hay contexto"})
            
        SYSTEM_PROMPT = (
            "Eres el asistente del sistema eCommerce llamado BodeGON. "
            "Usa solo la información provista en el 'CONTEXT' para responder "
            "consultas sobre productos, disponibilidad del stock y productos mas vendidos. "
            "Si no puedes responder con la información disponible, indica que no puedes responder."
        )
        
        # 🔧 CORRECCIÓN: Manejar historial SOLO si usuario está autenticado
        if request.user.is_authenticated:
            historial_usuario = Conversacion.objects.filter(usuario=request.user).order_by('-fecha_creacion')[:3]
            historial_plano = "".join([
                f"\nPregunta: {h.pregunta.lower()}\nUsuario: {h.respuesta.lower()}" for h in historial_usuario
            ])
        else:
            historial_plano = "Sin historial previo (usuario no autenticado).\n"
        
        prompt = (
            f"{SYSTEM_PROMPT}\n\n"
            f"=== CONTEXT ===\n{contexto}\n\n"
            f"=== HISTORIAL RELEVANTE ===\n"
            f"{historial_plano}\n"
            f"\n=== INSTRUCCIÓN ===\n"
            "\nResponde solo con información del contexto. Sé claro, conciso y emite la respuesta en texto plano.\n"
        )
        
        temperatura = serializer.validated_data.get("temperatura", 0.7)
        modelo = serializer.validated_data.get("modelo", "modelo_base")
        
        try:
            print("Prompt:", prompt)
            print("Haciendo petición con el modelo:", modelo)
            respuesta = generar_respuesta(
                prompt, pregunta, temperatura=temperatura, engine=engine)
            print("Respuesta:", respuesta)
            
            LISTA_ERROR = ["No puedo responder a esa pregunta.",
                           "No puedo responder a tu pregunta.", "No puedo responder a tu pregunta", ""]
            
            if respuesta and respuesta not in LISTA_ERROR:
                print("Guardando conversacion")
                # 🔧 CORRECCIÓN: Solo guardar si usuario está autenticado
                if request.user.is_authenticated:
                    Conversacion.objects.create(
                        pregunta=pregunta, 
                        respuesta=respuesta, 
                        usuario=request.user, 
                        temperatura=temperatura
                    )
                else:
                    print("Usuario anónimo - no se guarda conversación")
                
                return Response({"pregunta": pregunta, "respuesta": respuesta})
                
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        return Response({"pregunta": pregunta, "respuesta": respuesta})