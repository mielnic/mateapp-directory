# Separates filename of extension (and shortens name for display).

def splitFilename(filename):

    blue = ['doc', 'docx', 'dot', 'dotx', 'pages', 'txt', 'rtf']
    green = ['xls', 'xlsx', 'xlt', 'xltx', 'xltm', 'xlm', 'xlsm', 'numbers']
    red = ['pdf', 'ppt', 'pptx', 'key']
    yellow = ['jpeg', 'jpg', 'png', 'tiff', 'svg']

    x = filename.split('.')
    ext = x[-1]
    x.pop()
    name = '.'.join(x)
    if len(name) > 15:
        shortname = f'{name[:15]}...'
    else:
        shortname = name
    
    if ext in blue:
        color = 'primary'
    elif ext in green:
        color = 'success'
    elif ext in red:
        color = 'danger'
    elif ext in yellow:
        color = 'warning'
    else:
        color = 'secondary'

    return shortname, color, ext