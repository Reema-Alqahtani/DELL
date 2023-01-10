"""Check if a host is in the Google Chrome HSTS Preload list"""

import functools
import os
import typing

__version__ = "2022.12.1"
__checksum__ = "1ff634747300a9e98206f93f7231fd09c00f55fdf77c114d75c90c810348efab"
__all__ = ["in_hsts_preload"]

# fmt: off
_GTLD_INCLUDE_SUBDOMAINS = {b'android', b'app', b'azure', b'bank', b'bing', b'boo', b'channel', b'chrome', b'dad', b'day', b'dev', b'eat', b'esq', b'fly', b'foo', b'gle', b'gmail', b'google', b'hangout', b'hotmail', b'ing', b'insurance', b'meet', b'meme', b'microsoft', b'mov', b'new', b'nexus', b'office', b'page', b'phd', b'play', b'prof', b'rsvp', b'search', b'skype', b'windows', b'xbox', b'youtube', b'zip'}  # noqa: E501
_JUMPTABLE = [[(0, 11), (11, 10), (21, 9), (30, 61), (91, 26), (117, 12), None, (129, 19), (148, 22), (170, 7), (177, 20), (197, 18), None, (215, 29), (244, 45), (289, 7), (296, 9), (305, 36), (341, 24), (365, 10), (375, 28), None, (403, 62), (465, 8), (473, 28), (501, 19), (520, 13), (533, 14), (547, 14), None, None, (561, 40), (601, 20), (621, 35), (656, 14), (670, 32), (702, 28), (730, 9), (739, 25), (764, 25), (789, 8), (797, 13), (810, 10), None, (820, 17), (837, 6), (843, 26), (869, 10), (879, 5), (884, 19), (903, 14), (917, 11), (928, 12), (940, 27), None, (967, 24), (991, 11), (1002, 7), (1009, 29), (1038, 18), (1056, 27), (1083, 46), (1129, 25), (1154, 16), (1170, 18), (1188, 5), (1193, 22), (1215, 18), None, (1233, 36), (1269, 15), (1284, 8), (1292, 11), None, (1303, 5), (1308, 23), (1331, 18), (1349, 18), None, (1367, 20), (1387, 26), (1413, 48), (1461, 19), (1480, 20), (1500, 59), (1559, 14), (1573, 14), (1587, 20), None, (1607, 10), (1617, 13), (1630, 20), (1650, 29), None, (1679, 13), (1692, 19), (1711, 11), (1722, 4), (1726, 22), (1748, 10), (1758, 13), (1771, 14), (1785, 28), (1813, 11), (1824, 21), (1845, 12), (1857, 32), None, (1889, 10), (1899, 14), (1913, 26), (1939, 45), (1984, 15), None, (1999, 11), (2010, 30), (2040, 21), (2061, 26), (2087, 6), (2093, 6), (2099, 7), (2106, 5), (2111, 30), (2141, 23), (2164, 35), (2199, 17), (2216, 15), (2231, 29), (2260, 12), (2272, 70), (2342, 55), (2397, 12), (2409, 23), (2432, 16), (2448, 42), (2490, 6), (2496, 24), (2520, 44), (2564, 6), (2570, 41), (2611, 22), (2633, 23), (2656, 36), (2692, 20), (2712, 8), (2720, 15), (2735, 12), (2747, 19), (2766, 25), (2791, 15), None, (2806, 46), (2852, 21), (2873, 17), (2890, 23), (2913, 26), (2939, 5), (2944, 37), (2981, 39), (3020, 16), (3036, 33), (3069, 17), (3086, 23), (3109, 14), (3123, 17), (3140, 8), (3148, 14), (3162, 7), (3169, 29), (3198, 6), (3204, 18), (3222, 32), (3254, 20), (3274, 17), (3291, 24), (3315, 12), (3327, 40), (3367, 40), (3407, 12), (3419, 48), (3467, 32), (3499, 17), None, (3516, 8), (3524, 25), (3549, 25), (3574, 6), (3580, 23), None, (3603, 36), (3639, 33), (3672, 14), (3686, 16), (3702, 27), None, (3729, 30), (3759, 41), (3800, 50), (3850, 15), (3865, 20), (3885, 31), (3916, 21), (3937, 32), (3969, 24), (3993, 20), (4013, 17), (4030, 60), (4090, 6), (4096, 9), (4105, 12), (4117, 18), (4135, 11), (4146, 10), (4156, 48), (4204, 42), None, (4246, 36), (4282, 28), None, (4310, 8), (4318, 8), (4326, 7), None, (4333, 25), (4358, 17), None, (4375, 21), (4396, 35), (4431, 21), (4452, 10), (4462, 41), (4503, 20), (4523, 31), (4554, 32), (4586, 19), (4605, 12), (4617, 5), (4622, 30), (4652, 29), (4681, 14), (4695, 14), (4709, 47), (4756, 52), None, None, (4808, 51), (4859, 42), None, (4901, 18), None, (4919, 15), (4934, 8), (4942, 21), (4963, 6), (4969, 16), (4985, 22)], [(5007, 10435), (15442, 10697), (26139, 10917), (37056, 10256), (47312, 10275), (57587, 10078), (67665, 11093), (78758, 9865), (88623, 11007), (99630, 10321), (109951, 11320), (121271, 10289), (131560, 10922), (142482, 12043), (154525, 10596), (165121, 11261), (176382, 11620), (188002, 10926), (198928, 10860), (209788, 10004), (219792, 11180), (230972, 10807), (241779, 10869), (252648, 10918), (263566, 11317), (274883, 10710), (285593, 11111), (296704, 10945), (307649, 10306), (317955, 10782), (328737, 11350), (340087, 10944), (351031, 10745), (361776, 10556), (372332, 10091), (382423, 10881), (393304, 10646), (403950, 11482), (415432, 11289), (426721, 11390), (438111, 11680), (449791, 10202), (459993, 10398), (470391, 10707), (481098, 10736), (491834, 11050), (502884, 10476), (513360, 11992), (525352, 10826), (536178, 9843), (546021, 10718), (556739, 11114), (567853, 10987), (578840, 10656), (589496, 10990), (600486, 10718), (611204, 10971), (622175, 10847), (633022, 10895), (643917, 9352), (653269, 10611), (663880, 10685), (674565, 10666), (685231, 11029), (696260, 11116), (707376, 11227), (718603, 10751), (729354, 11346), (740700, 11472), (752172, 10900), (763072, 10689), (773761, 10241), (784002, 9662), (793664, 11197), (804861, 10697), (815558, 11269), (826827, 10152), (836979, 11606), (848585, 10724), (859309, 10322), (869631, 11035), (880666, 9558), (890224, 10477), (900701, 10788), (911489, 10350), (921839, 10931), (932770, 11416), (944186, 10602), (954788, 10899), (965687, 10889), (976576, 12321), (988897, 10271), (999168, 10554), (1009722, 10451), (1020173, 10893), (1031066, 11072), (1042138, 10789), (1052927, 10477), (1063404, 11021), (1074425, 10257), (1084682, 10580), (1095262, 10739), (1106001, 10524), (1116525, 10481), (1127006, 10503), (1137509, 11075), (1148584, 11316), (1159900, 11207), (1171107, 11699), (1182806, 10942), (1193748, 11450), (1205198, 10874), (1216072, 10547), (1226619, 10681), (1237300, 10985), (1248285, 10897), (1259182, 10978), (1270160, 10828), (1280988, 10605), (1291593, 11666), (1303259, 11372), (1314631, 11059), (1325690, 10801), (1336491, 11261), (1347752, 11891), (1359643, 10696), (1370339, 10423), (1380762, 11660), (1392422, 10659), (1403081, 12345), (1415426, 11412), (1426838, 10541), (1437379, 10729), (1448108, 10314), (1458422, 10659), (1469081, 10962), (1480043, 10258), (1490301, 11468), (1501769, 10542), (1512311, 10535), (1522846, 11335), (1534181, 11313), (1545494, 10191), (1555685, 10579), (1566264, 11306), (1577570, 10113), (1587683, 10969), (1598652, 10470), (1609122, 10383), (1619505, 11103), (1630608, 10947), (1641555, 11073), (1652628, 10968), (1663596, 10173), (1673769, 10893), (1684662, 10803), (1695465, 10744), (1706209, 11083), (1717292, 10258), (1727550, 10014), (1737564, 10035), (1747599, 10917), (1758516, 11494), (1770010, 10092), (1780102, 10793), (1790895, 11925), (1802820, 10978), (1813798, 10384), (1824182, 11670), (1835852, 10605), (1846457, 10020), (1856477, 10620), (1867097, 12146), (1879243, 10176), (1889419, 10074), (1899493, 11277), (1910770, 10698), (1921468, 11062), (1932530, 10634), (1943164, 10244), (1953408, 13135), (1966543, 10833), (1977376, 10659), (1988035, 10765), (1998800, 11432), (2010232, 11779), (2022011, 9976), (2031987, 11347), (2043334, 10854), (2054188, 10552), (2064740, 11742), (2076482, 10200), (2086682, 10815), (2097497, 10546), (2108043, 10954), (2118997, 10888), (2129885, 10512), (2140397, 9964), (2150361, 10608), (2160969, 10255), (2171224, 11199), (2182423, 10834), (2193257, 11589), (2204846, 10499), (2215345, 11519), (2226864, 11321), (2238185, 10004), (2248189, 11178), (2259367, 11111), (2270478, 10997), (2281475, 11011), (2292486, 11094), (2303580, 10921), (2314501, 10651), (2325152, 11029), (2336181, 10621), (2346802, 10328), (2357130, 10969), (2368099, 10383), (2378482, 11585), (2390067, 10432), (2400499, 10120), (2410619, 11605), (2422224, 10731), (2432955, 11099), (2444054, 10594), (2454648, 10736), (2465384, 10027), (2475411, 11178), (2486589, 10940), (2497529, 11714), (2509243, 10625), (2519868, 10327), (2530195, 11287), (2541482, 10805), (2552287, 11788), (2564075, 10418), (2574493, 9994), (2584487, 9922), (2594409, 11431), (2605840, 11201), (2617041, 11413), (2628454, 10817), (2639271, 11071), (2650342, 10275), (2660617, 11330), (2671947, 11141), (2683088, 10148), (2693236, 10787), (2704023, 10274), (2714297, 10840), (2725137, 11085), (2736222, 11158), (2747380, 10535), (2757915, 10738), (2768653, 10750)], [(2779403, 1229), (2780632, 912), (2781544, 947), (2782491, 1192), (2783683, 927), (2784610, 1057), (2785667, 913), (2786580, 1298), (2787878, 915), (2788793, 1065), (2789858, 735), (2790593, 826), (2791419, 1102), (2792521, 1206), (2793727, 1228), (2794955, 1288), (2796243, 1594), (2797837, 889), (2798726, 1118), (2799844, 1061), (2800905, 1187), (2802092, 963), (2803055, 1228), (2804283, 985), (2805268, 1079), (2806347, 959), (2807306, 1413), (2808719, 1553), (2810272, 1048), (2811320, 1092), (2812412, 1214), (2813626, 1135), (2814761, 909), (2815670, 1019), (2816689, 1281), (2817970, 1081), (2819051, 1003), (2820054, 1091), (2821145, 1049), (2822194, 1401), (2823595, 1046), (2824641, 1281), (2825922, 1005), (2826927, 1028), (2827955, 1038), (2828993, 802), (2829795, 1229), (2831024, 1276), (2832300, 1045), (2833345, 719), (2834064, 1052), (2835116, 1050), (2836166, 1101), (2837267, 1302), (2838569, 1664), (2840233, 878), (2841111, 976), (2842087, 1033), (2843120, 972), (2844092, 1035), (2845127, 1104), (2846231, 1188), (2847419, 1371), (2848790, 1215), (2850005, 985), (2850990, 1158), (2852148, 1021), (2853169, 815), (2853984, 978), (2854962, 1175), (2856137, 1035), (2857172, 1079), (2858251, 797), (2859048, 1067), (2860115, 896), (2861011, 1015), (2862026, 897), (2862923, 988), (2863911, 1074), (2864985, 837), (2865822, 1160), (2866982, 926), (2867908, 1162), (2869070, 937), (2870007, 1021), (2871028, 918), (2871946, 1036), (2872982, 1095), (2874077, 1197), (2875274, 1130), (2876404, 1460), (2877864, 1392), (2879256, 1298), (2880554, 979), (2881533, 1109), (2882642, 724), (2883366, 1220), (2884586, 1038), (2885624, 852), (2886476, 907), (2887383, 1080), (2888463, 1271), (2889734, 1092), (2890826, 779), (2891605, 956), (2892561, 1123), (2893684, 792), (2894476, 724), (2895200, 1226), (2896426, 1391), (2897817, 1123), (2898940, 980), (2899920, 1091), (2901011, 1113), (2902124, 1080), (2903204, 1090), (2904294, 1009), (2905303, 910), (2906213, 975), (2907188, 879), (2908067, 1381), (2909448, 1017), (2910465, 1112), (2911577, 745), (2912322, 1082), (2913404, 1081), (2914485, 1052), (2915537, 1237), (2916774, 976), (2917750, 1346), (2919096, 1136), (2920232, 1007), (2921239, 1107), (2922346, 908), (2923254, 1145), (2924399, 1171), (2925570, 1021), (2926591, 1007), (2927598, 1029), (2928627, 855), (2929482, 955), (2930437, 926), (2931363, 1008), (2932371, 815), (2933186, 793), (2933979, 755), (2934734, 1026), (2935760, 896), (2936656, 976), (2937632, 926), (2938558, 1013), (2939571, 906), (2940477, 773), (2941250, 1174), (2942424, 1130), (2943554, 981), (2944535, 966), (2945501, 1229), (2946730, 1070), (2947800, 884), (2948684, 1329), (2950013, 1006), (2951019, 952), (2951971, 1133), (2953104, 1340), (2954444, 1001), (2955445, 922), (2956367, 1183), (2957550, 985), (2958535, 962), (2959497, 1030), (2960527, 906), (2961433, 1261), (2962694, 1091), (2963785, 1133), (2964918, 1221), (2966139, 1120), (2967259, 884), (2968143, 1051), (2969194, 1002), (2970196, 2196), (2972392, 805), (2973197, 1044), (2974241, 1036), (2975277, 1358), (2976635, 1031), (2977666, 991), (2978657, 928), (2979585, 829), (2980414, 1330), (2981744, 888), (2982632, 812), (2983444, 1055), (2984499, 1320), (2985819, 1239), (2987058, 1155), (2988213, 1005), (2989218, 848), (2990066, 1024), (2991090, 975), (2992065, 1141), (2993206, 883), (2994089, 1134), (2995223, 909), (2996132, 1083), (2997215, 837), (2998052, 1108), (2999160, 1338), (3000498, 1015), (3001513, 1242), (3002755, 1070), (3003825, 1042), (3004867, 1187), (3006054, 1382), (3007436, 1035), (3008471, 998), (3009469, 1190), (3010659, 944), (3011603, 914), (3012517, 749), (3013266, 1055), (3014321, 1179), (3015500, 834), (3016334, 1325), (3017659, 869), (3018528, 1089), (3019617, 1012), (3020629, 1194), (3021823, 1188), (3023011, 1047), (3024058, 1178), (3025236, 879), (3026115, 1244), (3027359, 973), (3028332, 907), (3029239, 868), (3030107, 958), (3031065, 599), (3031664, 1151), (3032815, 1274), (3034089, 1092), (3035181, 924), (3036105, 969), (3037074, 859), (3037933, 1187), (3039120, 909), (3040029, 845), (3040874, 1218), (3042092, 771), (3042863, 1202), (3044065, 2741), (3046806, 925), (3047731, 980), (3048711, 1246), (3049957, 1193), (3051150, 737)], [(3051887, 48), None, (3051935, 35), (3051970, 42), None, None, None, None, None, None, None, None, None, None, (3052012, 21), None, None, (3052033, 42), None, (3052075, 25), (3052100, 44), (3052144, 22), (3052166, 82), None, None, None, None, (3052248, 26), None, None, None, None, (3052274, 21), (3052295, 46), None, (3052341, 21), (3052362, 44), None, None, None, None, (3052406, 71), (3052477, 21), (3052498, 23), None, None, None, None, (3052521, 48), None, None, None, None, None, (3052569, 31), None, None, None, None, (3052600, 42), None, (3052642, 22), None, (3052664, 21), None, (3052685, 26), (3052711, 56), None, None, (3052767, 77), (3052844, 27), None, None, None, None, (3052871, 21), (3052892, 52), None, None, (3052944, 54), (3052998, 42), None, None, None, (3053040, 25), None, None, (3053065, 21), None, None, None, None, None, (3053086, 24), (3053110, 21), None, None, (3053131, 48), None, (3053179, 18), None, (3053197, 54), None, None, None, None, None, None, (3053251, 26), None, None, None, (3053277, 20), (3053297, 28), None, (3053325, 64), (3053389, 42), (3053431, 17), (3053448, 17), (3053465, 26), None, (3053491, 45), None, None, None, (3053536, 26), (3053562, 20), (3053582, 26), (3053608, 16), (3053624, 42), (3053666, 63), None, (3053729, 20), None, (3053749, 40), (3053789, 48), None, None, None, (3053837, 47), None, None, None, None, None, None, None, (3053884, 42), None, (3053926, 80), None, (3054006, 9), None, (3054015, 21), (3054036, 42), None, None, (3054078, 65), (3054143, 82), (3054225, 45), None, (3054270, 72), None, None, (3054342, 24), (3054366, 21), None, None, None, None, None, (3054387, 42), (3054429, 21), (3054450, 21), None, (3054471, 42), (3054513, 25), None, (3054538, 38), (3054576, 21), (3054597, 73), None, None, (3054670, 21), (3054691, 19), (3054710, 26), (3054736, 24), (3054760, 16), None, (3054776, 21), None, None, (3054797, 38), None, (3054835, 22), (3054857, 21), (3054878, 21), (3054899, 21), None, (3054920, 63), None, (3054983, 21), (3055004, 42), None, (3055046, 17), None, None, None, None, (3055063, 21), (3055084, 21), None, None, (3055105, 21), None, None, (3055126, 21), None, (3055147, 26), None, (3055173, 50), (3055223, 22), None, None, (3055245, 50), (3055295, 26), (3055321, 21), (3055342, 21), (3055363, 19), None, (3055382, 35), (3055417, 26), (3055443, 23), (3055466, 39), (3055505, 42), None, None, None, None, None, None, (3055547, 21), None, None, None, (3055568, 21), None, None, (3055589, 90), None, (3055679, 239), (3055918, 38), None, None, (3055956, 21), None]]  # noqa: E501
_CRC8_TABLE = [
    0x00, 0x07, 0x0e, 0x09, 0x1c, 0x1b, 0x12, 0x15,
    0x38, 0x3f, 0x36, 0x31, 0x24, 0x23, 0x2a, 0x2d,
    0x70, 0x77, 0x7e, 0x79, 0x6c, 0x6b, 0x62, 0x65,
    0x48, 0x4f, 0x46, 0x41, 0x54, 0x53, 0x5a, 0x5d,
    0xe0, 0xe7, 0xee, 0xe9, 0xfc, 0xfb, 0xf2, 0xf5,
    0xd8, 0xdf, 0xd6, 0xd1, 0xc4, 0xc3, 0xca, 0xcd,
    0x90, 0x97, 0x9e, 0x99, 0x8c, 0x8b, 0x82, 0x85,
    0xa8, 0xaf, 0xa6, 0xa1, 0xb4, 0xb3, 0xba, 0xbd,
    0xc7, 0xc0, 0xc9, 0xce, 0xdb, 0xdc, 0xd5, 0xd2,
    0xff, 0xf8, 0xf1, 0xf6, 0xe3, 0xe4, 0xed, 0xea,
    0xb7, 0xb0, 0xb9, 0xbe, 0xab, 0xac, 0xa5, 0xa2,
    0x8f, 0x88, 0x81, 0x86, 0x93, 0x94, 0x9d, 0x9a,
    0x27, 0x20, 0x29, 0x2e, 0x3b, 0x3c, 0x35, 0x32,
    0x1f, 0x18, 0x11, 0x16, 0x03, 0x04, 0x0d, 0x0a,
    0x57, 0x50, 0x59, 0x5e, 0x4b, 0x4c, 0x45, 0x42,
    0x6f, 0x68, 0x61, 0x66, 0x73, 0x74, 0x7d, 0x7a,
    0x89, 0x8e, 0x87, 0x80, 0x95, 0x92, 0x9b, 0x9c,
    0xb1, 0xb6, 0xbf, 0xb8, 0xad, 0xaa, 0xa3, 0xa4,
    0xf9, 0xfe, 0xf7, 0xf0, 0xe5, 0xe2, 0xeb, 0xec,
    0xc1, 0xc6, 0xcf, 0xc8, 0xdd, 0xda, 0xd3, 0xd4,
    0x69, 0x6e, 0x67, 0x60, 0x75, 0x72, 0x7b, 0x7c,
    0x51, 0x56, 0x5f, 0x58, 0x4d, 0x4a, 0x43, 0x44,
    0x19, 0x1e, 0x17, 0x10, 0x05, 0x02, 0x0b, 0x0c,
    0x21, 0x26, 0x2f, 0x28, 0x3d, 0x3a, 0x33, 0x34,
    0x4e, 0x49, 0x40, 0x47, 0x52, 0x55, 0x5c, 0x5b,
    0x76, 0x71, 0x78, 0x7f, 0x6a, 0x6d, 0x64, 0x63,
    0x3e, 0x39, 0x30, 0x37, 0x22, 0x25, 0x2c, 0x2b,
    0x06, 0x01, 0x08, 0x0f, 0x1a, 0x1d, 0x14, 0x13,
    0xae, 0xa9, 0xa0, 0xa7, 0xb2, 0xb5, 0xbc, 0xbb,
    0x96, 0x91, 0x98, 0x9f, 0x8a, 0x8d, 0x84, 0x83,
    0xde, 0xd9, 0xd0, 0xd7, 0xc2, 0xc5, 0xcc, 0xcb,
    0xe6, 0xe1, 0xe8, 0xef, 0xfa, 0xfd, 0xf4, 0xf3
]
# fmt: on

_IS_LEAF = 0x80
_INCLUDE_SUBDOMAINS = 0x40


try:
    from importlib.resources import open_binary

    def open_pkg_binary(path: str) -> typing.BinaryIO:
        return open_binary("hstspreload", path)


except ImportError:

    def open_pkg_binary(path: str) -> typing.BinaryIO:
        return open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), path),
            "rb",
        )


@functools.lru_cache(maxsize=1024)
def in_hsts_preload(host: typing.AnyStr) -> bool:
    """Determines if an IDNA-encoded host is on the HSTS preload list"""

    if isinstance(host, str):
        host = host.encode("ascii")
    labels = host.lower().split(b".")

    # Fast-branch for gTLDs that are registered to preload all sub-domains.
    if labels[-1] in _GTLD_INCLUDE_SUBDOMAINS:
        return True

    with open_pkg_binary("hstspreload.bin") as f:
        for layer, label in enumerate(labels[::-1]):
            # None of our layers are greater than 4 deep.
            if layer > 3:
                return False

            # Read the jump table for the layer and label
            jump_info = _JUMPTABLE[layer][_crc8(label)]
            if jump_info is None:
                # No entry: host is not preloaded
                return False

            # Read the set of entries for that layer and label
            f.seek(jump_info[0])
            data = bytearray(jump_info[1])
            f.readinto(data)

            for is_leaf, include_subdomains, ent_label in _iter_entries(data):
                # We found a potential leaf
                if is_leaf:
                    if ent_label == host:
                        return True
                    if include_subdomains and host.endswith(b"." + ent_label):
                        return True

                # Continue traversing as we're not at a leaf.
                elif label == ent_label:
                    break
            else:
                return False
    return False


def _iter_entries(data: bytes) -> typing.Iterable[typing.Tuple[int, int, bytes]]:
    while data:
        flags = data[0]
        size = data[1]
        label = bytes(data[2 : 2 + size])
        yield (flags & _IS_LEAF, flags & _INCLUDE_SUBDOMAINS, label)
        data = data[2 + size :]


def _crc8(value: bytes) -> int:
    # CRC8 reference implementation: https://github.com/niccokunzmann/crc8
    checksum = 0x00
    for byte in value:
        checksum = _CRC8_TABLE[checksum ^ byte]
    return checksum