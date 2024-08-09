from rest_framework import renderers
import json

class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''

        # Vérifie si 'ErrorDetail' est présent dans les données
        if 'ErrorDetail' in str(data):
            # Si oui, structure la réponse avec un objet JSON contenant les erreurs
            response = json.dumps({'errors': data})
        else:
            # Sinon, convertit les données en JSON normalement
            response = json.dumps(data)
        
        return response
