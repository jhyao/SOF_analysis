from .constants import *

all_params_default = {
    Param.PAGE: 1,
    Param.PAGESIZE: 50,
    Param.FROMDATE: None,
    Param.TODATE: None,
    Param.ORDER: Order.DESC,
    Param.MIN: None,
    Param.MAX: None,
    Param.SORT: Sort.REPUTATION,
    Param.SITE: 'stackoverflow'
}
required_default = [Param.ORDER, Param.SORT, Param.SITE]
api_url = 'https://api.stackexchange.com/2.2/'
user_api_url = 'https://api.stackexchange.com/2.2/users'