# author: HRH

# date: 2022/3/7

# PyCharm
from utils.decorator.sql import connectAndDisconnect
@connectAndDisconnect
def test(db):
    assert db is not None
    print(type(db))
    cs=db.cursor()
    assert cs is not None

test()