from app import Database
from app.common.dijkstra import GraphUndirectedWeighted

RATES_COLLECTION = 'Estafeta_rates'
TYPES_STR_TO_ID = {"ESTAFETA_DIA_SIGUIENTE": "8619166", "ESTAFETA_TERRESTRE_CONSUMO": "1377731"}
TYPES_ID_TO_STR = {"8619166": "ESTAFETA_DIA_SIGUIENTE",
                   "1377731": "ESTAFETA_TERRESTRE_CONSUMO",
                   "8608731": "ESTAFETA_METROPOLITANDO"}
TYPES_ID_TOSERVICE_TYPE = {"DIA SIG.": "8619166",
                           "TERRESTRE": "1377731"}
TYPES = {"8619166",
         "8668532",
         "8622603",
         "4000613",
         "5056308",
         "5522411"
         }
MAX_WEIGHT = 70
SPECIAL_TYPE = "1377731"
# NON_OPTIMIZABLE_TYPES = {"8619166", "8646029", "8608731"}
# OPTIMIZABLE_TYPES = {"8668532", "8622603", "4000613", "5056308", "5522411"}
EXTRA_FEE = 64.11
TYPE_KG_LIMIT = 20
DF_ZIP_CODES = ['01000', '01010', '01020', '01030', '01030', '01040', '01048', '01049', '01050', '01060', '01060',
                '01070', '01080', '01089', '01090', '01090', '01090', '01100', '01109', '01110', '01110', '01110',
                '01110', '01120', '01120', '01120', '01120', '01125', '01130', '01130', '01130', '01130', '01139',
                '01140', '01140', '01150', '01150', '01160', '01160', '01160', '01160', '01170', '01170', '01180',
                '01180', '01180', '01184', '01200', '01210', '01219', '01220', '01220', '01220', '01220', '01220',
                '01220', '01230', '01230', '01230', '01230', '01230', '01239', '01240', '01250', '01250', '01250',
                '01250', '01250', '01259', '01259', '01260', '01260', '01260', '01260', '01260', '01269', '01269',
                '01270', '01270', '01270', '01270', '01270', '01270', '01275', '01276', '01278', '01279', '01280',
                '01280', '01280', '01280', '01280', '01285', '01289', '01290', '01290', '01296', '01296', '01296',
                '01298', '01299', '01299', '01310', '01320', '01330', '01340', '01376', '01376', '01376', '01376',
                '01377', '01379', '01389', '01400', '01400', '01407', '01408', '01410', '01410', '01419', '01420',
                '01420', '01430', '01440', '01450', '01450', '01450', '01460', '01470', '01470', '01480', '01490',
                '01490', '01500', '01500', '01509', '01510', '01510', '01510', '01520', '01520', '01520', '01520',
                '01520', '01530', '01537', '01538', '01539', '01539', '01540', '01540', '01540', '01540', '01540',
                '01548', '01549', '01550', '01550', '01550', '01560', '01560', '01560', '01560', '01566', '01567',
                '01569', '01588', '01590', '01600', '01610', '01610', '01618', '01618', '01619', '01619', '01620',
                '01630', '01630', '01630', '01630', '01640', '01645', '01650', '01650', '01650', '01650', '01650',
                '01650', '01650', '01700', '01700', '01700', '01700', '01700', '01700', '01708', '01708', '01710',
                '01710', '01720', '01729', '01730', '01730', '01740', '01740', '01740', '01750', '01750', '01750',
                '01759', '01760', '01760', '01760', '01770', '01770', '01780', '01780', '01788', '01789', '01790',
                '01790', '01800', '01807', '01810', '01820', '01820', '01830', '01840', '01849', '01849', '01856',
                '01857', '01859', '01860', '01863', '01870', '01900', '01904', '02000', '02010', '02010', '02010',
                '02020', '02020', '02040', '02040', '02050', '02050', '02060', '02060', '02070', '02070', '02080',
                '02080', '02090', '02099', '02100', '02109', '02120', '02128', '02129', '02130', '02140', '02150',
                '02160', '02169', '02200', '02230', '02240', '02240', '02250', '02300', '02310', '02320', '02330',
                '02340', '02360', '02400', '02410', '02419', '02420', '02420', '02430', '02440', '02450', '02450',
                '02459', '02460', '02470', '02479', '02480', '02490', '02500', '02510', '02510', '02519', '02520',
                '02525', '02530', '02540', '02600', '02630', '02630', '02640', '02650', '02660', '02670', '02680',
                '02700', '02710', '02719', '02720', '02720', '02729', '02730', '02739', '02750', '02750', '02760',
                '02760', '02770', '02780', '02790', '02800', '02810', '02810', '02830', '02840', '02850', '02860',
                '02870', '02900', '02910', '02920', '02930', '02940', '02950', '02960', '02970', '02980', '02980',
                '02990', '03000', '03010', '03020', '03023', '03100', '03100', '03103', '03104', '03200', '03220',
                '03230', '03240', '03300', '03303', '03310', '03313', '03320', '03330', '03340', '03400', '03410',
                '03420', '03430', '03440', '03500', '03510', '03520', '03530', '03540', '03550', '03560', '03570',
                '03580', '03590', '03600', '03610', '03620', '03630', '03640', '03650', '03660', '03700', '03710',
                '03720', '03730', '03740', '03800', '03810', '03820', '03840', '03900', '03910', '03920', '03930',
                '03940', '04000', '04010', '04020', '04030', '04040', '04100', '04120', '04120', '04200', '04210',
                '04230', '04239', '04240', '04250', '04260', '04260', '04260', '04260', '04270', '04300', '04310',
                '04318', '04319', '04319', '04320', '04320', '04320', '04326', '04330', '04330', '04330', '04330',
                '04340', '04340', '04350', '04350', '04350', '04359', '04360', '04360', '04368', '04369', '04370',
                '04370', '04380', '04380', '04390', '04390', '04400', '04410', '04410', '04420', '04440', '04440',
                '04440', '04450', '04460', '04470', '04470', '04480', '04480', '04480', '04480', '04489', '04490',
                '04490', '04500', '04510', '04519', '04530', '04600', '04610', '04620', '04630', '04640', '04650',
                '04660', '04660', '04700', '04710', '04718', '04719', '04730', '04730', '04738', '04739', '04800',
                '04800', '04810', '04815', '04830', '04840', '04849', '04870', '04890', '04890', '04899', '04908',
                '04909', '04909', '04909', '04910', '04918', '04919', '04920', '04929', '04930', '04938', '04939',
                '04940', '04950', '04960', '04970', '04980', '04980', '04980', '05000', '05010', '05020', '05030',
                '05030', '05039', '05050', '05060', '05100', '05110', '05118', '05119', '05120', '05129', '05200',
                '05214', '05219', '05220', '05230', '05238', '05240', '05260', '05268', '05269', '05270', '05280',
                '05310', '05320', '05330', '05330', '05330', '05330', '05348', '05360', '05370', '05379', '05400',
                '05410', '05410', '05500', '05520', '05530', '05600', '05610', '05619', '05620', '05700', '05710',
                '05730', '05750', '05760', '05780', '06000', '06010', '06020', '06030', '06038', '06040', '06050',
                '06060', '06070', '06080', '06090', '06100', '06140', '06170', '06200', '06220', '06240', '06250',
                '06270', '06280', '06300', '06350', '06400', '06430', '06450', '06470', '06500', '06600', '06700',
                '06707', '06720', '06760', '06780', '06800', '06820', '06840', '06850', '06860', '06870', '06880',
                '06890', '06900', '06920', '07000', '07010', '07010', '07010', '07020', '07040', '07050', '07058',
                '07060', '07069', '07070', '07070', '07070', '07080', '07089', '07090', '07090', '07100', '07100',
                '07109', '07110', '07119', '07119', '07130', '07130', '07140', '07140', '07140', '07140', '07144',
                '07144', '07149', '07150', '07150', '07160', '07164', '07164', '07164', '07164', '07170', '07180',
                '07180', '07180', '07183', '07187', '07188', '07189', '07190', '07199', '07200', '07207', '07209',
                '07210', '07214', '07220', '07220', '07224', '07230', '07239', '07240', '07249', '07249', '07250',
                '07259', '07268', '07269', '07270', '07279', '07280', '07290', '07300', '07300', '07310', '07320',
                '07320', '07320', '07323', '07326', '07328', '07330', '07340', '07340', '07350', '07350', '07359',
                '07360', '07360', '07363', '07369', '07370', '07380', '07380', '07400', '07410', '07410', '07420',
                '07420', '07430', '07440', '07450', '07455', '07456', '07456', '07457', '07457', '07458', '07459',
                '07460', '07469', '07470', '07480', '07500', '07509', '07509', '07510', '07520', '07530', '07540',
                '07548', '07549', '07549', '07550', '07560', '07570', '07580', '07600', '07620', '07630', '07640',
                '07650', '07670', '07680', '07700', '07707', '07708', '07709', '07720', '07730', '07730', '07730',
                '07739', '07740', '07750', '07754', '07755', '07760', '07770', '07770', '07780', '07780', '07790',
                '07790', '07800', '07810', '07820', '07820', '07830', '07838', '07839', '07840', '07840', '07850',
                '07850', '07858', '07859', '07860', '07860', '07869', '07870', '07870', '07880', '07889', '07890',
                '07890', '07890', '07899', '07900', '07909', '07910', '07918', '07919', '07920', '07920', '07930',
                '07939', '07940', '07950', '07960', '07960', '07960', '07969', '07969', '07970', '07979', '07979',
                '07980', '07990', '08000', '08010', '08020', '08029', '08030', '08040', '08100', '08200', '08210',
                '08220', '08230', '08240', '08300', '08310', '08320', '08400', '08420', '08500', '08510', '08600',
                '08610', '08620', '08650', '08700', '08710', '08720', '08730', '08760', '08760', '08760', '08770',
                '08800', '08810', '08830', '08840', '08900', '08910', '08920', '08930', '09000', '09000', '09000',
                '09000', '09000', '09000', '09000', '09010', '09020', '09030', '09040', '09040', '09060', '09060',
                '09070', '09080', '09089', '09090', '09099', '09100', '09110', '09120', '09130', '09140', '09160',
                '09160', '09180', '09200', '09208', '09209', '09210', '09220', '09230', '09230', '09230', '09230',
                '09233', '09239', '09240', '09250', '09260', '09270', '09280', '09290', '09300', '09310', '09310',
                '09310', '09319', '09320', '09350', '09359', '09360', '09360', '09368', '09369', '09369', '09369',
                '09400', '09400', '09410', '09410', '09410', '09410', '09420', '09420', '09429', '09430', '09430',
                '09438', '09440', '09440', '09440', '09450', '09460', '09470', '09479', '09480', '09500', '09500',
                '09510', '09520', '09520', '09530', '09550', '09560', '09570', '09577', '09577', '09578', '09579',
                '09600', '09608', '09609', '09620', '09630', '09630', '09630', '09630', '09630', '09630', '09630',
                '09630', '09630', '09630', '09630', '09630', '09630', '09630', '09630', '09637', '09638', '09640',
                '09640', '09648', '09660', '09670', '09680', '09689', '09690', '09696', '09698', '09700', '09700',
                '09700', '09700', '09704', '09704', '09704', '09705', '09705', '09706', '09706', '09708', '09709',
                '09710', '09719', '09720', '09720', '09730', '09740', '09750', '09750', '09750', '09760', '09767',
                '09769', '09770', '09780', '09780', '09790', '09800', '09800', '09800', '09800', '09800', '09800',
                '09800', '09800', '09800', '09800', '09800', '09809', '09810', '09810', '09810', '09810', '09819',
                '09820', '09820', '09820', '09820', '09820', '09828', '09829', '09830', '09830', '09830', '09830',
                '09830', '09836', '09837', '09838', '09839', '09839', '09840', '09849', '09850', '09850', '09850',
                '09856', '09856', '09857', '09858', '09859', '09860', '09860', '09860', '09860', '09860', '09860',
                '09860', '09864', '09868', '09870', '09870', '09870', '09870', '09880', '09880', '09880', '09880',
                '09889', '09890', '09897', '09897', '09899', '09900', '09900', '09900', '09910', '09910', '09920',
                '09930', '09940', '09960', '09960', '09960', '09960', '09960', '09969', '09970', '09979', '10000',
                '10010', '10010', '10020', '10100', '10130', '10200', '10300', '10309', '10320', '10330', '10340',
                '10350', '10360', '10368', '10369', '10369', '10370', '10378', '10379', '10380', '10400', '10500',
                '10580', '10600', '10610', '10620', '10630', '10640', '10640', '10640', '10660', '10700', '10710',
                '10720', '10800', '10810', '10820', '10830', '10840', '10840', '10900', '10910', '10920', '10926',
                '11000', '11000', '11000', '11000', '11000', '11000', '11000', '11000', '11040', '11100', '11100',
                '11109', '11200', '11200', '11210', '11220', '11220', '11230', '11239', '11240', '11250', '11259',
                '11260', '11260', '11270', '11280', '11289', '11290', '11290', '11300', '11310', '11320', '11320',
                '11330', '11340', '11350', '11360', '11370', '11400', '11410', '11410', '11420', '11430', '11430',
                '11440', '11440', '11450', '11450', '11450', '11460', '11460', '11460', '11460', '11470', '11470',
                '11479', '11480', '11480', '11489', '11490', '11490', '11500', '11510', '11520', '11529', '11530',
                '11540', '11550', '11560', '11580', '11590', '11600', '11610', '11619', '11649', '11650', '11700',
                '11800', '11800', '11810', '11820', '11830', '11840', '11850', '11850', '11860', '11870', '11910',
                '11920', '11930', '11950', '12000', '12000', '12000', '12000', '12000', '12000', '12000', '12070',
                '12080', '12100', '12100', '12100', '12100', '12100', '12110', '12110', '12200', '12200', '12200',
                '12200', '12250', '12300', '12400', '12400', '12400', '12410', '12500', '12600', '12700', '12800',
                '12910', '12920', '12930', '12940', '12950', '13000', '13010', '13020', '13030', '13040', '13050',
                '13060', '13060', '13060', '13063', '13070', '13070', '13080', '13090', '13093', '13094', '13099',
                '13100', '13100', '13110', '13119', '13120', '13120', '13123', '13123', '13123', '13129', '13150',
                '13180', '13200', '13210', '13219', '13219', '13220', '13230', '13250', '13270', '13273', '13278',
                '13278', '13280', '13300', '13300', '13300', '13300', '13300', '13310', '13315', '13317', '13317',
                '13318', '13319', '13360', '13360', '13360', '13363', '13400', '13410', '13410', '13419', '13420',
                '13430', '13440', '13450', '13450', '13460', '13508', '13508', '13509', '13510', '13520', '13529',
                '13530', '13530', '13540', '13540', '13545', '13546', '13549', '13550', '13550', '13559', '13600',
                '13610', '13625', '13630', '13640', '13700', '13700', '14000', '14000', '14010', '14020', '14030',
                '14038', '14038', '14039', '14039', '14040', '14040', '14049', '14050', '14060', '14070', '14070',
                '14070', '14070', '14080', '14080', '14090', '14098', '14100', '14100', '14100', '14100', '14100',
                '14108', '14108', '14110', '14110', '14120', '14129', '14130', '14140', '14148', '14150', '14160',
                '14200', '14200', '14208', '14209', '14210', '14219', '14219', '14220', '14220', '14230', '14239',
                '14240', '14240', '14248', '14250', '14250', '14250', '14250', '14260', '14260', '14266', '14267',
                '14268', '14269', '14270', '14273', '14275', '14276', '14300', '14300', '14300', '14307', '14308',
                '14308', '14309', '14310', '14310', '14310', '14320', '14325', '14326', '14327', '14328', '14328',
                '14329', '14330', '14330', '14330', '14334', '14335', '14336', '14337', '14338', '14338', '14340',
                '14340', '14350', '14356', '14357', '14357', '14358', '14360', '14360', '14360', '14370', '14370',
                '14370', '14370', '14376', '14377', '14378', '14380', '14380', '14386', '14387', '14388', '14389',
                '14390', '14390', '14390', '14390', '14399', '14400', '14406', '14408', '14409', '14410', '14420',
                '14420', '14420', '14426', '14426', '14427', '14427', '14428', '14429', '14430', '14430', '14438',
                '14439', '14440', '14449', '14449', '14449', '14456', '14460', '14470', '14470', '14476', '14479',
                '14480', '14490', '14500', '14520', '14529', '14550', '14600', '14608', '14609', '14610', '14620',
                '14629', '14630', '14630', '14639', '14640', '14643', '14646', '14647', '14647', '14647', '14650',
                '14653', '14654', '14654', '14655', '14657', '14658', '14659', '14700', '14710', '14720', '14730',
                '14734', '14735', '14735', '14737', '14738', '14739', '14740', '14748', '14748', '14749', '14750',
                '14760', '14780', '14790', '14900', '15000', '15010', '15020', '15100', '15120', '15200', '15210',
                '15220', '15220', '15230', '15240', '15250', '15260', '15270', '15280', '15290', '15299', '15300',
                '15309', '15310', '15320', '15330', '15339', '15340', '15350', '15370', '15380', '15390', '15400',
                '15410', '15420', '15430', '15440', '15450', '15460', '15470', '15500', '15510', '15520', '15530',
                '15540', '15600', '15610', '15620', '15630', '15640', '15640', '15650', '15660', '15670', '15680',
                '15700', '15710', '15720', '15730', '15740', '15750', '15800', '15810', '15820', '15830', '15840',
                '15850', '15860', '15870', '15900', '15950', '15960', '15968', '15970', '15980', '15990', '16000',
                '16000', '16000', '16010', '16010', '16010', '16010', '16010', '16010', '16020', '16020', '16029',
                '16030', '16030', '16030', '16030', '16034', '16035', '16035', '16036', '16038', '16040', '16040',
                '16050', '16050', '16050', '16057', '16058', '16059', '16059', '16060', '16070', '16070', '16070',
                '16070', '16080', '16080', '16080', '16080', '16090', '16090', '16090', '16090', '16100', '16200',
                '16210', '16220', '16240', '16240', '16244', '16247', '16248', '16300', '16310', '16320', '16340',
                '16400', '16410', '16420', '16428', '16429', '16430', '16440', '16443', '16450', '16457', '16459',
                '16500', '16510', '16513', '16513', '16514', '16514', '16514', '16514', '16515', '16520', '16520',
                '16530', '16530', '16533', '16550', '16550', '16600', '16604', '16605', '16606', '16607', '16609',
                '16610', '16614', '16615', '16616', '16617', '16620', '16629', '16629', '16630', '16640', '16710',
                '16720', '16739', '16740', '16749', '16750', '16770', '16776', '16776', '16776', '16780', '16780',
                '16780', '16780', '16780', '16780', '16797', '16799', '16800', '16808', '16810', '16810', '16810',
                '16810', '16810', '16810', '16810', '16813', '16819', '16819', '16840', '16840', '16850', '16850',
                '16860', '16866', '16869', '16870', '16880', '16880', '16880', '16888', '16888', '16888', '16889',
                '16900', '16900', '16909', '16910']


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
