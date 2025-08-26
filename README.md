
# 📦 df2html
Save your pandas.DataFrame to an .html file with Jupyter Notebook styles.

## Code sample

### General

```python
import pandas as pd
import org_df2html

df: pd.DataFrame = pd.DataFrame({
    'planet': ['Earth', 'Mars'],
    'link': ['https://en.wikipedia.org/wiki/Earth', 'https://en.wikipedia.org/wiki/Mars'],
    'radius_km': [6371, 3390],
})

org_df2html.save(df)  # will print - link to file & link to code line
```

### Using a different font size

```python
df2html.save(df, styles_extended=[{'selector': '', 'props': [('font-size', '10px')]}])
```
