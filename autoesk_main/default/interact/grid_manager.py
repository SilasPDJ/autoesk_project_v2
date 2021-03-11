class TuplasTabelas:
    def el_grid_setting(self, row: int, col: int, rp=1, cp=1, mt=0, start_row=0, start_col=0):
        """
        :param row: till row
        :param col: till col
        :param rp: row_span
        :param cp: col_span
        :param start_row: ...
        :param start_col: ...

        :param mt: 0 -> line increment, 1 -> col increment, 2 -> both increment

        :return: generator with all equal sized for grid
        """
        if mt > 2:
            mt = 0

        range_row = row + start_row
        range_col = col + start_col

        from itertools import zip_longest
        if mt == 0:
            # line increment
            for r, c, rs, cs in zip_longest(range(start_row, range_row), f'{col}' * row,
                                            range(rp, rp + 1), range(cp, cp + 1), fillvalue=1):
                tup = int(r), int(c), int(rs), int(cs)
                # print(tup)
                yield tup
        elif mt == 1:
            # col increment
            for r, c, rs, cs in zip_longest(f'{row}' * col, range(start_col, range_col),
                                            range(rp, rp + 1), range(cp, cp + 1), fillvalue=1):
                tup = int(r), int(c), int(rs), int(cs)
                # print(tup)
                yield tup
        elif mt == 2:
            # both increment
            for r in range(0, row):
                for c in range(0, col):
                    # print('col')
                    for rs, cs in zip(range(rp, rp + 1), range(cp, cp + 1)):
                        tup = int(r), int(c), int(rs), int(cs)
                        yield tup

        # input()
