from flask_restx import Namespace, Resource
from backend.app.services.facade2 import PortfolioFacade

facade = PortfolioFacade()

api = Namespace("descriptions", description="Gestion des descriptions")


@api.route("/<string:entity_type>/<int:entity_id>")
class DescriptionList(Resource):
    def get(self, entity_type, entity_id):
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
