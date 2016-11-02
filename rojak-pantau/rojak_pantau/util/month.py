month = {
        'mei': 'May',
        'agu': 'Aug',
        'agt': 'Aug',
        'okt': 'Oct',
        'des': 'Dec'
}

def sanitize(indo_mth):
    indo_mth = indo_mth[0:3].lower()
    return month[indo_mth] if indo_mth in month else indo_mth.title()
