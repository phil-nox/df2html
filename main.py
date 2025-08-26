
import inspect
import pathlib as pl

import pandas as pd
import pandas.io.formats.style

import df2html.part_s.p00_get_code_name_var as p00
import df2html.part_s.p01_set_styles as p01


def save(
        df: pd.DataFrame | pandas.io.formats.style.Styler,
        name: str = 'df',
        to_print: bool = True,
        styles_extended: None | list | dict = None,     # api/pandas.io.formats.style.Styler.set_table_styles.html
        hyperlinks: None | str = 'html',                # api/pandas.io.formats.style.Styler.format.html
) -> str:

    if not isinstance(df, pd.DataFrame | pandas.io.formats.style.Styler):
        raise RuntimeError('df should be pd.DataFrame OR pandas.io.formats.style.Styler type')

    caller_frame = inspect.stack()[1]
    _, var_name = p00.var_name_from_frame(
        caller_frame=caller_frame,
        trg=df,
        default_name=name,
    )

    the_path = pl.Path(var_name if var_name.endswith('.html') else f'{var_name}.html')

    the_style = df.style if isinstance(df, pd.DataFrame) else df
    the_style = p01.set_jupyter_styles(the_style, styles_extended)

    the_style.format(hyperlinks=hyperlinks)

    the_html = the_style.to_html()
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

    the_df_style = the_df.style

    df2html.save(the_df_style)
    df2html.save(the_df.head(3), styles_extended=[{'selector': '', 'props': [('font-size', '10px')]}])
