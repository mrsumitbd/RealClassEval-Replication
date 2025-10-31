from zsim.define import ENEMY_ATK_PARAMETER_DICT, ENEMY_ATTACK_ACTION, ENEMY_ATTACK_METHOD_CONFIG, ENEMY_ATTACK_REPORT, ENEMY_RANDOM_ATTACK, ENEMY_REGULAR_ATTACK
import ast
import numpy as np

class EnemyAttackAction:
    """敌人的单个进攻动作，它不记录任何动态数据，只是一个静态的动作数据结构，"""

    def __init__(self, ID: int):
        if ID == 0:
            raise ValueError('EnemyAttackAction实例化所用的ID为0，请检查配置信息！')
        self.id = ID
        self.action_dict = action_file.loc[ID].to_dict()
        self.tag = self.action_dict.get('tag', '')
        self.description = self.action_dict.get('description', '')
        self.hit = int(self.action_dict.get('hit', 0))
        if self.hit <= 0:
            raise ValueError('hit参数必须大于0，请检查配置信息！')
        self.duration = float(self.action_dict.get('duration', 0))
        if self.duration <= 0:
            raise ValueError('duration参数必须大于0，请检查配置信息！')
        self.cd = int(self.action_dict.get('cd', 0))
        hit_list_str = self.action_dict.get('hit_list', None)
        if hit_list_str is None or hit_list_str is np.nan:
            self.hit_list = list((self.duration / (self.hit + 1) * (i + 1) for i in range(int(self.hit))))
        else:
            self.hit_list = ast.literal_eval(hit_list_str)
        if len(self.hit_list) != self.hit:
            raise ValueError(f'{self.tag}的命中数量与命中时间列表长度不符，请检查配置信息！')
        self.parryable = bool(self.action_dict.get('blockable', True))
        self.interruption_level_list = self.action_dict.get('interruption_level_list', None)
        if self.interruption_level_list is None or self.interruption_level_list is np.nan:
            self.interruption_level_list = [1] * self.hit
        else:
            self.interruption_level_list = self.interruption_level_list.split('|')
        self.effect_radius_list = self.action_dict.get('effect_radius_list', None)
        self.stoppable = self.action_dict.get('stoppable', True)
        self.hit_type = self.action_dict.get('hit_type', 'Light')
        if self.hit_type == 'Chain' and self.hit <= 1:
            raise ValueError(f'{self.tag}为连续进攻动作，但是其命中数量为{self.hit}，请检查配置信息！')
        if self.hit_type in ['Light', 'Heavy'] and self.hit > 1:
            raise ValueError(f'{self.tag}为{self.hit_type}攻击，但是其命中数量为{self.hit}，请检查配置信息！')

    def get_hit_tick(self, another_ta: int=None, hit_count: int=1) -> int:
        """获取命中时间，"""
        if not self.hit_list:
            raise ValueError('hit_list为空，无法获取命中点！')
        hit_tick = self.hit_list[hit_count - 1]
        Ta = ENEMY_ATK_PARAMETER_DICT.get('Taction') if another_ta is None else another_ta
        if hit_tick < Ta:
            raise ValueError(f'{self.tag}的第一个命中点({hit_tick})小于响应动作持续时间({Ta})，请检查数据库！')
        return self.hit_list[0]

    def get_first_hit(self) -> int:
        """获取第一个命中点"""
        if not self.hit_list:
            raise ValueError('hit_list为空，无法获取第一个命中点！')
        first_hit_tick = self.hit_list[0]
        Ta = ENEMY_ATK_PARAMETER_DICT.get('Taction')
        if first_hit_tick < Ta:
            raise ValueError(f'{self.tag}的第一个命中点({first_hit_tick})小于相应动作持续时间({Ta})，请检查数据库！')
        return self.hit_list[0]

    def __str__(self):
        return f'进攻动作ID：{self.id}, 技能Tag：{self.tag}，动作耗时：{self.duration}，单次动作的冷却时间：{self.cd}'