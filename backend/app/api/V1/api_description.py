"""
Module de gestion des descriptions liées à leur entité.

Ce module contient les endpoints REST permettant de consulter les différents 
descriptions. Il s'agit d'endpoints en lecture seule (GET uniquement).
"""

from flask_restx import Namespace, Resource
from backend.app.services.facade2 import PortfolioFacade

facade = PortfolioFacade()

api = Namespace("descriptions", description="Gestion des descriptions")


@api.route("/<string:entity_type>/<int:entity_id>")
class DescriptionList(Resource):
    """Gestion des descriptions associées à une entité."""
    def get(self, entity_type, entity_id):
        """
        Récupère toutes les descriptions d'une entité spécifique

        Cette méthode permet d'obtenir la liste complète des descriptions associés
        à une entité identifié par son type et son ID

        Args: 
            entity_type (str): Type de l'entité. Valeurs acceptées: 
                'character', 'place', 'race', 'history', 'region', 'foret',
                'montagne', 'forteresse', 'ville', 'capitale', 'eau', 'ruine',
                'dark', 'mine', 'port', 'pont', 'plaine', 'chemin', 'monument',
                'special', 'default'            entity_id (int): Identifiant unique de l'entité
            entity_id (int): Identifiant unique de l'entité

        Returns:
            tuple: Un tuple contenant:
                - dict: Dictionnaire avec la structure:
                    {
                        "success": bool,
                        "data": list[dict] avec les champs:
                            - id: Identifiant de la description
                            - entity_type: Type de l'entité
                            - entity_id: ID de l'entité
                            - title: Titre de la description
                            - content: Contenu de la description
                            - order_index: Index d'ordre pour le tri
                            - created_at: Date de création (ISO format)
                    }
                - int: Code de statut HTTP (200 en cas de succès, 500 en cas d'erreur)
        Note:
            Les descriptions sont triées par order_index (si défini).
        """
        try:
            descriptions = facade.get_descriptions(entity_type, entity_id)
            return {
                "success": True,
                "data": [
                    {
                        "id": d.id,
                        "entity_type": d.entity_type,
                        "entity_id": d.entity_id,
                        "title": d.title,
                        "content": d.content,
                        "order_index": d.order_index,
                        "created_at": d.created_at.isoformat() if d.created_at else None
                    } for d in descriptions
                ]
            }, 200
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {"success": False, "error": str(e)}, 500
