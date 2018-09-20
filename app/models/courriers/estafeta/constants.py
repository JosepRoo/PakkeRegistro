from app import Database
from app.common.dijkstra import GraphUndirectedWeighted

RATES_COLLECTION = 'Estafeta_rates'
TYPES_STR_TO_ID = {"ESTAFETA_DIA_SIGUIENTE": "8619166", "ESTAFETA_TERRESTRE_CONSUMO": "1377731"}
TYPES_ID_TO_STR = {"8619166": "ESTAFETA_DIA_SIGUIENTE", "1377731": "ESTAFETA_TERRESTRE_CONSUMO"}
TYPES = {"8619166",
         "8668532",
         "8622603",
         "4000613",
         "5056308",
         "5522411"
         }
SPECIAL_TYPE = "1377731"
# NON_OPTIMIZABLE_TYPES = {"8619166", "8646029", "8608731"}
# OPTIMIZABLE_TYPES = {"8668532", "8622603", "4000613", "5056308", "5522411"}
EXTRA_FEE = 25.0
TYPE_KG_LIMIT = 20


def create_graph() -> GraphUndirectedWeighted:
    rates = list(
        Database.find("Estafeta_rates", {"description": "TERRESTRE", "type": {"$ne": "METROPOLITANO"}},
                      {"_id": 0}))
    rates = {rate.pop('type'): dict(**rate) for rate in rates}
    graph = GraphUndirectedWeighted(22)
    for i in range(1, 21):
        if i <= rates['TERRESTRE_2']['kg']:
            description = 'TERRESTRE_2'
            rate = rates[description]['total']
        elif rates['TERRESTRE_2']['kg'] < i <= rates['TERRESTRE_5']['kg']:
            description = 'TERRESTRE_5'
            rate = rates[description]['total']
        elif rates['TERRESTRE_5']['kg'] < i <= rates['TERRESTRE_10']['kg']:
            description = 'TERRESTRE_10'
            rate = rates[description]['total']
        else:
            description = 'TERRESTRE_20'
            rate = rates[description]['total']
        graph.add_edge(0, i, rate, description)
        if i == 1:
            continue
        graph.add_edge(i, i + 1, rates['TERRESTRE_2']['adicional'], "adicional")

    return graph
