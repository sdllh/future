'''
自定义的天勤函数
'''
from datetime import date
import time
import re
from tqsdk import TqApi, TqKq, TqAuth, TqBacktest, BacktestFinished, TargetPosTask, tafunc

account = ''
password = ''   

## 下单等待10s后追单，直到全部成交
def open_insert_order_wait(_api, _quote, _direction, _volume,_wait_time, 
                           _method='最新价', _over_price_tick=0):
    """
    开仓下单,可设置挂单方式、超价和等待时间，如果达到等待时间仍没有全部成交，
    则撤单重新挂单,直到全部成交
    Args:
        _api:天勤接口及数据管理类
        _quote:订阅的quote行情对象
        _direction (str): "BUY" 或 "SELL"
        _volume (int): 下单数量(手)
        _wait_time (int): 等待时间(秒)
        _method(str):"市价" / "对价" / "挂价" / "最新价" , 默认最新价
        _over_price_tick(int):超价(跳)， 默认 0 跳
    Returns:
        True: 订单已经全部成交
    """
    print('开仓挂单{0}手'.format(_volume))
    start_time = time.time()  # 秒级
    mysymbol = _quote.underlying_symbol if '@' in _quote.instrument_id \
                    else _quote.instrument_id
    if _direction == 'BUY':
        if _method == '市价':
            myprice = _quote.upper_limit
        elif _method == '对价':
            myprice = _quote.ask_price1 + _quote.price_tick*_over_price_tick
        elif _method == '挂价':
            myprice = _quote.bid_price1 + _quote.price_tick*_over_price_tick
        elif _method == '最新价':
            myprice = _quote.last_price + _quote.price_tick*_over_price_tick
        else:
            print('挂单方式错误，选择:市价/对价/挂价/最新价')
        if myprice > _quote.upper_limit:
            myprice = _quote.upper_limit
        print('挂单价{0}'.format(myprice))
        open_order = _api.insert_order(symbol=mysymbol, direction="BUY", 
                                       offset="OPEN", volume=_volume,
                                       limit_price=myprice)
    elif _direction == 'SELL':
        if _method == '市价':
            myprice = _quote.lower_limit
        elif _method == '对价':
            myprice = _quote.bid_price1 - _quote.price_tick*_over_price_tick
        elif _method == '挂价':
            myprice = _quote.ask_price1 - _quote.price_tick*_over_price_tick
        elif _method == '最新价':
            myprice = _quote.last_price - _quote.price_tick*_over_price_tick
        else:
            print('挂单方式错误，选择:市价/对价/挂价/最新价')
        if myprice < _quote.lower_limit:
            myprice = _quote.lower_limit
        print('挂单价{0}'.format(myprice))
        open_order = _api.insert_order(symbol=mysymbol, direction="SELL",
                                       offset="OPEN", volume=_volume,
                                       limit_price=myprice)
    else:
        print('开仓方向有误，请输入 BUY（做多）  SELL（做空）')

    while True:
        _api.wait_update()
        print("{0}  最新价:{1}".format(_quote.datetime, _quote.last_price))
        if open_order.status == 'FINISHED':  # 全部成交
            print('下单手数{0}  成交{1}   全部成交了'.format(_volume, _volume
                  - open_order.volume_left))
            return True
        elif time.time() < start_time + _wait_time: # 没有全部成交，时间没到
            continue
        else:    # 没有全部成交，时间到
            _api.cancel_order(open_order)
            _api.wait_update()
            print('没有全部成交，时间到,撤单,剩余{0}手'
                  .format(open_order.volume_left))
            open_insert_order_wait(_api, _quote, _direction,
                                   open_order.volume_left, _wait_time,
                                   _method, _over_price_tick)
            return True




## 全部平多单（知乎已发）
def insert_order_close_long(_api, _symbol, _price):
    order_list_long = []
    _position = _api.get_position(_symbol)
    if _position.exchange_id != 'SHFE' and _position.exchange_id != 'INE':
        order = _api.insert_order(symbol=_symbol, direction="SELL",
                                  offset="CLOSE",
                                  volume=_position.pos_long,
                                  limit_price=_price)
        order_list_long.append(order)
    elif _position.pos_long_today == 0 and _position.pos_long_his != 0:
        order = _api.insert_order(symbol=_symbol, direction="SELL",
                                  offset="CLOSE",
                                  volume=_position.pos_long_his,
                                  limit_price=_price)
        order_list_long.append(order)
    elif _position.pos_long_today != 0 and _position.pos_long_his == 0:
        order = _api.insert_order(symbol=_symbol, direction="SELL",
                                  offset="CLOSETODAY",
                                  volume=_position.pos_long_today,
                                  limit_price=_price)
        order_list_long.append(order)
    elif _position.pos_long_today != 0 and _position.pos_long_his != 0:
        order = _api.insert_order(symbol=_symbol, direction="SELL",
                                  offset="CLOSE",
                                  volume=_position.pos_long_his,
                                  limit_price=_price)
        order_list_long.append(order)
        order = _api.insert_order(symbol=_symbol, direction="SELL",
                                  offset="CLOSETODAY",
                                  volume=_position.pos_long_today,
                                  limit_price=_price)
        order_list_long.append(order)
    else:
        print('上期或者能源品种，无多头持仓！')
    return order_list_long


## 全部平空单（知乎已发）
def insert_order_close_short(_api, _symbol, _price):
    order_list_short = []
    _position = _api.get_position(_symbol)
    if _position.exchange_id != 'SHFE' and _position.exchange_id != 'INE':
        order = _api.insert_order(symbol=_symbol, direction="BUY",
                                  offset="CLOSE",
                                  volume=_position.pos_short,
                                  limit_price=_price)
        order_list_short.append(order)
    elif _position.pos_short_today == 0 and _position.pos_short_his != 0:
        order = _api.insert_order(symbol=_symbol, direction="BUY",
                                  offset="CLOSE",
                                  volume=_position.pos_short_his,
                                  limit_price=_price)
        order_list_short.append(order)
    elif _position.pos_short_today != 0 and _position.pos_short_his == 0:
        order = _api.insert_order(symbol=_symbol, direction="BUY",
                                  offset="CLOSETODAY",
                                  volume=_position.pos_short_today,
                                  limit_price=_price)
        order_list_short.append(order)
    elif _position.pos_short_today != 0 and _position.pos_short_his != 0:
        order = _api.insert_order(symbol=_symbol, direction="BUY",
                                  offset="CLOSE",
                                  volume=_position.pos_short_his,
                                  limit_price=_price)
        order_list_short.append(order)
        order = _api.insert_order(symbol=_symbol, direction="BUY",
                                  offset="CLOSETODAY",
                                  volume=_position.pos_short_today,
                                  limit_price=_price)
        order_list_short.append(order)
    else:
        print('上期或者能源品种，无空头持仓！')
    return order_list_short


## 检验是否全平（知乎已发）
def order_is_finished(_order_exit_list):
    order_is_finished_number = 0
    for _order_one in _order_exit_list:
        if _order_one.status == 'FINISHED': 
            order_is_finished_number += 1
    if order_is_finished_number == len(_order_exit_list):
        return True
    return False


# 全部撤单（之前需要有订阅）（知乎已发）
def cancel_all_order(_api):
    order_all = _api.get_order()
    # print('订单数量为：{0}'.format(len(order_all)))
    for k, order in order_all.items():
        if order.status == 'ALIVE':
            _api.cancel_order(order)
    _api.wait_update()


# 撤单并全部平仓（知乎已发）
def cancel_order_close_all_position_now(_api, _symbol, _close_long_price, 
                                        _close_short_price):
    cancel_all_order(_api)
    position = _api.get_position(_symbol)
    if position.pos_long:
        order_close_long = insert_order_close_long(_api, _symbol,
                                                   _close_long_price)
        while True:
            _api.wait_update()
            if order_is_finished(order_close_long):
                break
    if position.pos_short:
        order_close_short = insert_order_close_short(_api, _symbol,
                                                     _close_short_price)
        while True:
            _api.wait_update()
            if order_is_finished(order_close_short):
                break
    return True


# 不同交易所的合约名称规律
# 1.中金所  CFFEX   ：大写字母1-2位+数字4位
# 2.郑商所  CZCE    ：大写字母2位+数字3位
# 3.大商所  DCE     ：小写字母1-2位+数字4位
# 4.能源所  INE     ：小写字母2位+数字4位
# 5.上期所  SHFE    ：小写字母2位+数字4位
## 检验单个合约的命名是否符合天勤的规则（知乎已发）
def examine_one_symbol(_symbol):
    pattern_dict_normal = {
        'CFFEX':re.compile(r'^(CFFEX).([A-Z]{1,2})(\d{4})$'),
        'CZCE': re.compile(r'^(CZCE).([A-Z]{2})(\d{3})$'),
        'DCE': re.compile(r'^(DCE).([a-z]{1,2})(\d{4})$'),
        'INE': re.compile(r'^(INE).([a-z]{2})(\d{4})$'),
        'SHFE':  re.compile(r'^(SHFE).([a-z]{2})(\d{4})$'),
        'KQ.m': re.compile(r'^(KQ.m@)(CFFEX|CZCE|DCE|INE|SHFE).(\w{1,2})$')
        }

    for k,ipattern in pattern_dict_normal.items():
        matchsymbol = ipattern.match(_symbol)
        if matchsymbol:
            exchange,variety,expiry_month = \
                matchsymbol.group(1),matchsymbol.group(2),matchsymbol.group(3)
            return [exchange,variety,expiry_month]
    return False



###  天勤主力合约换月(模拟/实盘/回测)（知乎已发）
def switch_contract(_api, _last_symbol, _today_symbol):
    last_symbol_list = examine_one_symbol(_last_symbol)
    today_symbol_list = examine_one_symbol(_today_symbol)
    if not last_symbol_list or not today_symbol_list:
        print('旧合约/新合约代码有误，请检验')
        return False
    if (today_symbol_list[0] == 'KQ.m@'
        and (today_symbol_list[1] != last_symbol_list[0]
             or today_symbol_list[2] != last_symbol_list[1])):
        print('旧合约/新合约品种不一，请检验')
        return False
    if (today_symbol_list[0] != 'KQ.m@'
        and (today_symbol_list[0] != last_symbol_list[0]
             or today_symbol_list[1] != last_symbol_list[1])):
        print('旧合约/新合约品种不一，请检验')
        return False

    quote = _api.get_quote(symbol = _today_symbol)
    if today_symbol_list[0] == 'KQ.m@':
        _today_symbol = quote.underlying_symbol
    if _today_symbol <= _last_symbol:
        print('新合约并非远月合约，不换月')
        return 'NO'
    else:
        print('合约已切换，进行换月操作')
        position_last_for = _api.get_position(_last_symbol)
        long_last_for = position_last_for.pos_long
        short_last_for = position_last_for.pos_short
        position_new_for = _api.get_position(_today_symbol)
        long_new_for = position_new_for.pos_long
        short_new_for = position_new_for.pos_short

        my_ask_price = quote.upper_limit # quote.ask_price1 + 5
        my_bid_price = quote.lower_limit # quote.bid_price1 - 5

        if long_last_for:
            order_list_long = insert_order_close_long(_api, _last_symbol,
                                                      my_bid_price)
            order_long = _api.insert_order(symbol=_today_symbol, 
                                           direction="BUY",
                                           offset="OPEN",
                                           volume=long_last_for,
                                           limit_price=my_ask_price)
            while True:
                _api.wait_update()
                if (order_is_finished(order_list_long)
                        and order_long.status == 'FINISHED'):
                    break
        if short_last_for:
            order_list_short = insert_order_close_short(_api, _last_symbol,
                                                        my_ask_price)
            order_short = _api.insert_order(symbol=_today_symbol,
                                            direction="SELL",
                                            offset="OPEN",
                                            volume=short_last_for,
                                            limit_price=my_bid_price)
            while True:
                _api.wait_update()
                if (order_is_finished(order_list_short)
                        and order_short.status == 'FINISHED'):
                    break

        position_last_aft = _api.get_position(_last_symbol)
        long_last_aft = position_last_aft.pos_long
        short_last_aft = position_last_aft.pos_short
        position_new_aft = _api.get_position(_today_symbol)
        long_new_aft = position_new_aft.pos_long
        short_new_aft = position_new_aft.pos_short
        print('合约换月完成! 旧合约{0}，换月前，多头{1}手，空头{2}手。\
               换月后，多头{3}手，空头{4}手'
               .format(_last_symbol, long_last_for, short_last_for,
                       long_last_aft, short_last_aft))
        print('新合约{0}，换月前，多头{1}手，空头{2}手。\
               换月后，多头{3}手，空头{4}手。'\
               .format(_today_symbol, long_new_for, short_new_for,
                       long_new_aft, short_new_aft))
        return 'YES'


# 计算出一个价格，可能有小数点，获取离这个价格最近的可挂单价格，或者向上取，向下取
def get_order_price_up_down(_real_price, _tick, _method = 'NEAR'):
    if _real_price % _tick == 0: 
        return _real_price

    price_datum = int(_real_price - 10*_tick)
    while True:
        if _real_price > price_datum + _tick:
            price_datum += _tick
        else:
            price_down = price_datum
            price_up = price_datum + _tick
            if _method == 'UP':
                return price_up
            elif _method == 'DOWN':
                return price_down
            elif _method == 'NEAR':
                if _real_price - price_down < price_up - _real_price:
                    return price_down
                else:
                    return price_up




def get_all_symbol_dict():
    all_symbol_future={}
    all_symbol_future['IC']=['CFFEX','中证500指数']
    all_symbol_future['IF']=['CFFEX','沪深300指数']
    all_symbol_future['IH']=['CFFEX','上证50指数']
    all_symbol_future['T']=['CFFEX','10年期国债']
    all_symbol_future['TF']=['CFFEX','5年期国债']
    all_symbol_future['TS']=['CFFEX','2年期国债']
    all_symbol_future['IO']=['CFFEX','沪深300股指期权']

    all_symbol_future['AP']=['CZCE','苹果']
    all_symbol_future['CF']=['CZCE','一号棉花']
    all_symbol_future['CJ']=['CZCE','红枣']
    all_symbol_future['CY']=['CZCE','棉纱']
    all_symbol_future['FG']=['CZCE','玻璃']
    all_symbol_future['JR']=['CZCE','粳稻']
    all_symbol_future['LR']=['CZCE','晚籼稻']
    all_symbol_future['MA']=['CZCE','甲醇']
    all_symbol_future['OI']=['CZCE','菜籽油']
    all_symbol_future['PF']=['CZCE','短纤']
    all_symbol_future['PK']=['CZCE','花生仁']
    all_symbol_future['PM']=['CZCE','普通小麦']
    all_symbol_future['RI']=['CZCE','早籼稻']
    all_symbol_future['RM']=['CZCE','菜籽粕']
    all_symbol_future['RS']=['CZCE','油菜籽']
    all_symbol_future['SA']=['CZCE','纯碱']
    all_symbol_future['SF']=['CZCE','硅铁']
    all_symbol_future['SM']=['CZCE','锰硅']
    all_symbol_future['SR']=['CZCE','白砂糖']
    all_symbol_future['TA']=['CZCE','精对苯二甲酸']
    all_symbol_future['UR']=['CZCE','尿素']
    all_symbol_future['WH']=['CZCE','优质强筋小麦']
    all_symbol_future['ZC']=['CZCE','动力煤']

    all_symbol_future['a']=['DCE','黄大豆1号']
    all_symbol_future['b']=['DCE','黄大豆2号']
    all_symbol_future['bb']=['DCE','胶合板']
    all_symbol_future['c']=['DCE','黄玉米']
    all_symbol_future['cs']=['DCE','玉米淀粉']
    all_symbol_future['eb']=['DCE','苯乙烯']
    all_symbol_future['eg']=['DCE','乙二醇']
    all_symbol_future['fb']=['DCE','纤维板']
    all_symbol_future['i']=['DCE','铁矿石']
    all_symbol_future['j']=['DCE','冶金焦炭']
    all_symbol_future['jd']=['DCE','鸡蛋']
    all_symbol_future['jm']=['DCE','焦煤']
    all_symbol_future['l']=['DCE','线型低密度聚乙烯']
    all_symbol_future['lh']=['DCE','生猪']
    all_symbol_future['m']=['DCE','豆粕']
    all_symbol_future['p']=['DCE','棕榈油']
    all_symbol_future['pg']=['DCE','液化石油气']
    all_symbol_future['pp']=['DCE','聚丙烯']
    all_symbol_future['rr']=['DCE','粳米']
    all_symbol_future['v']=['DCE','聚氯乙烯']
    all_symbol_future['y']=['DCE','豆油']

    all_symbol_future['bc']=['INE','国际铜']
    all_symbol_future['lu']=['INE','低硫燃料油']
    all_symbol_future['nr']=['INE','20号胶']
    all_symbol_future['sc']=['INE','原油']

    all_symbol_future['ag']=['SHFE','白银']
    all_symbol_future['al']=['SHFE','铝']
    all_symbol_future['au']=['SHFE','黄金']
    all_symbol_future['bu']=['SHFE','石油沥青']
    all_symbol_future['cu']=['SHFE','铜']
    all_symbol_future['fu']=['SHFE','燃料油']
    all_symbol_future['hc']=['SHFE','热轧卷板']
    all_symbol_future['ni']=['SHFE','镍']
    all_symbol_future['pb']=['SHFE','铅']
    all_symbol_future['rb']=['SHFE','螺纹钢']
    all_symbol_future['ru']=['SHFE','天然橡胶']
    all_symbol_future['sn']=['SHFE','锡']
    all_symbol_future['sp']=['SHFE','漂针浆']
    all_symbol_future['ss']=['SHFE','不锈钢']
    all_symbol_future['wr']=['SHFE','线材']
    all_symbol_future['zn']=['SHFE','锌']
    return all_symbol_future




