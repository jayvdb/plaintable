__version__ = '0.1'
__license__ = 'MIT'
__copyright__ = '(c) 2014 Stefan Tatschner <stefan@sevenbyte.org>'


class Table:

    THEMES = {'simple': {'header_overline' : '',
                         'header_underline': '-',
                        'footer_overline' : '',
                         'footer_underline': ''},
              'plain':  {'header_overline' : '',
                         'header_underline': '',
                         'footer_overline' : '',
                         'footer_underline': ''}}

    def __init__(self, data, headline=None, align='l', padding=2, floatprec=2,
                 theme='simple'):
        data = data
        self.align = align
        self.padding = padding
        self.floatprec = floatprec
        self.theme = theme

        data = self._normalize(data)
        self.cols = list(zip(*data))
        # At first get the longest value in a column, then calculate its length.
        self._col_widths = [len(max(col, key=len)) for col in self.cols]

        if headline:
            # Append the table to header and update cols.
            d = self._get_header(headline)
            d.extend(data)
            self.cols = list(zip(*d))
            self._col_widths = [len(max(col, key=len)) for col in self.cols]

        #self._add_footer()
        self.cols = self._align_cols()

    def _normalize(self, data):
        norm_data = []
        for row in data:
            norm_row = []
            for col in row:
                if isinstance(col, float):
                    format_str = '{{:.{}f}}'.format(self.floatprec)
                    item = format_str.format(col)
                else:
                    item = str(col)
                norm_row.append(item)
            norm_data.append(norm_row)
        return norm_data

    def _get_col_widths(self):
        # At first get the longest value in a column, then calculate its length.
        widths = [len(max(col, key=len)) for col in self.cols]
        return widths

    def _align_cols(self):
        al_cols = []
        # Iterate over several lists at the same time.
        # http://stackoverflow.com/a/10080389
        for col, width in zip(self.cols, self._col_widths):
            al_col = []
            for item in col:
                pad_width = width + self.padding
                # Build formatstring depending on alignment.
                if self.align == 'l':
                    format_str = '{{:<{}}}'.format(pad_width)
                elif self.align == 'r':
                    format_str = '{{:>{}}}'.format(pad_width)
                elif self.align == 'c':
                    format_str = '{{:^{}}}'.format(pad_width)
                else:
                    print('Error: Wrong alignment!')
                    exit(1)

                al_item = format_str.format(item)
                al_col.append(al_item)
            al_cols.append(al_col)
        return al_cols

    def _get_header(self, headline):
        header = []
        header_overline = []
        header_underline = []

        for width in self._col_widths:
            if self.THEMES[self.theme]['header_overline']:
                item = self.THEMES[self.theme]['header_overline'] * width
                header_overline.append(item)
            elif self.THEMES[self.theme]['header_underline']:
                item = self.THEMES[self.theme]['header_underline'] * width
                header_underline.append(item)

        if header_overline:
            header.append(header_overline)
        header.append(headline)
        if header_underline:
            header.append(header_underline)
        return header

    def __str__(self):
        table = [''.join(col) for col in zip(*self.cols)]
        table = '\n'.join(table)
        return table
