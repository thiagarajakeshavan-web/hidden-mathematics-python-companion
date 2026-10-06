"""Dependency-free SVG plots from current JSON results. No GUI or web access."""
from pathlib import Path
import html
import json
import math
from common import ROOT

COLORS = ['#117A8B','#D67B12','#6B4CA5']

def line_chart(destination, title, subtitle, xlabel, ylabel, series):
    left, top, width, height = 90, 112, 640, 270
    xs = [x for _, rows in series for x,y in rows]
    ys = [y for _, rows in series for x,y in rows]
    xmin, xmax, ymin, ymax = min(xs),max(xs),min(ys),max(ys)
    if xmax==xmin: xmax+=1
    if ymax==ymin: ymax+=1
    pad=(ymax-ymin)*.05
    ymin-=pad; ymax+=pad
    def point(x,y):
        return (left+(x-xmin)/(xmax-xmin)*width, top+height-(y-ymin)/(ymax-ymin)*height)
    esc=html.escape
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="480" viewBox="0 0 800 480" role="img" aria-label="{esc(title)}">',
         f'<title>{esc(title)}</title><desc>{esc(subtitle)}</desc>',
         '<rect width="800" height="480" fill="white"/>',
         '<g font-family="Arial, sans-serif" fill="#17324D">',
         f'<text x="40" y="34" font-size="23" font-weight="bold">{esc(title)}</text>',
         f'<text x="40" y="57" font-size="13">{esc(subtitle)}</text>']
    for i,(label,rows) in enumerate(series):
        x=90+i*220
        svg.append(f'<line x1="{x}" y1="82" x2="{x+20}" y2="82" stroke="{COLORS[i]}" stroke-width="3"/>')
        svg.append(f'<text x="{x+28}" y="86" font-size="12">{esc(label)}</text>')
    for i in range(6):
        y=ymin+(ymax-ymin)*i/5
        _,py=point(xmin,y)
        svg.append(f'<line x1="{left}" y1="{py:.2f}" x2="{left+width}" y2="{py:.2f}" stroke="#E3E8ED"/>')
        svg.append(f'<text x="{left-12}" y="{py+4:.2f}" text-anchor="end" font-size="11">{y:.2g}</text>')
        x=xmin+(xmax-xmin)*i/5
        px,_=point(x,ymin)
        svg.append(f'<text x="{px:.2f}" y="405" text-anchor="middle" font-size="11">{x:.3g}</text>')
    svg.append(f'<path d="M {left} {top} V {top+height} H {left+width}" fill="none" stroke="#17324D"/>')
    for i,(_,rows) in enumerate(series):
        points=' '.join(f'{px:.2f},{py:.2f}' for px,py in [point(x,y) for x,y in rows])
        svg.append(f'<polyline points="{points}" fill="none" stroke="{COLORS[i]}" stroke-width="2.5"/>')
    svg += [f'<text x="410" y="432" text-anchor="middle" font-size="13">{esc(xlabel)}</text>',
            f'<text x="24" y="250" text-anchor="middle" transform="rotate(-90 24 250)" font-size="13">{esc(ylabel)}</text>',
            '<text x="40" y="465" font-size="11" fill="#586A78">Volume I companion · Keshavan Thiagaraja · Synthetic teaching experiment</text>', '</g></svg>']
    Path(destination).write_text('\n'.join(svg)+'\n',encoding='utf-8')

def main():
    stats=json.loads((ROOT/'V1C04/results.json').read_text())
    hist=stats['simulations']['clt_histograms']
    series=[]
    for h in hist:
        mids=[(a+b)/2 for a,b in zip(h['edges'][:-1],h['edges'][1:])]
        density=[count/(5000*.25) for count in h['counts']]
        series.append((f"Sample size {h['sample_size']}",list(zip(mids,density))))
    line_chart(ROOT/'V1C04/clt_sampling_distribution.svg','Standardized sample means',
               '5,000 independent exponential samples per size; histogram density, seed 404',
               'sqrt(n) × (sample mean − 1)','Estimated density',series)
    gd=json.loads((ROOT/'V1C05/results.json').read_text())
    series=[]
    for label,key in [('Rate 0.2: converges','stable'),('Rate 0.8: oscillates','boundary_oscillation'),('Rate 1.0: diverges','divergence')]:
        series.append((label,[(r['iteration'],math.log10(r['loss'])) for r in gd[key]]))
    line_chart(ROOT/'V1C05/learning_rate_loss.svg','Learning rate changes the outcome',
               'The two-point objective uses mean squared error divided by two.',
               'Update number','log10(loss)',series)
    rows=gd['conditioning']['history']
    line_chart(ROOT/'V1C05/conditioning_loss.svg','Conditioning changes convergence speed',
               'Quadratic curvature diag(1, 100); exact diagonal preconditioner for this toy case.',
               'Update number','log10(loss)',[
                   ('Raw rate 0.01',[(r['iteration'],math.log10(r['raw_loss'])) for r in rows]),
                   ('Preconditioned rate 0.5',[(r['iteration'],math.log10(r['preconditioned_loss'])) for r in rows])])
    print('Wrote three SVG charts in V1C04 and V1C05.')

if __name__=='__main__':
    main()
