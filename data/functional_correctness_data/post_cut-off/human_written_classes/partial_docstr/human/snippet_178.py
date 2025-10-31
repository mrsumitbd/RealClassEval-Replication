from copy import deepcopy
from zsim.models.event_enums import ListenerBroadcastSignal as LBS
from zsim.define import ELEMENT_TYPE_MAPPING as ETM, ALICE_REPORT

class PolarizedAssaultEvent:

    def __init__(self, execute_tick: int, anomlay_bar: 'AnomalyBar', char_instance: 'Character', skill_node: 'SkillNode'):
        """这是爱丽丝的极性强击事件，该事件拥有最低的优先级，保证自己能够在本tick的最后才被递归执行
        Args:
            execute_tick: int: 该事件在Schedule阶段，被执行的tick
            anomlay_bar: AnomalyBar: 极性强击事件基于当前强击异常条的状态，所以构造时必须传入强击异常条的深拷贝
            char_instance: Character: 爱丽丝的char实例
            skill_node: SkillNode: 触发极性强击事件的触发源（应该是大招或是三蓄力普攻）
        """
        self.execute_tick = execute_tick
        self.schedule_priority = 998
        self.anomaly_bar: 'AnomalyBar' = anomlay_bar
        assert not self.anomaly_bar.settled, '【极性强击事件警告】构造极性强击事件时，传入的异常条必须是未结算的异常条！'
        self.anomaly_bar.anomaly_settled()
        self.anomaly_bar.rename_tag = '极性强击'
        self.char: 'Character' = char_instance
        if self.char.NAME != '爱丽丝':
            raise ValueError(f'【极性强击事件警告】构造极性强击事件时，传入的Char实例并非爱丽丝，而是{self.char.NAME}')
        self.skill_node: 'SkillNode' = skill_node
        self.allowed_skill_tag_list: list[str] = ['1401_SNA_3', '1401_Q']
        if self.skill_node.skill_tag not in self.allowed_skill_tag_list:
            raise ValueError(f'【极性强击事件警告】检测到非法的极性强击触发源：{skill_node.skill_tag}')
        elif skill_node.skill_tag == '1401_Q' and self.char.cinema < 2:
            raise ValueError('【极性强击事件警告】检测到低于2画的爱丽丝企图用 大招 触发极性强击')
        if self.anomaly_bar.element_type != 0:
            raise ValueError(f'【极性强击事件警告】构造极性强击事件时，必须传入物理异常条的深拷贝！当前传入的异常条属性为：{ETM[self.anomaly_bar.element_type]}')
        self.sim_instance = self.anomaly_bar.sim_instance

    def execute(self):
        """执行极性强击事件，向EventList添加强击、紊乱事件"""
        event_list = self.sim_instance.schedule_data.event_list
        enemy = self.sim_instance.enemy
        self.sim_instance.listener_manager.broadcast_event(event=self.anomaly_bar, signal=LBS.POLARIZED_ASSAULT_SPAWN)
        event_list.append(self.anomaly_bar)
        if ALICE_REPORT:
            self.sim_instance.schedule_data.change_process_state()
            print(f'【爱丽丝事件】{self.skill_node.skill.skill_text} 触发的极性强击事件结算！向事件列表添加一个强击异常！')
        from zsim.sim_progress.Update.UpdateAnomaly import anomaly_effect_active
        anomaly_effect_active(bar=self.anomaly_bar, timenow=self.sim_instance.tick, enemy=enemy, new_anomaly=self.anomaly_bar, element_type=0, sim_instance=self.sim_instance)
        active_anomaly_list = enemy.dynamic.get_active_anomaly()
        if not active_anomaly_list:
            return
        anomaly_bar = active_anomaly_list[0]
        anomaly_bar_new = deepcopy(anomaly_bar)
        if not anomaly_bar_new.settled:
            anomaly_bar_new.anomaly_settled()
        '\n        由于爱丽丝的极性强击不影响原有的异常条状态，\n        所以这里必须用深拷贝规避结算紊乱函数对于异常条的破坏性修改\n        '
        from zsim.sim_progress.Update.UpdateAnomaly import spawn_output
        disorder: 'Disorder' = spawn_output(anomaly_bar=anomaly_bar_new, skill_node=self.skill_node, mode_number=1, sim_instance=self.sim_instance)
        event_list.append(disorder)
        if ALICE_REPORT:
            self.sim_instance.schedule_data.change_process_state()
            print(f'【爱丽丝事件】同时，极性强击事件结算了一次【{ETM[disorder.element_type]}】属性的紊乱！')