"""Plot the documented geometric route as a standalone overview artifact."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT/'data/phase1'


def main():
    plan=json.loads((DATA/'route-plan.json').read_text())
    land=json.loads((DATA/'land.geojson').read_text())
    route=json.loads((DATA/'route.geojson').read_text())
    fig=plt.figure(figsize=(13,12), facecolor='white')
    ax=fig.add_axes([.05,.12,.58,.78], facecolor='#f0f6fa')
    for f in land['features']:
        x,y=zip(*[c[:2] for c in f['geometry']['coordinates'][0]])
        ax.fill(x,y,color='#e1dece',linewidth=0)
    colors=plt.get_cmap('tab20').colors
    for f in route['features']:
        x,y=zip(*[c[:2] for c in f['geometry']['coordinates']])
        ax.plot(x,y,color=colors[f['properties']['stage_ccw']-1],linewidth=1.8)
    for n,stage in enumerate(plan['stages_calculated'],1):
        point=plan['spots'][stage['stops'][-1]]['landing_coordinate']
        ax.scatter(*point,color=colors[n-1],edgecolors='white',s=65,zorder=4)
        ax.annotate(str(n),point,xytext=(6,4),textcoords='offset points',fontsize=10,weight='bold')
        fig.text(.66,.853-(n-1)*.041,f'{n:02d}  '+plan['spots'][stage['stops'][-1]]['name'],fontsize=9.5)
        fig.text(.66,.838-(n-1)*.041,f"      {stage['km']:.1f} km  ·  {stage['hours']:.2f} h Fahrt",fontsize=8,color='#63717b')
    ax.set_aspect(1/.766)
    ax.set_xlim(8.03,9.93);ax.set_ylim(38.77,41.36)
    ax.set_xlabel('Länge Ost (WGS84)');ax.set_ylabel('Breite Nord (WGS84)')
    ax.grid(alpha=.14)
    fig.text(.06,.96,'Sardinien mit dem Wingfoil',fontsize=24,weight='bold',color='#173647')
    fig.text(.06,.93,f"Routenentwurf · {plan['total_km']:.0f} km · Start/Ziel Poetto · Sant’Antioco aussen",fontsize=13)
    fig.text(.66,.89,'Hotelziele der 16 Module (CCW)',fontsize=12,weight='bold')
    fig.text(.66,.16,'Auch als 9 Fahrtage gebündelt.\nBeide Richtungen dokumentiert.\nPausen und Quellen in den Markdown-Dateien.',fontsize=10,linespacing=1.6)
    fig.text(.06,.035,'Planungsentwurf auf Basis einer geometrischen Route. Wind-Simulation folgt in Phase 2.\nKüste: Regione Autonoma della Sardegna, WFS DBGT · eigene Berechnung · 18.10.2026',fontsize=9,color='#52616b')
    fig.savefig(DATA/'route-overview.png',dpi=160)
    plt.close(fig)


if __name__=='__main__':
    main()
