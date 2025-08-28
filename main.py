
import inspect
import pathlib as pl

import pandas as pd
import pandas.io.formats.style

import df2html.part_s.p00_get_code_name_var as p00
import df2html.part_s.p01_set_styles as p01


def save(
        df: pd.DataFrame | pandas.io.formats.style.Styler,
        name: str | None = None,
        to_print: bool = True,
        styles_extended: None | list | dict = None,     # api/pandas.io.formats.style.Styler.set_table_styles.html
) -> str:

    if not isinstance(df, pd.DataFrame | pandas.io.formats.style.Styler):
        raise RuntimeError('df should be pd.DataFrame OR pandas.io.formats.style.Styler type')

    caller_frame = inspect.stack()[1]

    if name is None:
        _, name = p00.var_name_from_frame(
            caller_frame=caller_frame,
            trg=df,
            default_name='df',
        )

    the_path = pl.Path(name if name.endswith('.html') else f'{name}.html')

    style = df.style.format(hyperlinks='html') if isinstance(df, pd.DataFrame) else df
    style = p01.set_jupyter_styles(style, styles_extended)

    the_html = style.to_html()
    the_path.write_text(the_html)

    if to_print:
        print(
            f'file://{str(the_path.resolve())} \t- '                        # link to saved file
            f'File "{caller_frame.filename}", line {caller_frame.lineno}'   # for quick navigation in code (some IDEs)
        )

    return f'file://{str(the_path.resolve())}'


if __name__ == '__main__':
    import df2html

    the_df: pd.DataFrame = pd.DataFrame({
        'planet': ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune'],
        'link': [
            'https://en.wikipedia.org/wiki/Mercury_(planet)',
            'https://en.wikipedia.org/wiki/Venus',
            'https://en.wikipedia.org/wiki/Earth',
            'https://en.wikipedia.org/wiki/Mars',
            'https://en.wikipedia.org/wiki/Jupiter',
            'https://en.wikipedia.org/wiki/Saturn',
            'https://en.wikipedia.org/wiki/Uranus',
            'https://en.wikipedia.org/wiki/Neptune',
        ],
        'radius_km': [2440, 6052, 6371, 3390, 69911, 58232, 25362, 24622],
    })

    the_style = the_df.style
    the_style.format(hyperlinks='html')
    df2html.save(the_style, name='df')

    df2html.save(the_df.head(3), styles_extended=[{'selector': '', 'props': [('font-size', '10px')]}])
