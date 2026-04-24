# KismetAlertExtractor

Extracts alerts from .kismet files.

## Installation

It is recommended to install KismetAlertExtractor using [pipx](https://pipx.pypa.io/stable/):

`pipx install git+https://github.com/JamesConlan96/KismetAlertExtractor.git`

## Usage

```
usage: kismetAlertExtractor.py [-h] [-f FIELD [FIELD ...]] [-i FILE [FILE ...]] [-l] [-n] [-o FILE]
                               [-s {asciidoc,colon_grid,double_grid,double_outline,fancy_grid,fancy_outline,github,grid,heavy_grid,heavy_outline,html,jira,latex,latex_booktabs,latex_longtable,latex_raw,mediawiki,mixed_grid,mixed_outline,moinmoin,orgtbl,outline,pipe,plain,presto,pretty,psql,rounded_grid,rounded_outline,rst,simple,simple_grid,simple_outline,textile,tsv,unsafehtml,youtrack}]

Kismet alert extractor

options:
  -h, --help            show this help message and exit
  -f, --fields FIELD [FIELD ...]
                        kismet alert fields to include in output(Default: 'kismet.alert.timestamp, kismet.alert.class, kismet.alert.header, kismet.alert.text, kismet.alert.severity,
                        kismet.alert.source_mac, kismet.alert.dest_mac, kismet.alert.frequency, kismet.alert.channel')
  -i, --inputFiles FILE [FILE ...]
                        kismet file(s) to extract alerts from
  -l, --listFields      list supported kismet alert fields
  -n, --noPrompt        overwrite existing output files without asking
  -o, --outputFile FILE
                        file to save alerts to
  -s, --style {asciidoc,colon_grid,double_grid,double_outline,fancy_grid,fancy_outline,github,grid,heavy_grid,heavy_outline,html,jira,latex,latex_booktabs,latex_longtable,latex_raw,mediawiki,mixed_grid,mixed_outline,moinmoin,orgtbl,outline,pipe,plain,presto,pretty,psql,rounded_grid,rounded_outline,rst,simple,simple_grid,simple_outline,textile,tsv,unsafehtml,youtrack}
                        style for output tables (default: github)
```