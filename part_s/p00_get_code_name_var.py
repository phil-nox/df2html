
import inspect
import types
import typing as ty

import pandas as pd


def var_name_from_frame(
        caller_frame: inspect.FrameInfo,
        trg: ty.Any,
        default_name: str = 'default_name',
) -> tuple[int, str]:    # tuple[err, name]

    err, rlt = _get_by_code_context(caller_frame)
    if err == 0:
        return 0, rlt

    err, rlt = _get_by_identity_of_object(caller_frame, trg)
    if err == 0:
        return 0, rlt

    return 1, default_name


def _get_by_code_context(                   # works only with single_line call
        caller_frame: inspect.FrameInfo,
) -> tuple[int, str]:    # tuple[err, name]:

    line = caller_frame.code_context[0]
    offset = caller_frame.positions.col_offset

    start = line.find('(', offset)
    if start == -1:
        return 1, ''
    start += 1

    end = start
    while end < len(line) and line[end] not in {',', '(', ')', '[', ']', '\n'}:
        end += 1
    if end == start or end == len(line):
        return 1, ''

    return 0, line[start:end]


def _get_by_identity_of_object(
    caller_frame: inspect.FrameInfo,
    trg: ty.Any,
) -> tuple[int, str]:    # tuple[err, name]:

    src_frame: types.FrameType = caller_frame.frame
    # one id(obj) could have multiple names. suppose f_locals.items is ordered then get first by reversed
    id_2_name = {id(value): name for name, value in reversed(src_frame.f_locals.items())}

    if id(trg) in id_2_name:
        return 0, id_2_name[id(trg)]

    return 1, ''


if __name__ == '__main__':

    def _mock_caller_one(df: pd.DataFrame):
        print(var_name_from_frame(inspect.stack()[1], df))

    def _mock_caller_two(df: pd.DataFrame):
        print(var_name_from_frame(inspect.stack()[1], df))

    best_name_ever: pd.DataFrame = pd.DataFrame({
        'planet': ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune'],
        'radius_km': [2440, 6052, 6371, 3390, 69911, 58232, 25362, 24622],
    })

    _mock_caller_one(
        best_name_ever
    )
    _mock_caller_two(best_name_ever.copy())
