"""
Ce module initialise une instance unique (singleton) de la façade `PortfolioFacade`.

La façade centralise l'accès aux services métiers de l'application,
afin de simplifier l'interaction avec les repositories, modèles et autres services.

Exemple d'utilisation :
    from backend.app.facade_instance import facade
    users = facade.user_service.get_all_users()
"""
from backend.app.services.facade import PortfolioFacade

facade = PortfolioFacade()

# 🔹 Pourquoi un singleton ?
# Cette instance sera utilisée partout dans l'application pour garantir qu'il
# n'existe qu'une seule façade, évitant ainsi :
# - la création multiple de connexions ou sessions inutiles,
# - la duplication des services ou de la logique métier,
# - et facilitant la maintenance et la cohérence des données.
