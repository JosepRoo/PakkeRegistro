from app import Database
from app.common.dijkstra import GraphUndirectedWeighted

RATES_COLLECTION = 'Estafeta_rates'
TYPES_STR_TO_ID = {"ESTAFETA_DIA_SIGUIENTE": "8619166", "ESTAFETA_TERRESTRE_CONSUMO": "1377731"}
TYPES_ID_TO_STR = {"8619166": "ESTAFETA_DIA_SIGUIENTE",
                   "1377731": "ESTAFETA_TERRESTRE_CONSUMO",
                   "8608731": "ESTAFETA_METROPOLITANDO"}
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
DF_ZIP_CODES = ['01020', '01110', '01210', '01790', '02300', '02460', '02630', '02770', '02800', '02870', '03020', '03400', '03100', '03810', '03700', '03510', '03900', '03940', '04100', '04620', '04650', '04910', '05100', '05120', '06400', '06600', '06700', '06720', '06800', '06900', '07770', '07780', '07800', '07820', '07920', '08100', '08200', '08300', '08400', '08500', '09040', '09060', '09070', '09230', '09510', '09620', '09640', '09810', '09850', '10370', '10300', '11000', '11230', '11400', '11500', '11510', '11520', '11560', '11580', '11590', '11650', '11700', '11800', '11820', '11850', '13270', '14020', '14090', '15400', '15810', '15820', '15850', '15900', '16050']


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
