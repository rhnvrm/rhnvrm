#!/usr/bin/env python3
"""Read the workbench's public generated fragment; preserve hand-written sections."""
from pathlib import Path
from urllib.request import Request, urlopen

START = '<!-- github-activity:start -->'
END = '<!-- github-activity:end -->'


def replace_activity(readme, fragment):
    if readme.count(START) != 1 or readme.count(END) != 1:
        raise ValueError('README must contain one pair of activity markers')
    before, rest = readme.split(START)
    _, after = rest.split(END)
    return before + START + '\n' + fragment.strip() + '\n' + END + after


if __name__ == '__main__':
    request = Request('https://raw.githubusercontent.com/rhnvrm/rhnvrm.github.io/master/data/profile-activity.md', headers={'User-Agent':'rhnvrm-profile'})
    with urlopen(request, timeout=30) as response:
        fragment = response.read().decode('utf-8')
    if not fragment.strip() or len(fragment) > 20000:
        raise ValueError('Invalid activity fragment; README left unchanged')
    readme = Path('README.md')
    readme.write_text(replace_activity(readme.read_text(), fragment))
