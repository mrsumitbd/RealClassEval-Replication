import uuid

class S3BucketLifecycleBuilder:

    def __init__(self, **kwargs):
        self.rules = []
        self.add_rule(abort_incomplete_multipart_upload=30)
        if kwargs:
            self.add_rule(**kwargs)

    def add_rule(self, prefix='', tags=None, expiration=None, transitions=None, abort_incomplete_multipart_upload=None):
        rule = dict(ID=__name__ + '.' + str(uuid.uuid4()), Status='Enabled', Filter=dict(Prefix=prefix))
        if tags:
            rule.update(Filter=dict(And=dict(Prefix=prefix, Tags=[dict(Key=k, Value=v) for k, v in tags.items()])))
        if expiration:
            rule.update(Expiration=expiration)
        if transitions:
            rule.update(Transitions=transitions)
        if abort_incomplete_multipart_upload:
            rule.update(AbortIncompleteMultipartUpload=dict(DaysAfterInitiation=abort_incomplete_multipart_upload))
        self.rules.append(rule)

    def __iter__(self):
        yield ('Rules', self.rules)