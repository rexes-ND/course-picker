from api.models import *
from api.utils import *

gr = greedy_recommend(20190786)
for i in range(5):
    print(gr[i]['old_code'])
