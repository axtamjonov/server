from loader import dp
from .admin import isAdmin, isStr

if __name__==("filters"):
    dp.filters_factory.bind(isAdmin)