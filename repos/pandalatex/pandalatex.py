def latex_max(data, bgcolor='yellow', fgcolor="black", ignore=['AvgContent',]):
    '''
    highlight the maximum in a Series or DataFrame
    '''
    txt = '{:.3f}'
    attr = '\textbf{{{}}}'
    attr_max = '\colorbox{{' + bgcolor + '}}{{\textcolor{{' + fgcolor + '}}{{{}}}}}'
#     print(data)
    is_max = data >= data.drop(ignore).max()
    mx = data.drop(ignore).max()
    real_mx = data.max()
    attrs = []
    for v in data:
        a = txt.format(v)
        if v == mx:
            a = attr.format(a)
        if v == real_mx:
            a = attr_max.format(a)
        attrs.append(a)
    return pd.Series(attrs, index=data.index)

def to_latex(df, *args, **kwargs):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.max_colwidth', -1):
        print(df.apply(lambda x: latex_max(x, *args, **kwargs), axis=1).to_latex(escape=False))