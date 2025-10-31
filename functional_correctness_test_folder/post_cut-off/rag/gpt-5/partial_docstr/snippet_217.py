
>> > options = {"k1": "v1", "k2": "v2", "M1": "m1"}
>> > from_to = {"k1": "M1", "k2": "M2"}
>> > new_options = replace_keys(options, from_to)
>> > print(new_options)
... {"M1": "m1", "M2": "v2"}
