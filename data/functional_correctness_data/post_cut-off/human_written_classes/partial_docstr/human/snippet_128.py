class Evaluator:
    """A simple evaluator"""

    def __init__(self):
        self.partial_scores = None

    def eval_hardness(self, sql):
        count_comp1_ = count_component1(sql)
        count_comp2_ = count_component2(sql)
        count_others_ = count_others(sql)
        if count_comp1_ <= 1 and count_others_ == 0 and (count_comp2_ == 0):
            return 'easy'
        elif count_others_ <= 2 and count_comp1_ <= 1 and (count_comp2_ == 0) or (count_comp1_ <= 2 and count_others_ < 2 and (count_comp2_ == 0)):
            return 'medium'
        elif count_others_ > 2 and count_comp1_ <= 2 and (count_comp2_ == 0) or (2 < count_comp1_ <= 3 and count_others_ <= 2 and (count_comp2_ == 0)) or (count_comp1_ <= 1 and count_others_ == 0 and (count_comp2_ <= 1)):
            return 'hard'
        else:
            return 'extra'

    def eval_exact_match(self, pred, label):
        partial_scores = self.eval_partial_match(pred, label)
        self.partial_scores = partial_scores
        for key, score in partial_scores.items():
            if score['f1'] != 1:
                return 0
        if len(label['from']['table_units']) > 0:
            label_tables = sorted(label['from']['table_units'])
            pred_tables = sorted(pred['from']['table_units'])
            return label_tables == pred_tables
        return 1

    def eval_partial_match(self, pred, label):
        res = {}
        label_total, pred_total, cnt, cnt_wo_agg = eval_sel(pred, label)
        acc, rec, f1 = get_scores(cnt, pred_total, label_total)
        res['select'] = {'acc': acc, 'rec': rec, 'f1': f1, 'label_total': label_total, 'pred_total': pred_total}
        acc, rec, f1 = get_scores(cnt_wo_agg, pred_total, label_total)
        res['select(no AGG)'] = {'acc': acc, 'rec': rec, 'f1': f1, 'label_total': label_total, 'pred_total': pred_total}
        label_total, pred_total, cnt, cnt_wo_agg = eval_where(pred, label)
        acc, rec, f1 = get_scores(cnt, pred_total, label_total)
        res['where'] = {'acc': acc, 'rec': rec, 'f1': f1, 'label_total': label_total, 'pred_total': pred_total}
        acc, rec, f1 = get_scores(cnt_wo_agg, pred_total, label_total)
        res['where(no OP)'] = {'acc': acc, 'rec': rec, 'f1': f1, 'label_total': label_total, 'pred_total': pred_total}
        label_total, pred_total, cnt = eval_group(pred, label)
        acc, rec, f1 = get_scores(cnt, pred_total, label_total)
        res['group(no Having)'] = {'acc': acc, 'rec': rec, 'f1': f1, 'label_total': label_total, 'pred_total': pred_total}
        label_total, pred_total, cnt = eval_having(pred, label)
        acc, rec, f1 = get_scores(cnt, pred_total, label_total)
        res['group'] = {'acc': acc, 'rec': rec, 'f1': f1, 'label_total': label_total, 'pred_total': pred_total}
        label_total, pred_total, cnt = eval_order(pred, label)
        acc, rec, f1 = get_scores(cnt, pred_total, label_total)
        res['order'] = {'acc': acc, 'rec': rec, 'f1': f1, 'label_total': label_total, 'pred_total': pred_total}
        label_total, pred_total, cnt = eval_and_or(pred, label)
        acc, rec, f1 = get_scores(cnt, pred_total, label_total)
        res['and/or'] = {'acc': acc, 'rec': rec, 'f1': f1, 'label_total': label_total, 'pred_total': pred_total}
        label_total, pred_total, cnt = eval_IUEN(pred, label)
        acc, rec, f1 = get_scores(cnt, pred_total, label_total)
        res['IUEN'] = {'acc': acc, 'rec': rec, 'f1': f1, 'label_total': label_total, 'pred_total': pred_total}
        label_total, pred_total, cnt = eval_keywords(pred, label)
        acc, rec, f1 = get_scores(cnt, pred_total, label_total)
        res['keywords'] = {'acc': acc, 'rec': rec, 'f1': f1, 'label_total': label_total, 'pred_total': pred_total}
        return res