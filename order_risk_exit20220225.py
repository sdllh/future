from tqsdk import tafunc
import time
from tqsdk.ta import ATR
import sys
import numbers
import pandas as pd
import numpy as np
import time
import hongyuan_ABC_func as ABC
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)


class Parameters():
    def __init__(self, _public_para):
        # 主程序参数
        self.account =  _public_para['参数'].loc['天勤账号']
        self.password =  _public_para['参数'].loc['天勤密码']
        self.api_select =  _public_para['参数'].loc['启动模式']
        self.symbol =  _public_para['参数'].loc['合约名称']
        self.margin_rate =  _public_para['参数'].loc['保证金比例']
        # 风控
        self.max_loss_ratio =  _public_para['参数'].loc['单日最大亏损比例']
        self.available_funds_ratio_high =  _public_para['参数'].loc['可用资金占比高']
        self.available_funds_ratio_low =  _public_para['参数'].loc['可用资金占比低']
        self.close_time_afternoon_hour =  _public_para['参数'].loc['下午平仓时间小时']
        self.close_time_afternoon_minute =  _public_para['参数'].loc['下午平仓时间分钟']
        self.close_time_evening_hour =  _public_para['参数'].loc['晚上平仓时间小时']
        self.close_time_evening_minute =  _public_para['参数'].loc['晚上平仓时间分钟']
        # 开仓
        self.open_k_period_s =  _public_para['参数'].loc['开仓k线周期_秒']
        self.open_k_number = _public_para['参数'].loc['开仓k线数量']
        self.open_times = _public_para['参数'].loc['开仓次数']
        # 订单
        self.open_position_select = int(_public_para['参数'].loc['开仓手数选择'])
        self.open_position_1_position = _public_para['参数'].loc['开仓手数1仓位']
        self.open_position_2_loss = _public_para['参数'].loc['开仓手数2亏损量']
        self.open_position_2_k_number = _public_para['参数'].loc['开仓手数2k线数量']
        self.open_position_2_ATR_k_number = _public_para['参数'].loc['开仓手数2ATRk线数量']
        self.open_position_2_ATR_ratio = _public_para['参数'].loc['开仓手数2倍数']

        self.open_rule_1_long = _public_para['参数'].loc['开仓规则1做多参照']
        self.open_rule_1_long_overprice_tick = _public_para['参数'].loc['开仓规则1做多超价']
        self.open_rule_1_short = _public_para['参数'].loc['开仓规则1做空参照']
        self.open_rule_1_short_overprice_tick = _public_para['参数'].loc['开仓规则1做空超价']
        self.increase_rule_1_long = _public_para['参数'].loc['加仓规则1做多参照']
        self.increase_rule_1_long_overprice_tick = _public_para['参数'].loc['加仓规则1做多超价']
        self.increase_rule_1_short = _public_para['参数'].loc['加仓规则1做空参照']
        self.increase_rule_1_short_overprice_tick = _public_para['参数'].loc['加仓规则1做空超价']

        self.exit_rule_1_long = _public_para['参数'].loc['平仓规则1多头参照']
        self.exit_rule_1_long_overprice_tick = _public_para['参数'].loc['平仓规则1多头超价']
        self.exit_rule_1_short = _public_para['参数'].loc['平仓规则1空头参照']
        self.exit_rule_1_short_overprice_tick = _public_para['参数'].loc['平仓规则1空头超价']
        self.exit_2_low_level_tick = _public_para['参数'].loc['平仓规则2极端下水位线']
        self.exit_2_high_level_tick = _public_para['参数'].loc['平仓规则2极端上水位线']
        self.wait_time_seconds = _public_para['参数'].loc['开仓加仓平仓等待时间']
        # 退出

        # 有下划线 ‘_’表示退出策略不唯一 ，没有下划线 ‘_’表示退出策略唯一
        if '_' in str(_public_para['参数'].loc['退出策略选择']):
            self.my_exit_method =  _public_para['参数'].loc['退出策略选择'].split('_')
            self.my_exit_method = [ int(i) for i in self.my_exit_method]
        else:
            self.my_exit_method =  [_public_para['参数'].loc['退出策略选择']]
        self.exit_1_k_number =  _public_para['参数'].loc['移动退出1k线数量']
        self.exit_2_ma =  _public_para['参数'].loc['移动退出2ma']
        self.exit_2_ATR_k_number =  _public_para['参数'].loc['移动退出2ATRk线数量']
        self.exit_2_ATR_ratio =  _public_para['参数'].loc['移动退出2ATR比例']
        self.exit_move_select =  _public_para['参数'].loc['移动退出启动时机']

        self.exit_3_k_number =  _public_para['参数'].loc['固定退出3k线数量']
        self.exit_4_ATR_k_number =  _public_para['参数'].loc['固定退出4ATRk线数量']
        self.exit_4_ATR_ratio =  _public_para['参数'].loc['固定退出4ATR比例']
        # 加仓
        self.increase_strategy_select =  _public_para['参数'].loc['加仓策略选择']
        self.increase_1_ATR_k_number =  _public_para['参数'].loc['加仓1ATRk线数量']
        self.increase_1_cell_number =  _public_para['参数'].loc['加仓1格子数量']
        self.increase_1_adjust_ratio =  _public_para['参数'].loc['加仓1调整比例']
        self.increase_1_exit_ratio =  _public_para['参数'].loc['加仓1退出比例']
        self.increase_1_last_adjust_ratio =  _public_para['参数'].loc['加仓1倒数一格调整比例']
        self.increase_1_last_profit_ratio =  _public_para['参数'].loc['加仓1倒数一格盈利比例']
        self.increase_1_last_exit_ratio =  _public_para['参数'].loc['加仓1倒数两格退出比例']

        self.increase_2_ATR_k_number =  _public_para['参数'].loc['加仓2ATRk线数量']
        self.increase_2_adjust_ratio =  _public_para['参数'].loc['加仓2调整比例']
        self.increase_2_increase_ratio =  _public_para['参数'].loc['加仓2加仓比例']
        self.increase_2_increase_exit_ratio_x =  _public_para['参数'].loc['加仓2加仓后退出点x']
        self.increase_2_increase_exit_ratio_y =  _public_para['参数'].loc['加仓2加仓后退出点y']
        self.increase_2_exit_ratio =  _public_para['参数'].loc['加仓2退出比例']
        self.increase_2_last_adjust_ratio =  _public_para['参数'].loc['加仓2倒数一格调整比例']
        self.increase_2_last_profit_ratio =  _public_para['参数'].loc['加仓2倒数一格盈利比例']
        self.increase_2_last_exit_ratio =  _public_para['参数'].loc['加仓2倒数两格退出比例']
        self.increase_3_ATR_k_number =  _public_para['参数'].loc['加仓3ATRk线数量']
        self.increase_3_first_ATR_ratio =  _public_para['参数'].loc['加仓3首次加仓间隔倍数']
        self.increase_3_next_ATR_ratio =  _public_para['参数'].loc['加仓3后次加仓间隔倍数']
        self.increase_3_eixt_ATR_ratio =  _public_para['参数'].loc['加仓3止损间隔倍数']
        self.increase_3_all_increase_times =  _public_para['参数'].loc['加仓3加仓总次数']
        self.increase_3_modify_exit_strategy =  _public_para['参数'].loc['加仓3加仓几次调整退出策略']


class  Order(Parameters):
    # def __init__(self, _public_para):
    #     Parameter.__init__(self, _public_para)

    def get_open_shoushu(self,_quote, _klines, _direstion):
        # 如果选用方式1，直接返回固定的开仓手数
        if self.open_position_select == 1:
            return self.open_position_1_position
        # 如果选用方式2，需要计算，手数取小
        elif self.open_position_select == 2:
            # 计算最新价与前几根k线的差值（分做多做空）
            shou_shu_a = 9999
            if _direstion == 'BUY':
                chazhi = _quote.last_price - min(_klines['low'][-(self.open_position_2_k_number + 1) : -1])
            elif _direstion == 'SELL':
                chazhi = max(_klines['high'][-(self.open_position_2_k_number + 1) : -1]) - _quote.last_price
            
            # 如果差值>0, 为正常情况，如果差值<=0，直接用方案b
            if chazhi > 0:
                shou_shu_a = self.open_position_2_loss / (chazhi * _quote.volume_multiple)
            
            atr = ATR(_klines, self.open_position_2_ATR_k_number)
            shou_shu_b = self.open_position_2_loss / (self.open_position_2_ATR_ratio * atr['atr'].iloc[-1] * _quote.volume_multiple)    
            # 手数取小，仅仅取整数部分（注意：有可能为0）
            shou_shu = int(min(shou_shu_a,shou_shu_b))
            return shou_shu

# order_open , start_time = myorder.open_insert_order(_api, _symbol, _quote, _direction, _shou_shu)
    def open_insert_order(self, _api, _quote, _direction, _shou_shu):
        start_time = time.time()  # 秒级
        if _direction == 'BUY':
            if self.open_rule_1_long == '卖一':
                myprice = _quote.ask_price1 + self.open_rule_1_long_overprice_tick * _quote.price_tick
            elif self.open_rule_1_long == '最新价':
                myprice = _quote.last_price + self.open_rule_1_long_overprice_tick * _quote.price_tick
            elif self.open_rule_1_long == '涨停价':
                myprice = _quote.upper_limit   
            else:
                print('开仓下单规则错误，请输入卖一/最新价/涨停价')
            
            if myprice > _quote.upper_limit:
                myprice = _quote.upper_limit
                print('做多时挂单价大于涨停价，以涨停价挂单')
            order_open = _api.insert_order(symbol= _quote.instrument_id , direction="BUY", offset="OPEN",\
                volume= _shou_shu, limit_price = myprice)
        elif _direction == 'SELL':
            if self.open_rule_1_short == '买一':
                myprice = _quote.bid_price1 - self.open_rule_1_short_overprice_tick * _quote.price_tick
            elif self.open_rule_1_short == '最新价':
                myprice = _quote.last_price - self.open_rule_1_short_overprice_tick * _quote.price_tick
            elif self.open_rule_1_short == '跌停价':
                myprice = _quote.lower_limit    
            else:
                print('开仓下单规则错误，请输入买一/最新价/跌停价')

            if myprice < _quote.lower_limit:
                myprice = _quote.lower_limit
                print('做空时挂单价小于跌停价，以跌停价挂单')         
            order_open = _api.insert_order(symbol= _quote.instrument_id , direction="SELL", offset="OPEN",\
                volume= _shou_shu, limit_price = myprice)
        else:
            print('开仓方向有误，请输入BUY（做多）  SELL（做空）')
        return order_open, start_time


# 注意订单状态是在  wait_update  中变化，此为单次检验
# myorder.open_order_examine(order_open, start_time)
    def open_order_is_finished(self, _api, _order_open, _start_time, _direction):
        if _order_open.status == 'FINISHED':  # 全部成交
            if _direction == 'BUY':
                return 'wait_close_or_increase_long',_order_open.volume_orign 
            elif _direction == 'SELL':
                return 'wait_close_or_increase_short',_order_open.volume_orign 

        elif time.time() < _start_time + self.wait_time_seconds: # 没有全部成交，时间没到
            if _direction == 'BUY':
                return 'wait_open_order_finish_long',0   
            elif _direction == 'SELL':
                return 'wait_open_order_finish_short',0  
        else:    # 没有全部成交，时间到
            shoushu_finished = _order_open.volume_orign - _order_open.volume_left
            if shoushu_finished:
                _api.cancel_order(_order_open)
                if _direction == 'BUY':
                    return 'wait_close_or_increase_long',shoushu_finished
                elif _direction == 'SELL':
                    return 'wait_close_or_increase_short',shoushu_finished
            else:
                _api.cancel_order(_order_open)
                return  'wait_open',0          


# order_increase , start_time = myorder.increase_insert_order(_api, _symbol, _quote, _direction, _shou_shu)
    def increase_insert_order(self, _api, _quote, _direction, _shou_shu):
        start_time = time.time()  # 秒级
        if _direction == 'BUY':
            if self.increase_rule_1_long == '卖一':
                myprice = _quote.ask_price1 + self.increase_rule_1_long_overprice_tick * _quote.price_tick
            elif self.increase_rule_1_long == '最新价':
                myprice = _quote.last_price + self.increase_rule_1_long_overprice_tick * _quote.price_tick
            elif self.increase_rule_1_long == '涨停价':
                myprice = _quote.upper_limit   
            else:
                print('加仓下单规则错误，请输入卖一/最新价/涨停价')

            if myprice > _quote.upper_limit:
                myprice = _quote.upper_limit
                print('加仓（多）时挂单价大于涨停价，以涨停价挂单')
            order_increase = _api.insert_order(symbol= _quote.instrument_id , direction="BUY", offset="OPEN",\
                volume= _shou_shu, limit_price = myprice)
        elif _direction == 'SELL':
            if self.increase_rule_1_short == '买一':
                myprice = _quote.bid_price1 - self.increase_rule_1_short_overprice_tick * _quote.price_tick
            elif self.increase_rule_1_short == '最新价':
                myprice = _quote.last_price - self.increase_rule_1_short_overprice_tick * _quote.price_tick
            elif self.increase_rule_1_short == '跌停价':
                myprice = _quote.lower_limit       
            else:
                print('加仓下单规则错误，请输入买一/最新价/跌停价')

            if myprice < _quote.lower_limit:
                myprice = _quote.lower_limit
                print('加仓（空）时挂单价小于跌停价，以跌停价挂单')        
            order_increase = _api.insert_order(symbol= _quote.instrument_id , direction="SELL", offset="OPEN",\
                volume= _shou_shu, limit_price = myprice)
        else:
            print('加仓方向有误，请输入.....')
        return order_increase, start_time


# 注意订单状态是在  wait_update  中变化，此为单次检验
# myorder.increase_order_examine(order_increase, start_time)
    def increase_order_is_finished(self, _api, _quote,_direction, _order_increase, _start_time):
        if _order_increase.status == 'FINISHED':   # 全部成交
            if _direction == 'BUY':
                return 'wait_close_or_increase_long'
            elif _direction == 'SELL':
                return 'wait_close_or_increase_short'
        elif time.time() - _start_time < self.wait_time_seconds: # 没有全部成交，时间没到
            if _direction == 'BUY':
                return 'wait_increase_order_finish_long'
            elif _direction == 'SELL':
                return 'wait_increase_order_finish_short'
        else:  # 没有全部成交，时间到
            shou_shu = _order_increase.volume_left
            _api.cancel_order(_order_increase)
            _order_increase , _start_time = self.increase_insert_order(_api, _quote, _direction, shou_shu)
            self.increase_order_is_finished(_api, _quote,_direction, _order_increase, _start_time)


    def exit_insert_order(self, _api, _quote, _direction, _position):
        start_time = time.time()  # 秒级
        # 多头卖平
        if _direction == 'SELL':
            # 获取挂单价格
            if self.exit_rule_1_long == '买一':
                myprice = _quote.bid_price1 - self.exit_rule_1_long_overprice_tick * _quote.price_tick
            elif self.exit_rule_1_long == '最新价':
                myprice = _quote.last_price - self.exit_rule_1_long_overprice_tick * _quote.price_tick
            elif self.exit_rule_1_long == '跌停价':
                myprice = _quote.lower_limit   
            else:
                print('退出下单规则错误，请输入买一/最新价/跌停价')

            if myprice < _quote.lower_limit:
                myprice = _quote.lower_limit
                print('多头平仓时挂单价小于跌停价，以跌停价挂单')

            order_exit_list = ABC.insert_order_close_long(_api, _quote.instrument_id, myprice)

            return order_exit_list, start_time
        # 空头平仓
        elif _direction == 'BUY':
            # 获取挂单价格
            if self.exit_rule_1_short == '卖一':
                myprice = _quote.ask_price1 + self.exit_rule_1_short_overprice_tick * _quote.price_tick
            elif self.exit_rule_1_short == '最新价':
                myprice = _quote.last_price + self.exit_rule_1_short_overprice_tick * _quote.price_tick
            elif self.exit_rule_1_short == '涨停价':
                myprice = _quote.upper_limit       
            else:
                print('退出下单规则错误，请输入卖一/最新价/涨停价')

            if myprice > _quote.upper_limit:
                myprice = _quote.upper_limit
                print('空头平仓时挂单价大于涨停价，以涨停价挂单')

            order_exit_list = ABC.insert_order_close_short(_api, _quote.instrument_id, myprice)

            return order_exit_list, start_time
        else:
            print('平仓函数传入的买卖方向有误！ 1表示空头买平，-1表示多头卖平')
        return 'ERROR'



    def exit_order_is_finished(self, _api, _quote, _direction, _position, _order_exit_list, _start_time):
        order_is_finished_number = 0
        for _order_one in _order_exit_list:
            if _order_one.status == 'FINISHED': order_is_finished_number += 1
        if order_is_finished_number == len(_order_exit_list):   # 所有订单全部成交，订单结束
            return 'wait_open'
        elif time.time() - _start_time < self.wait_time_seconds:  # 没有全部成交，普通情况下时间没到
            if _direction == 'BUY':
                return 'wait_exit_order_finish_long'
            elif _direction == 'SELL':
                return 'wait_exit_order_finish_short'
        else:     # 没有全部成交，普通情况下时间到了,撤单，重新判断情况进行挂单
            for _order_one in _order_exit_list:
                if _order_one.status == 'ALIVE': _api.cancel_order(_order_one)
            _order_exit_list, _start_time = self.exit_insert_order(_api, _quote, _direction, _position)
            self.exit_order_is_finished(_api, _quote, _direction, _position, _order_exit_list, _start_time)


class  Risk(Parameters):
    # def __init__(self, _public_para):
    #     Parameter.__init__(self, _public_para)

    # 开仓/加仓之前进行判断：如果本交易日的亏损达到总金额的一定比例，就不能开仓/加仓了
    #  can_open_or_increase_1 = myrisk.today_profit_loss_risk_manage(account) 
    def today_profit_loss_risk_manage(self, _account):
        self.today_profit_loss = _account.position_profit + _account.close_profit  # 今日盈亏
        if self.today_profit_loss < 0 and abs(self.today_profit_loss / _account.static_balance) > self.max_loss_ratio:
            return False  
        return True

    # 开仓/加仓之前进行判断：如果开仓前可用资金低于总资金的一定比例，不可以开仓/加仓
    #  can_open_or_increase_2 = myrisk.available_manage_1(account) 
    def available_manage_1(self, _account):
        if _account.available < _account.static_balance * self.available_funds_ratio_high:
            return False
        return True

    # 开仓/加仓之前进行判断：如果开仓后可用资金低于总资金的一定比例，不可以开仓/加仓
    #  can_open_or_increase_3 = myrisk.available_manage_2(account) 
    def available_manage_2(self, _account, _quote, _shou_shu, _margin_rate):
        _now_margin = _shou_shu * _quote.last_price * _quote.volume_multiple * _margin_rate
        if _account.available - _now_margin < _account.static_balance * self.available_funds_ratio_low:
            return False  
        return True



class  Exit(Parameters):
    def __init__(self):
        # Parameter.__init__(self, _public_para)
        # --------------------------------------退出策略分类 --------------------------------
        # 将所有的退出策略分为 移动 固定 2 类
        self.all_exit_method_move = [1, 2]
        self.all_exit_method_fixed = [3, 4] 

        # 将我的退出策略与退出策略（移动，固定）分别取交集，获得我的（移动，固定）退出策略
        self.my_exit_method_move = list(set(self.all_exit_method_move) & set(self.my_exit_method))
        self.my_exit_method_fixed = list(set(self.all_exit_method_fixed) & set(self.my_exit_method))
        print('我的退出策略是{0}'.format(self.my_exit_method))
        print('我的移动退出策略为{0}'.format(self.my_exit_method_move))
        print('我的固定退出策略为{0}'.format(self.my_exit_method_fixed))
        # 策略中至少有1个固定退出策略，若没有，则停止程序
        if not self.my_exit_method_fixed:
            message = '没有固定退出方式，策略停止执行!!!!!!'
            print(message)
            # logging.warning(message)
            # send_email.send_emails('停止!',message)
            time.sleep(10)
            sys.exit(0)

        # 定义做多时的退出策略字典，可以根据退出策略参数选择对应的退出函数
        self.exit_dict_long={1:self.get_exit_1_long, 2:self.get_exit_2_long,\
                             3:self.get_exit_3_long, 4:self.get_exit_4_long} 
        self.increase_dict_long={ 1:self.get_increase_1_long, 2:self.get_increase_2_long,\
                                  3:self.get_increase_3_long } 

        # 定义做空时的退出策略字典，可以根据退出策略参数选择对应的退出函数
        self.exit_dict_short={1:self.get_exit_1_short, 2:self.get_exit_2_short,\
                             3:self.get_exit_3_short, 4:self.get_exit_4_short} 
        self.increase_dict_short={ 1:self.get_increase_1_short, 2:self.get_increase_2_short,\
                                  3:self.get_increase_3_short} 

        # --------------------------以下参数在平仓后需要 重新设置为0/[]-----------------------------
        # self.can_open_symbol = 0
        # self.open_price = []
        # self.old_price = []
        # self.high_track = []
        # self.low_track = []
        # self.middle_track = []  #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        self.exit_1 = []
        self.exit_2 = []
        self.exit_3 = [] 
        self.exit_4 = []   

        self.increase_1 = [] 
        self.increase_1_last = []
        self.increase_1_ATR = []
        self.increase_1_position_now = 1

        self.increase_2 = [] 
        self.increase_2_last = [] 
        self.increase_2_ATR = []
        self.increase_2_position_now = 1
        self.increase_2_exit_after_increase = []
        self.increase_2_cell_number = []

        self.increase_3 = [] 
        self.increase_3_ATR = []
        self.increase_3_increase_list = []
        self.increase_3_exit_list = []
        self.increase_3_position_now = 0
        self.increase_3_position_last = 0
        
        self.increase_already_increase_number = 0


    # --------------------------------如果是极端行情，那么直接退出---------------------------------------
    def examine_extreme_market(self, _api, _quote, _position):
        if _position.pos_long and \
            _quote.last_price < _quote.lower_limit + self.exit_2_low_level_tick * _quote.price_tick:
            order_list = ABC.insert_order_close_long(_api, _quote.instrument_id,_quote.lower_limit)
            while True:
                _api.wait_update()
                if ABC.order_is_finished(order_list):
                    print('平仓订单全部成交，退出')
                    break
                print('平仓订单还没有全部成交，再等会')
        if _position.pos_short and \
            _quote.last_price > _quote.upper_limit - self.exit_2_high_level_tick * _quote.price_tick:
            order_list = ABC.insert_order_close_short(_api, _quote.instrument_id,_quote.upper_limit)
            while True:
                _api.wait_update()
                if ABC.order_is_finished(order_list):
                    print('平仓订单全部成交，退出')
                    break
                print('平仓订单还没有全部成交，再等会')



    # --------------------------------下面是做多后的退出策略--------------------------------------------
    def get_exit_1_long(self, _klines):
        self.exit_1 = min(_klines['low'][ -(self.exit_1_k_number): -1])
        return self.exit_1
        
    def get_exit_2_long(self, _klines):
        ma = tafunc.ma(_klines.close, self.exit_2_ma)
        atr = ATR(_klines, self.exit_2_ATR_k_number)
        self.exit_2 = ma.iloc[-2] - atr['atr'].iloc[-2] * self.exit_2_ATR_ratio
        return self.exit_2

    def get_exit_3_long(self, _klines):
        if self.exit_3 == []:
            self.exit_3 = min(_klines['low'][ -(self.exit_3_k_number): -1])
        return self.exit_3
        
    def get_exit_4_long(self, _klines):
        if self.exit_4 == []:
            atr = ATR(_klines, self.exit_4_ATR_k_number)
            self.exit_4 = self.open_price - atr['atr'].iloc[-1] * self.exit_4_ATR_ratio
        return self.exit_4

    # --------------------------------下面是做空后的退出策略--------------------------------------------
    def get_exit_1_short(self, _klines):
        self.exit_1 = max(_klines['high'][ -(self.exit_1_k_number): -1])
        return self.exit_1
        
    def get_exit_2_short(self, _klines):
        ma = tafunc.ma(_klines.close, self.exit_2_ma)
        atr = ATR(_klines, self.exit_2_ATR_k_number)
        self.exit_2 = ma.iloc[-2] + atr['atr'].iloc[-2] * self.exit_2_ATR_ratio
        return self.exit_2

    def get_exit_3_short(self, _klines):
        if self.exit_3 == []:
            self.exit_3 = max(_klines['high'][ -(self.exit_3_k_number): -1])
        return self.exit_3
        
    def get_exit_4_short(self, _klines):
        if self.exit_4 == []:
            atr = ATR(_klines, self.exit_4_ATR_k_number)
            self.exit_4 = self.open_price + atr['atr'].iloc[-1] * self.exit_4_ATR_ratio
        return self.exit_4


    # --------------------------------下面是做多后的加仓策略--------------------------------------------

# 本格下部 ： self.open_price + _quote.price_tick + \
# self.increase_1_ATR * (self.increase_1_position_now - 1)

# 上格下部 ： self.open_price + _quote.price_tick + \
# self.increase_1_ATR * (self.increase_1_position_now - 2)

    def get_increase_1_long(self, _quote, _klines):
        if self.increase_1_ATR == []:
            self.increase_1_ATR = ATR(_klines, self.increase_1_ATR_k_number)['atr'].iloc[-1]

        self.increase_1_position_now = (_quote.last_price - self.open_price - _quote.price_tick) // self.increase_1_ATR
        self.increase_1_position_now = int(self.increase_1_position_now  +  1)

        benge_low =  self.open_price + _quote.price_tick + self.increase_1_ATR * (self.increase_1_position_now - 1)
        shangge_low = self.open_price + _quote.price_tick + self.increase_1_ATR * (self.increase_1_position_now - 2)
        # 亏损了
        if self.increase_1_position_now <= 0:
            if self.increase_1_last == []:     # 一开始就亏损，将退出价设置设置为 0 
                self.increase_1_last = 0
                return self.increase_1_last
            else:
                return self.increase_1_last    # 之前已经计算过退出价，直接返回退出价 
        # 首个格子
        elif self.increase_1_position_now == 1:
            if _quote.last_price >= self.open_price + _quote.price_tick + self.increase_1_ATR * self.increase_1_adjust_ratio:
                self.increase_1 = max(self.increase_1_last, benge_low)
                self.increase_1_last = self.increase_1
                return self.increase_1
            else:
                return  self.increase_1_last   
        # 最后一个格子
        elif self.increase_1_position_now >= self.increase_1_cell_number:
            if _quote.last_price >= benge_low + self.increase_1_ATR * self.increase_1_last_profit_ratio:
                return 'exit_long'
            elif _quote.last_price >= benge_low + self.increase_1_ATR * self.increase_1_last_adjust_ratio:
                self.increase_1 = max(self.increase_1_last, benge_low)
                self.increase_1_last = self.increase_1
                return self.increase_1
            else:
                self.increase_1 = max(self.increase_1_last, shangge_low + self.increase_1_ATR * self.increase_1_last_exit_ratio)
                self.increase_1_last = self.increase_1
                return self.increase_1
        # 偶数加仓格子
        elif self.increase_1_position_now % 2 == 0:
            if _quote.last_price >= benge_low + self.increase_1_ATR * self.increase_1_adjust_ratio:
                if self.increase_already_increase_number < self.increase_1_position_now // 2: 
                    self.increase_1 = max(self.increase_1_last, benge_low)
                    self.increase_1_last = self.increase_1
                    self.increase_already_increase_number += 1
                    return 'increase_long'
                else:
                    self.increase_1 = max(self.increase_1_last, benge_low)
                    self.increase_1_last = self.increase_1
                    return self.increase_1
            else:
                self.increase_1 = max(self.increase_1_last, shangge_low + self.increase_1_ATR * self.increase_1_exit_ratio)
                self.increase_1_last = self.increase_1
                return self.increase_1
        # 奇数不加仓格子
        elif self.increase_1_position_now % 2 == 1:
            if _quote.last_price >= benge_low + self.increase_1_ATR * self.increase_1_adjust_ratio:
                self.increase_1 = max(self.increase_1_last, benge_low)
                self.increase_1_last = self.increase_1
                return self.increase_1
            else:
                self.increase_1 = max(self.increase_1_last, shangge_low + self.increase_1_ATR * self.increase_1_exit_ratio)
                self.increase_1_last = self.increase_1
                return self.increase_1


    def get_increase_2_long(self, _quote, _klines):
        if self.increase_2_ATR == []:
            self.increase_2_ATR = ATR(_klines, self.increase_2_ATR_k_number)['atr'].iloc[-1]
            # 获取格子总数
            for i in range(2,41,2):
                if self.increase_2_increase_exit_ratio_x + (i - 1) * self.increase_2_increase_exit_ratio_y >= 1: 
                    self.increase_2_cell_number = i
                    break

        self.increase_2_position_now = (_quote.last_price - self.open_price - _quote.price_tick) // self.increase_2_ATR
        self.increase_2_position_now = int(self.increase_2_position_now  +  1)

        benge_low =  self.open_price + _quote.price_tick + self.increase_2_ATR * (self.increase_2_position_now - 1)
        shangge_low = self.open_price + _quote.price_tick + self.increase_2_ATR * (self.increase_2_position_now - 2)
        # 亏损了
        if self.increase_2_position_now <= 0:
            if self.increase_2_last == []:     # 一开始就亏损，将退出价设置设置为 0 
                self.increase_2_last = 0
                return self.increase_2_last
            else:
                return self.increase_2_last    # 之前已经计算过退出价，直接返回退出价 
        # 首个格子
        elif self.increase_2_position_now == 1:
            if _quote.last_price >= self.open_price + _quote.price_tick + self.increase_2_ATR * self.increase_2_adjust_ratio:
                self.increase_2 = max(self.increase_2_last, benge_low)
                self.increase_2_last = self.increase_2
                return self.increase_2
            else:
                if self.increase_2_last == []:    
                    self.increase_2_last = 0
                    return self.increase_2_last 
                else:
                    return self.increase_2_last    
        # 最后一个格子
        elif self.increase_2_position_now >= self.increase_2_cell_number:
            if _quote.last_price >= benge_low + self.increase_2_ATR * self.increase_2_last_profit_ratio:
                return 'exit_long'
            elif _quote.last_price >= benge_low + self.increase_2_ATR * self.increase_2_last_adjust_ratio:
                self.increase_2 = max(self.increase_2_last, benge_low)
                self.increase_2_last = self.increase_2
                return self.increase_2
            else:
                self.increase_2 = max(self.increase_2_last, shangge_low + self.increase_2_ATR * self.increase_2_last_exit_ratio)
                self.increase_2_last = self.increase_2
                return self.increase_2
        # 偶数加仓格子
        elif self.increase_2_position_now % 2 == 0:
            if _quote.last_price >= benge_low + self.increase_2_ATR * self.increase_2_increase_ratio:
                if self.increase_already_increase_number < self.increase_2_position_now // 2: 
                    self.increase_2_exit_after_increase = self.increase_2_increase_exit_ratio_x + (self.increase_2_position_now-1) * self.increase_2_increase_exit_ratio_y
                    self.increase_2 = max(self.increase_2_last, shangge_low + self.increase_2_ATR * self.increase_2_exit_after_increase)
                    self.increase_2_last = self.increase_2
                    self.increase_already_increase_number += 1
                    return 'increase_long'
                else:
                    self.increase_2_exit_after_increase = self.increase_2_increase_exit_ratio_x + (self.increase_2_position_now-1) * self.increase_2_increase_exit_ratio_y
                    self.increase_2 = max(self.increase_2_last, shangge_low + self.increase_2_ATR * self.increase_2_exit_after_increase)
                    self.increase_2_last = self.increase_2
                    return self.increase_2
            else:
                self.increase_2 = max(self.increase_2_last, shangge_low)
                self.increase_2_last = self.increase_2
                return self.increase_2   
        # 奇数不加仓格子
        elif self.increase_2_position_now % 2 == 1:
            if _quote.last_price >= benge_low + self.increase_2_ATR * self.increase_2_adjust_ratio:
                self.increase_2 = max(self.increase_2_last, benge_low)
                self.increase_2_last = self.increase_2
                return self.increase_2
            else:
                self.increase_2 = max(self.increase_2_last, shangge_low + self.increase_2_ATR * self.increase_2_exit_ratio)
                self.increase_2_last = self.increase_2
                return self.increase_2


    def get_increase_3_long(self, _quote, _klines):
        if self.increase_3_ATR == []:
            self.increase_3_ATR = ATR(_klines, self.increase_3_ATR_k_number)['atr'].iloc[-1]
            
            self.increase_3_increase_list = [self.open_price]
            first_increase = self.open_price + self.increase_3_ATR * self.increase_3_first_ATR_ratio
            self.increase_3_increase_list = self.increase_3_increase_list + \
                list(np.arange(first_increase,\
                           first_increase + (self.increase_3_all_increase_times-1)*(self.increase_3_ATR * self.increase_3_next_ATR_ratio) + 1,\
                           self.increase_3_ATR * self.increase_3_next_ATR_ratio))

            self.increase_3_exit_list = [x - self.increase_3_ATR * self.increase_3_eixt_ATR_ratio for x in self.increase_3_increase_list]

        if _quote.last_price < self.increase_3_increase_list[1]:
            self.increase_3_position_now = 0
        elif _quote.last_price >= self.increase_3_increase_list[-1]:
            self.increase_3_position_now = self.increase_3_all_increase_times
        else:
            self.increase_3_position_now = 1 + ((_quote.last_price - self.increase_3_increase_list[1]) \
                                            // self.increase_3_ATR * self.increase_3_next_ATR_ratio)

        self.increase_3_position_now = max(self.increase_3_position_now, self.increase_3_position_last)
        self.increase_3_position_last = self.increase_3_position_now

        self.increase_3 = self.increase_3_exit_list[int(self.increase_3_position_now)]
        increase_price = self.increase_3_increase_list[int(self.increase_3_position_now)]
        if _quote.last_price >= increase_price and self.increase_already_increase_number < self.increase_3_position_now:
            self.increase_already_increase_number = self.increase_3_position_now
            return 'increase_long'

        return self.increase_3


    # --------------------------------下面是做空后的加仓策略--------------------------------------------

# 本格上部 ： self.open_price - _quote.price_tick - \
# self.increase_1_ATR * (self.increase_1_position_now - 1)

# 上格上部 ： self.open_price - _quote.price_tick - \
# self.increase_1_ATR * (self.increase_1_position_now - 2)

    def get_increase_1_short(self, _quote, _klines):
        if self.increase_1_ATR == []:
            self.increase_1_ATR = ATR(_klines, self.increase_1_ATR_k_number)['atr'].iloc[-1]

        self.increase_1_position_now = (self.open_price - _quote.price_tick - _quote.last_price) // self.increase_1_ATR
        self.increase_1_position_now = int(self.increase_1_position_now  +  1)

        benge_high =  self.open_price - _quote.price_tick - self.increase_1_ATR * (self.increase_1_position_now - 1)
        shangge_high = self.open_price - _quote.price_tick - self.increase_1_ATR * (self.increase_1_position_now - 2)
        # 亏损了
        if self.increase_1_position_now <= 0:
            if self.increase_1_last == []:     # 一开始就亏损，将退出价设置设置为 0 
                self.increase_1_last = 0
                return self.increase_1_last
            else:
                return self.increase_1_last    # 之前已经计算过退出价，直接返回退出价 
        # 首个格子
        elif self.increase_1_position_now == 1:
            if _quote.last_price <= self.open_price - _quote.price_tick - self.increase_1_ATR * self.increase_1_adjust_ratio:
                self.increase_1 = min(self.increase_1_last, benge_high)
                self.increase_1_last = self.increase_1
                return self.increase_1
            else:
                return  self.increase_1_last   
        # 最后一个格子
        elif self.increase_1_position_now >= self.increase_1_cell_number:
            if _quote.last_price <= benge_high - self.increase_1_ATR * self.increase_1_last_profit_ratio:
                return 'exit_short'
            elif _quote.last_price <= benge_high - self.increase_1_ATR * self.increase_1_last_adjust_ratio:
                self.increase_1 = min(self.increase_1_last, benge_high)
                self.increase_1_last = self.increase_1
                return self.increase_1
            else:
                self.increase_1 = min(self.increase_1_last, shangge_high - self.increase_1_ATR * self.increase_1_last_exit_ratio)
                self.increase_1_last = self.increase_1
                return self.increase_1
        # 偶数加仓格子
        elif self.increase_1_position_now % 2 == 0:
            if _quote.last_price <= benge_high - self.increase_1_ATR * self.increase_1_adjust_ratio:
                if self.increase_already_increase_number < self.increase_1_position_now // 2: 
                    self.increase_1 = min(self.increase_1_last, benge_high)
                    self.increase_1_last = self.increase_1
                    self.increase_already_increase_number += 1
                    return 'increase_short'
                else:
                    self.increase_1 = min(self.increase_1_last, benge_high)
                    self.increase_1_last = self.increase_1
                    return self.increase_1
            else:
                self.increase_1 = min(self.increase_1_last, shangge_high - self.increase_1_ATR * self.increase_1_exit_ratio)
                self.increase_1_last = self.increase_1
                return self.increase_1
        # 奇数不加仓格子
        elif self.increase_1_position_now % 2 == 1:
            if _quote.last_price <= benge_high - self.increase_1_ATR * self.increase_1_adjust_ratio:
                self.increase_1 = min(self.increase_1_last, benge_high)
                self.increase_1_last = self.increase_1
                return self.increase_1
            else:
                self.increase_1 = min(self.increase_1_last, shangge_high - self.increase_1_ATR * self.increase_1_exit_ratio)
                self.increase_1_last = self.increase_1
                return self.increase_1


    def get_increase_2_short(self, _quote, _klines):
        if self.increase_2_ATR == []:
            self.increase_2_ATR = ATR(_klines, self.increase_2_ATR_k_number)['atr'].iloc[-1]
            # 获取格子总数
            for i in range(2,41,2):
                if self.increase_2_increase_exit_ratio_x + (i - 1) * self.increase_2_increase_exit_ratio_y >= 1: 
                    self.increase_2_cell_number = i
                    break
        self.increase_2_position_now = (self.open_price - _quote.price_tick - _quote.last_price) // self.increase_2_ATR
        self.increase_2_position_now = int(self.increase_2_position_now  +  1)
        benge_high =  self.open_price - _quote.price_tick - self.increase_2_ATR * (self.increase_2_position_now - 1)
        shangge_high = self.open_price - _quote.price_tick - self.increase_2_ATR * (self.increase_2_position_now - 2)
        # 亏损了
        if self.increase_2_position_now <= 0:
            if self.increase_2_last == []:     # 一开始就亏损，将退出价设置设置为 0 
                self.increase_2_last = 0
                return self.increase_2_last
            else:
                return self.increase_2_last    # 之前已经计算过退出价，直接返回退出价 
        # 首个格子
        elif self.increase_2_position_now == 1:
            if _quote.last_price <= self.open_price - _quote.price_tick - self.increase_2_ATR * self.increase_2_adjust_ratio:
                self.increase_2 = min(self.increase_2_last, benge_high)
                self.increase_2_last = self.increase_2
                return self.increase_2
            else:
                if self.increase_2_last == []:    
                    self.increase_2_last = 0
                    return self.increase_2_last 
                else:
                    return self.increase_2_last    
        # 最后一个格子
        elif self.increase_2_position_now >= self.increase_2_cell_number:
            if _quote.last_price <= benge_high - self.increase_2_ATR * self.increase_2_last_profit_ratio:
                return 'exit_short'
            elif _quote.last_price <= benge_high - self.increase_2_ATR * self.increase_2_last_adjust_ratio:
                self.increase_2 = min(self.increase_2_last, benge_high)
                self.increase_2_last = self.increase_2
                return self.increase_2
            else:
                self.increase_2 = min(self.increase_2_last, shangge_high - self.increase_2_ATR * self.increase_2_last_exit_ratio)
                self.increase_2_last = self.increase_2
                return self.increase_2
        # 偶数加仓格子
        elif self.increase_2_position_now % 2 == 0:
            if _quote.last_price <= benge_high - self.increase_2_ATR * self.increase_2_increase_ratio:
                if self.increase_already_increase_number < self.increase_2_position_now // 2: 
                    self.increase_2_exit_after_increase = self.increase_2_increase_exit_ratio_x + (self.increase_2_position_now // 2 - 1) * self.increase_2_increase_exit_ratio_y
                    self.increase_2 = min(self.increase_2_last, shangge_high - self.increase_2_ATR * self.increase_2_exit_after_increase)
                    self.increase_2_last = self.increase_2
                    self.increase_already_increase_number += 1
                    return 'increase_short'
                else:
                    self.increase_2_exit_after_increase = self.increase_2_increase_exit_ratio_x + (self.increase_2_position_now // 2 - 1) * self.increase_2_increase_exit_ratio_y
                    self.increase_2 = min(self.increase_2_last, shangge_high - self.increase_2_ATR * self.increase_2_exit_after_increase)
                    self.increase_2_last = self.increase_2
                    return self.increase_2
            else:
                self.increase_2 = min(self.increase_2_last, shangge_high)
                self.increase_2_last = self.increase_2
                return self.increase_2   
        # 奇数不加仓格子
        elif self.increase_2_position_now % 2 == 1:
            if _quote.last_price <= benge_high - self.increase_2_ATR * self.increase_2_adjust_ratio:
                self.increase_2 = min(self.increase_2_last, benge_high)
                self.increase_2_last = self.increase_2
                return self.increase_2
            else:
                self.increase_2 = min(self.increase_2_last, shangge_high - self.increase_2_ATR * self.increase_2_exit_ratio)
                self.increase_2_last = self.increase_2
                return self.increase_2


    def get_increase_3_short(self, _quote, _klines):
        if self.increase_3_ATR == []:
            self.increase_3_ATR = ATR(_klines, self.increase_3_ATR_k_number)['atr'].iloc[-1]
            
            self.increase_3_increase_list = [self.open_price]
            first_increase = self.open_price - self.increase_3_ATR * self.increase_3_first_ATR_ratio
            self.increase_3_increase_list = self.increase_3_increase_list + \
                list(np.arange(first_increase,\
                           first_increase - (self.increase_3_all_increase_times-1)*(self.increase_3_ATR * self.increase_3_next_ATR_ratio) - 1,\
                            - self.increase_3_ATR * self.increase_3_next_ATR_ratio))

            self.increase_3_exit_list = [x + self.increase_3_ATR * self.increase_3_eixt_ATR_ratio for x in self.increase_3_increase_list]

        if _quote.last_price > self.increase_3_increase_list[1]:
            self.increase_3_position_now = 0
        elif _quote.last_price <= self.increase_3_increase_list[-1]:
            self.increase_3_position_now = self.increase_3_all_increase_times
        else:
            self.increase_3_position_now = 1 + ((self.increase_3_increase_list[1] - _quote.last_price) \
                                            // self.increase_3_ATR * self.increase_3_next_ATR_ratio)

        self.increase_3_position_now = max(self.increase_3_position_now, self.increase_3_position_last)
        self.increase_3_position_last = self.increase_3_position_now

        self.increase_3 = self.increase_3_exit_list[int(self.increase_3_position_now)]
        increase_price = self.increase_3_increase_list[int(self.increase_3_position_now)]
        if _quote.last_price <= increase_price and self.increase_already_increase_number < self.increase_3_position_now:
            self.increase_already_increase_number = self.increase_3_position_now
            return 'increase_short'
        return self.increase_3


    # ------------------------------做多时逐一判断事前选择的退出策略，看是否满足退出条件----------------------
    def exit_judge_long(self, _quote, _klines):
        self.exit_list = []
        # 加仓第几次之后启动移动退出策略
        if self.increase_already_increase_number >= self.exit_move_select:
            for i_move in self.my_exit_method_move:
                exit_price_move = self.exit_dict_long[i_move](_klines)
                self.exit_list.append(exit_price_move)
        for i_fix in self.my_exit_method_move:
            exit_price_fix = self.exit_dict_long[i_fix](_klines)
            self.exit_list.append(exit_price_fix)
        # 如果使用了加仓策略，那计算加仓返回值
        if self.increase_strategy_select:
            increase_return = self.increase_dict_long[self.increase_strategy_select](_quote, _klines)
            if increase_return == 'exit_long' or increase_return == 'increase_long':
                return increase_return
            elif isinstance(increase_return ,numbers.Number):
                self.exit_list.append(increase_return)
                if self.increase_strategy_select == 3 and \
                          self.increase_already_increase_number >= self.increase_3_modify_exit_strategy: 
                    self.exit_list = [increase_return]
            else:
                print('出错')

        if _quote.last_price <= max(self.exit_list):
            message = '{0},最新价{1}小于等于最大退出价{2},平多仓'.\
                format(_quote.datetime, _quote.last_price,  max(self.exit_list))
            print(message)
            return 'exit_long'
        return 'wait_close_or_increase_long'



    # ------------------------------做空时逐一判断事前选择的退出策略，看是否满足退出条件----------------------
    def exit_judge_short(self, _quote, _klines):
        self.exit_list = []
        # 加仓第几次之后启动移动退出策略
        if self.increase_already_increase_number >= self.exit_move_select:
            for i_move in self.my_exit_method_move:
                exit_price_move = self.exit_dict_short[i_move](_klines)
                self.exit_list.append(exit_price_move)
        for i_fix in self.my_exit_method_move:
            exit_price_fix = self.exit_dict_short[i_fix](_klines)
            self.exit_list.append(exit_price_fix)
        # 如果使用了加仓策略，那计算加仓返回值
        if self.increase_strategy_select:
            increase_return = self.increase_dict_short[self.increase_strategy_select](_quote, _klines)
            if increase_return == 'exit_short' or increase_return == 'increase_short':
                return increase_return
            elif isinstance(increase_return ,numbers.Number):
                self.exit_list.append(increase_return)
                if self.increase_strategy_select == 3 and \
                          self.increase_already_increase_number >= self.increase_3_modify_exit_strategy: 
                    self.exit_list = [increase_return]
            else:
                print('出错')

        if _quote.last_price >= min(self.exit_list):
            message = '{0},最新价{1}大于等于最小退出价{2},平空仓'.\
                format(_quote.datetime, _quote.last_price,  min(self.exit_list))
            print(message)
            return 'exit_short'
        return 'wait_close_or_increase_short'




