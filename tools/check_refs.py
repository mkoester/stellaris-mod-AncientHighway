#!/usr/bin/env python3
"""Cross-reference check for the mod folder given as argument: every ahw_* effect, trigger,
initializer, megastructure and bypass type used is defined, every text key exists once, every
megastructure has its outliner sprite. Prints problems; exit 1 if any."""
import re
import sys
import pathlib

M = pathlib.Path(sys.argv[1])
strip = lambda t: re.sub(r'"[^"]*"', '""', re.sub(r'#[^\n]*', '', t))
code = {p: strip(p.read_text()) for p in M.rglob('*.txt')}
alltxt = '\n'.join(code.values())
events_raw = '\n'.join(re.sub(r'#[^\n]*', '', p.read_text()) for p in M.rglob('events/*.txt'))


def defs(sub):
    return set(re.findall(r'^(\w+) = \{', '\n'.join(t for p, t in code.items() if sub in str(p)), re.M))


known = set().union(*(defs(d) for d in ('scripted_effects', 'scripted_triggers', 'megastructures', 'bypass',
                                        'technology', 'solar_system_initializers', 'megastructure_overclock_types',
                                        'star_classes', 'missions', 'event_chains')))
known |= set(re.findall(r'^\t\t(\w+) = \{', '\n'.join(t for p, t in code.items() if 'missions' in str(p)), re.M))  # contract counters
megas, byps = defs('megastructures'), defs('bypass')
problems = []
problems += [f'undefined: {c}' for c in sorted(set(re.findall(r'(?<![:.\w])(ahw_\w+) = (?:yes|\{)', alltxt)) - known)]
used_megas = {u for u in re.findall(r'(?<!bypass_)type = (ahw_[\w$]+)', alltxt) if '$' not in u}
problems += [f'undefined megastructure: {m}' for m in sorted(used_megas - megas)]
templated = re.findall(r'type = (ahw_\w+)_\$N\$', alltxt)
problems += [f'templated megastructure {t}_N missing for some N' for t in set(templated)
             if not any(k.startswith(t + '_') for k in megas)]
used_byp = {b for b in re.findall(r'(?:is_bypass_type|add_seen_bypass_type|bypass_type) = (ahw_\w+)', alltxt)}
problems += [f'undefined bypass type: {b}' for b in sorted(used_byp - byps)]
problems += [f'undefined initializer: {i}' for i in sorted(set(re.findall(r'initializer = (\w+)', alltxt)) - defs('solar_system_initializers'))]
loc = ''.join(p.read_text(encoding='utf-8-sig') for p in (M / 'localisation').rglob('*.yml'))
keys = re.findall(r'^ (\S+):0', loc, re.M)
problems += [f'duplicate text key: {k}' for k in sorted({k for k in keys if keys.count(k) > 1})]
need = {m + s for m in megas for s in ('', '_DESC', '_MEGASTRUCTURE_DETAILS')}
need |= {f'{p}_{b.upper()}' for b in byps for p in ('BYPASS', 'ENTRY_BYPASS', 'EXIT_BYPASS')}
need |= set(re.findall(r'(?:title|desc|name) = (ahw(?:_debug|_story)?\.[\w.]+)', events_raw))
need |= set(re.findall(r'^\s*name = (NAME_\w+)', alltxt, re.M))
# 0.1.1: tooltips and AI-weight descs naming our keys, resolutions and their categories (name +
# desc), and $KEY$ references from one of our texts to another
OURS = r'(?:AHW_\w+|ahw_\w+|resolution(?:_category)?_ahw_\w+)'
need |= set(re.findall(rf'(?:fail_text|custom_tooltip|desc) = "?({OURS})"?(?![.\w])', alltxt))
need |= {k + s for k in re.findall(r'^(resolution(?:_category)?_ahw_\w+) = \{', alltxt, re.M) for s in ('', '_desc')}
need |= set(re.findall(rf'\$({OURS})\$', loc))
# 2026-11-23: every event's chain line (event_chain = ...) is a defined chain, with its title and desc
chains = defs('event_chains')
used_chains = set(re.findall(r'event_chain = "?(\w+)"?', alltxt))
problems += [f'undefined event chain: {c}' for c in sorted(used_chains - chains)]
need |= {c + s for c in chains for s in ('_title', '_desc')}
problems += [f'missing text: {k}' for k in sorted(need - set(keys))]
defined_ev = set(re.findall(r'^\tid = (ahw\w*\.\d+)', events_raw, re.M))
fired = set(re.findall(r'(?:event|country_event|ship_event|fleet_event) = \{ id = (ahw\w*\.\d+)', alltxt))
fired |= set(re.findall(r'^\t\t(ahw\w*\.\d+)', '\n'.join(t for p, t in code.items() if 'on_actions' in str(p)), re.M))
problems += [f'undefined event: {e}' for e in sorted(fired - defined_ev)]
gfx = ''.join(p.read_text() for p in M.rglob('*.gfx'))
problems += [f'missing sprite: GFX_{m}_outliner_icon' for m in sorted(megas) if f'GFX_{m}_outliner_icon' not in gfx]
print('\n'.join(problems) or 'refs ok')
sys.exit(1 if problems else 0)
