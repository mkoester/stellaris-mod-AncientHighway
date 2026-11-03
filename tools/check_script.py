#!/usr/bin/env python3
import sys, re, pathlib
# Structure check for Clausewitz script: depth never negative, ends at 0; in event files every
# key directly inside an event block must be a known event field (catches a stray "}" that
# closes immediate early, as in 0.0.5-SPIKE's first build).
EVENT_KEYS = {'id','title','desc','is_triggered_only','hide_window','trigger','immediate','option',
              'after','picture','show_sound','location','fire_only_once','mean_time_to_happen','is_advisor'}
for p in sys.argv[1:]:
    t = re.sub(r'#[^\n]*', '', pathlib.Path(p).read_text())
    t = re.sub(r'"[^"]*"', '""', t)
    toks = re.findall(r'\{|\}|[^\s{}=]+|=', t)
    depth, bad, stack = 0, [], []
    for i, tk in enumerate(toks):
        if tk == '{':
            stack.append(toks[i-2] if i >= 2 and toks[i-1] == '=' else '?'); depth += 1
        elif tk == '}':
            depth -= 1
            if depth < 0: bad.append('negative depth'); depth = 0
            elif stack: stack.pop()
        elif tk != '=' and i + 1 < len(toks) and toks[i+1] == '=' and depth == 1 and stack and stack[-1].endswith('_event'):
            if tk not in EVENT_KEYS: bad.append('unexpected key in event: %s' % tk)
    print(pathlib.Path(p).name, 'end depth', depth, 'BAD' if bad or depth else 'ok', bad[:3])
