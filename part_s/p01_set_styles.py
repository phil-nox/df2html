
import pathlib as pl

import pandas as pd
import pandas.io.formats.style

jupyter_style = [                       # https://stackoverflow.com/a/63804055
    {
        'selector': '',                 # https://stackoverflow.com/a/77801513
        'props': [
            ('border', 'none'),
            ('border-collapse', 'collapse'),
            ('border-spacing', '0'),
            ('color', 'black'),
            ('font-size', '12px'),
            ('table-layout', 'fixed'),
            ('font-family', '"DejaVu Sans Mono", monospace'),
        ]
    },
    {
        'selector': 'thead',
        'props': [
            ('border-bottom', '1px solid black'),
            ('vertical-align', 'bottom'),
        ]
    },
    {
        'selector': 'tr',
        'props': [
            ('text-align', 'right'),
            ('vertical-align', 'middle'),
            ('padding', '0.5em 0.5em'),
            ('line-height', 'normal'),
            ('white-space', 'normal'),
            ('max-width', 'none'),
            ('border', 'none'),
        ]
    },
    {
        'selector': 'td',
        'props': [
            ('text-align', 'right'),
            ('vertical-align', 'middle'),
            ('padding', '0.5em 0.5em'),
            ('line-height', 'normal'),
            ('white-space', 'normal'),
            ('max-width', 'none'),
            ('border', 'none'),
        ]
    },
    {
        'selector': 'th',
        'props': [
            ('text-align', 'right'),
            ('vertical-align', 'middle'),
            ('padding', '0.5em 0.5em'),
            ('line-height', 'normal'),
            ('white-space', 'normal'),
            ('max-width', 'none'),
            ('border', 'none'),
            ('font-weight', 'bold'),
        ]
    },
    {
        'selector': 'tbody tr:nth-child(odd)',
        'props': [('background', '#f5f5f5')]
    },
    {
        'selector': 'tbody tr:hover',
        'props': [('background', 'rgba(66, 165, 245, 0.2)')]
    },
]


def set_jupyter_styles(
        df_style: pandas.io.formats.style.Styler,
        styles_extended: None | list | dict = None,   # /api/pandas.io.formats.style.Styler.set_table_styles.html
) -> pandas.io.formats.style.Styler:

    df_style.set_table_styles(jupyter_style)

    if styles_extended is not None:
        df_style.set_table_styles(table_styles=styles_extended, overwrite=False)

    return df_style


if __name__ == '__main__':

    sample: pd.DataFrame = pd.DataFrame({
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

    path = pl.Path('sample.html')
    style = set_jupyter_styles(sample.style, styles_extended=[{'selector': '', 'props': [('font-size', '10px')]}])
    style.format(hyperlinks='html')

    path.write_text(style.to_html())
    print(f'file://{str(path.resolve())}')
