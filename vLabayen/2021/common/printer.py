#https://misc.flogisoft.com/bash/tip_colors_and_formatting
#TODO: support for bgcolor

MODE = {
    'normal' : '{}',
    'bold' : '\033[1m{}',
    'dim' : '\033[2m{}',
    'underlined' : '\033[4m{}',
    'blink' : '\033[5m{}',
    'inverted' : '\033[7m{}',
    'hidden' : '\033[8m{}'
}
COLOR = {
    'default' : '\033[39m{}',           'black' : '\033[30m{}',                 'white' : '\033[97m{}',
    'red' : '\033[31m{}',               'lred' : '\033[38;5;196m{}',            'dred' : '\033[38;5;88m{}',
    'green' : '\033[32m{}',             'lgreen' : '\033[38;5;82m{}',           'dgreen' : '\033[38;5;22m{}',
    'yellow' : '\033[38;5;184m{}',      'lyellow' : '\033[38;5;226m{}',         'dyellow' : '\033[38;5;142m{}',
    'blue' : '\033[34m{}',              'lblue' : '\033[94m{}',                 'dblue' : '\033[38;5;17m{}',
    'magenta' : '\033[38;5;132m{}',     'lmagenta' : '\033[95m{}',              'dmagenta' : '\033[35m{}',
    'cyan' : '\033[38;5;43m{}',         'lcyan' : '\033[38;5;14m{}',            'dcyan' : '\033[36m{}',
    'orange' : '\033[38;5;214m{}',      'lorange' : '\033[38;5;202m{}',         'dorange' : '\033[38;5;172m{}',
    'gray' : '\033[38;5;245m{}',        'lgray' : '\033[38;5;250m{}',           'dgray' : '\033[38;5;240m{}'
}

def cprepare(text, color = 'default', mode = 'normal'):
    """
    Accepts any color from

        default,black,white,
        red,lred,dred,
        green,lgreen,dgreen,
        yellow,lyellow,dyellow,
        blue,lblue,dblue,
        magenta,lmagenta,dmagenta,
        cyan,lcyan,dcyan,
        orange,lorange,dorange,
        gray,lgray,dgray

    Accepts any mode from   normal,bold,dim,underlined,blink,inverted,hidden
        Also accepts an array of modes
    """
    if not isinstance(mode, list): mymode = MODE[mode]
    else :
        mymode = MODE[mode[0]]
        for m in mode[1:]: mymode = mymode.format(MODE[m])

    return '{}\033[0m'.format(mymode.format(COLOR[color].format(text)))

def cprint(text, color = 'default', mode='normal', **kargs):
    """
    Accepts any color from

        default,black,white,
        red,lred,dred,
        green,lgreen,dgreen,
        yellow,lyellow,dyellow,
        blue,lblue,dblue,
        magenta,lmagenta,dmagenta,
        cyan,lcyan,dcyan,
        orange,lorange,dorange,
        gray,lgray,dgray

    Accepts any mode from   normal,bold,dim,underlined,blink,inverted,hidden
        Also accepts an array of modes
    Accepts any keyword argument to the print function
    """
    print(cprepare(text, color, mode), **kargs)

def ecprepare(text, color = 'default', mode='normal', template='{}'):
    """
    """

    if not isinstance(text, list):
        if isinstance(color, list): raise TypeError("Color cannot be an array with non array text")
        prepared = cprepare(text, color = color, mode = mode)
        return template.format(prepared)

    else:
        if not isinstance(color, list) and not isinstance(mode, list):
            prepared = [cprepare(t, color = color, mode = mode) for t in text]

        elif not isinstance(color, list) and isinstance(mode, list) and not isinstance(mode[0], list):
            if len(text) != len(mode): raise ValueError("Mode and text must have the same lenght")
            prepared = [cprepare(t, color = color, mode = mode[i]) for i,t in enumerate(text)]

        elif not isinstance(color, list) and isinstance(mode, list) and isinstance(mode[0], list):
            if len(text) != len(mode): raise ValueError("First dimension of mode and text must have the same length")
            prepared = [cprepare(t, color = color, mode = mode[i]) for i,t in enumerate(text)]

        elif isinstance(color, list) and not isinstance(mode, list):
            if len(text) != len(color): raise ValueError("Color and text must have the same length")
            prepared = [cprepare(t, color = color[i], mode = mode) for i,t in enumerate(text)]

        elif isinstance(color, list) and isinstance(mode, list) and not isinstance(mode[0], list):
            if len(color) != len(text) or len(text) != len(mode): raise ValueError("Color, Mode and text must have the same length")
            prepared = [cprepare(t, color = color[i], mode = mode[i]) for i,t in enumerate(text)]

        else:
            if len(color) != len(text) or len(text) != len(mode): raise ValueError("Color, first dimension of mode and text must have the same length")
            prepared = [cprepare(t, color = color[i], mode = mode[i]) for i,t in enumerate(text)]

        if template == '{}': template = ' '.join(['{}'] * len(text))
        return template.format(*prepared)

def ecprint(text, color = 'default', mode='normal', template='{}', **kargs):
    """
    """

    print(ecprepare(text, color = color, mode = mode, template = template), **kargs)

def customprepare(text, color = 'default', mode = 'normal'):
    """
    Accepts any color number from   https://misc.flogisoft.com/_media/bash/colors_format/256_colors_fg.png
    Accepts any mode from   normal,bold,dim,underlined,blink,inverted,hidden
        Also accepts an array of modes
    """

    if not isinstance(mode, list): mymode = MODE[mode]
    else :
        mymode = MODE[mode[0]]
        for m in mode[1:]: mymode = mymode.format(MODE[m])

    if color == 'default': return '{}\033[0m'.format(mymode.format(COLOR[color]).format(text))
    else : return '{}\033[0m'.format(mymode.format('\033[38;5;{}m{}'.format(color, text)))

def customprint(text, color = 'default', mode = 'normal', **kargs):
    """
    Accepts any color number from   https://misc.flogisoft.com/_media/bash/colors_format/256_colors_fg.png
    Accepts any mode from   normal,bold,dim,underlined,blink,inverted,hidden
        Also accepts an array of modes
    Accepts any keyword argument to the print function
    """

    print(customprepare(text, color, mode), **kargs)

def ctable(header, data,
    header_color = 'default', header_mode = 'normal',
    rows_color = 'default', rows_mode = 'normal',
    table_color = 'default', table_mode = 'normal',
    side_spacing = 1, horizontal_separator = '-', vertical_separator = '|'):

    if len(data) == 0: raise ValueError('No data provided')
    if len(header) != len(data[0]): raise ValueError('Inconsisten header and data lengths')
    if len(set([len(x) for x in data])) != 1: raise ValueError('Inconsisten length in data rows')

    header = [str(h) for h in header]
    data = [[str(d) for d in row] for row in data]

    row_items_count = len(data[0])
    vertical_separator_len = len(vertical_separator)
    horizontal_separator_len = len(horizontal_separator)
    longest_match_lengths = [max(map(len, header[i:i+1] + [row[i] for row in data])) for i in range(len(header))]
    row_len = (2 * vertical_separator_len) + (vertical_separator_len * (row_items_count - 1)) + (row_items_count * (2 * side_spacing)) + sum(longest_match_lengths)

    item_templates = ['{}{}{}{}{}'.format(side_spacing * ' ', '{:<', longest, '}', side_spacing * ' ') for longest in longest_match_lengths]
    internal_separator = vertical_separator.join([horizontal_separator * (longest + (2 * side_spacing)) for longest in longest_match_lengths])

    row_separator = cprepare(vertical_separator, color = table_color, mode = table_mode)
    colored_header_templates = [cprepare(it, color = header_color, mode = header_mode) for it in item_templates]
    colored_item_templates = [cprepare(it, color = rows_color, mode = rows_mode) for it in item_templates]

    external_horizontal_line = cprepare(horizontal_separator * row_len, color = table_color, mode = table_mode)
    internal_horizontal_line = cprepare('{}{}{}'.format(vertical_separator, internal_separator, vertical_separator) , color = table_color, mode = table_mode)
    header_line_template = '{}{}{}'.format(row_separator, row_separator.join(colored_header_templates), row_separator)
    data_line_template = '{}{}{}'.format(row_separator, row_separator.join(colored_item_templates), row_separator)

    print(external_horizontal_line)
    print(header_line_template.format(*header))
    print(internal_horizontal_line)
    for row in data: print(data_line_template.format(*row))
    print(external_horizontal_line)

def ctable_v2(header, data,
    header_color = 'default', header_mode = 'default',
    cells_color = 'default', cells_mode = 'default',
    table_color = 'default', table_mode = 'normal',
    side_spacing = 1, horizontal_separator = '-', vertical_separator = '|'):

    if len(data) == 0: raise ValueError('No data provided')
    if len(header) != len(data[0]): raise ValueError('Inconsisten header and data lengths')
    if len(set([len(x) for x in data])) != 1: raise ValueError('Inconsisten length in data rows')

    columns_width = [max(len(str(cell)) for cell in col) for col in zip(*list([header] + data))]
    columns_templates = [(side_spacing * ' ' + '{:<' + str(cw) + '}' + ' ' * side_spacing) for cw in columns_width]
    row_len = 2 * side_spacing * len(header) + sum(columns_width) + (len(header) + 1) * len(vertical_separator)

    if not isinstance(header_color, list): header_color = [header_color for _ in header]
    if not isinstance(header_mode, list): header_mode = [header_mode for _ in header]
    if not isinstance(cells_color, list): cells_color = [[cells_color for col in row] for row in data]
    elif not isinstance(cells_color[0], list): cells_color = [[cells_color[i] for col in row] for i,row in enumerate(data)]
    if not isinstance(cells_mode, list): cells_mode = [[cells_mode for col in row] for row in data]
    elif not isinstance(cells_mode[0], list): cells_mode = [[cells_mode[i] for col in row] for i,row in enumerate(data)]

#    header = 
