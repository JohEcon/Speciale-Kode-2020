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