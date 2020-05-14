import math
import bisect
import random
#We define a get_index function, to make it possible to get the value from a key in a dictionary range.
def get_index(p):
    lower = math.floor(p/5)*5
    return range(lower, lower+4)

#We define a class that can create list of items that can be drawn with different probabilities
class WeightedTuple(object):
    """
    >>> p = WeightedTuple({'A': 2, 'B': 1, 'C': 3})
    >>> len(p)
    6
    >>> p[0], p[1], p[2], p[3], p[4], p[5]
    ('A', 'A', 'B', 'C', 'C', 'C')
    >>> p[-1], p[-2], p[-3], p[-4], p[-5], p[-6]
    ('C', 'C', 'C', 'B', 'A', 'A')
    >>> p[6]
    Traceback (most recent call last):
    ...
    IndexError
    >>> p[-7]
    Traceback (most recent call last):
    ...
    IndexError
    """
    def __init__(self, items):
        self.indexes = []
        self.items = []
        next_index = 0
        for key in sorted(items.keys()):
            val = items[key]
            self.indexes.append(next_index)
            self.items.append(key)
            next_index += val

        self.len = next_index

    def __getitem__(self, n):
        if n < 0:
            n = self.len + n
        if n < 0 or n >= self.len:
            raise IndexError

        idx = bisect.bisect_right(self.indexes, n)
        return self.items[idx-1]

    def __len__(self):
        return self.len

#Probabilities to generate age distribution. FOLK1A
dict_age = WeightedTuple({
20	:	16816618	,
21	:	17229276	,
22	:	17826348	,
23	:	18191678	,
24	:	18970132	,
25	:	19219592	,
26	:	18695260	,
27	:	18922805	,
28	:	18300787	,
29	:	18306383	,
30	:	17767363	,
31	:	17206428	,
32	:	16478332	,
33	:	16232603	,
34	:	15860045	,
35	:	15265538	,
36	:	14941707	,
37	:	15259477	,
38	:	15141974	,
39	:	15968922	,
40	:	16221878	,
41	:	16623112	,
42	:	16495818	,
43	:	17106878	,
44	:	18452328	,
45	:	18165799	,
46	:	18056923	,
47	:	18835377	,
48	:	18555376	,
49	:	17751510	,
50	:	17631909	,
51	:	18245999	,
52	:	19414730	,
53	:	20727541	,
54	:	20011568	,
55	:	19445738	,
56	:	18957543	,
57	:	17820985	,
58	:	17240933	,
59	:	17118535	,
60	:	16304643	,
61	:	16289256	,
62	:	16043759	,
63	:	16014850	,
64	:	15634133	,
65	:	15202824	,
66	:	15296546	,
67	:	14824671	,
68	:	14422271	,
69	:	14689449	,
70	:	14409215	,
71	:	14965254	,
72	:	15628770	,
73	:	15793600	,
74	:	14869667	,
75	:	13703501	,
76	:	12304661	,
77	:	11249936	,
78	:	9644534	,
79	:	9012725	,
80	:	8213987	,

})

#List of age specific moving rates (Hansen et al. 2013)
dict_move= {
    range(20, 24):0.0352618642070509,
    range(25, 29):0.0184234701262483,
    range(30, 34):0.0110659331391373,
    range(35, 39):0.00864987447880838,
    range(40, 44):0.00602930806612689,
    range(45, 49):0.00514301283182295,
    range(50, 54):0.00426531877756064,
    range(55, 59):0.00382964301630206,
    range(60, 64):0.00382964301630206,
    range(65, 69):0.00382964301630206,
    range(70, 74):0.00210759323186027,
    range(75, 79):0.00210759323186027,
    range(80, 84):0.00210759323186027,
    range(85, 89):0.00134321224262823,
    range(90, 94):0.00134321224262823,
    range(95, 99):0.00134321224262823,
    range(100, 104):0.00134321224262823,
    range(105, 109):0.00134321224262823,
    }

# List of age specific death rates
dict_death = {
    range(20, 24): 0.01 ,
    range(25, 29): 0.01 ,
    range(30, 34): 0 ,
    range(35, 39): 0,
    range(40, 44): 0 ,
    range(45, 49): 0 ,
    range(50, 54): 0 ,
    range(55, 59): 0 ,
    range(60, 64): 0 ,
    range(65, 69): 0 ,
    range(70, 74): 0,
    range(75, 79): 0,
    range(80, 84): 0,
    range(85, 89): 0,
    range(90, 94): 0,
    range(95, 99): 0,
    range(100, 104): 0,
    }

# List of age specific retirement propabilities
dict_retire = {
    range(0, 74):0.00,
    range(75, 79):0.005,
    range(80, 84):0.005,
    range(85, 89):0.01,
    range(90, 110):0.01
    }

# list of age dependent income increases INDKP106
dict_income_raise = {
    range(20, 24):1107,
    range(25, 29):967,
    range(30, 34):656,
    range(35, 39):509,
    range(40, 44):233,
    range(45, 49):-53,
    range(50, 54):-222,
    range(55, 59):-378,
    range(60, 64):-856,
    range(65, 69):-214,
    range(70, 74):0,
    range(75, 79):0,
    range(80, 84):0,
    range(85, 89):0,
    range(90, 94):0,
    range(95, 99):0,
    range(100, 104):0,
    range(105, 109):0,
}

#print(random.choices(dict_age, k=10))

dict_bin_ages = [
    20, 21,	22,	23,	24,	25,	26,	27,	28,	29,	30,	31,	32,	33,	34,	35,	36,	37,	38,	39,	40,	41,	42,	43,	44,	45,	46,	47,	48,	49,	50,	51,	52,	53,	54,	55,	56,	57,	58,	59,	60,	61,	62,	63,	64,	65,	66,	67,	68,	69,	70,	71,	72,	73,	74,	75,	76,	77,	78,	79,	80,	81,	82,	83,	84,	85,	86,	87,	88,	89,	90,	91,	92,	93,	94,	95,	96,	97,	98,	99,	100,	101,	102,	103,	104,	105,	106,	107,	108,	109,	110,
    ]

dict_bin_ages2 = [20, 22, 24,	26,	28,	30,	32,	34,	36,	38,	40,	42,	44,	46,	48,	50,	52,	54,	56,	58,	60,	62,	64,	66,	68,	70,	72,	74,	76,	78,	80,	82,	84,	86,	88,	90,	92,	94,	96,	98,	100,	102,	104,	106,	108,	110
]