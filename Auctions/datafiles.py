__author__ = 'eaura'


class AuctionStatus :
    active=0
    due=1
    adjudicated=2
    banned=3

    @classmethod
    def getName(cls,x):
        return {
            0:'Active',
            1 :'Due',
            2:'Adjudicated',
            3: 'Banned',
            }.get(x, 'Active')    # 9 is default if x not found