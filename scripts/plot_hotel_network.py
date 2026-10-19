"""Reproduce the current README map from archived coast, route and hotel data."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT=Path(__file__).resolve().parents[1]

def main():
    plan=json.loads((ROOT/'data/phase1/route-plan.json').read_text())
    network=json.loads((ROOT/'data/phase2/hotel-network-expanded.json').read_text())
    old=json.loads((ROOT/'data/phase2/hotel-network.json').read_text())
    new=set(network['additional_hotels'])-set(old['additional_hotels'])
    hotels={k for k,v in plan['spots'].items() if v.get('hotel')}|set(network['additional_hotels'])
    ordered=[l['start'] for l in plan['legs'] if l['start'] in hotels]
    assert len(ordered)==33 and len(new)==12
    land=json.loads((ROOT/'data/phase1/land.geojson').read_text())
    route=json.loads((ROOT/'data/phase1/route.geojson').read_text())
    plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none'})
    fig=plt.figure(figsize=(14,13),facecolor='#fbfcfd')
    ax=fig.add_axes([.055,.17,.56,.69],facecolor='#eaf3f8')
    for f in land['features']:
        x,y=zip(*[c[:2] for c in f['geometry']['coordinates'][0]])
        ax.fill(x,y,color='#dedfd3',linewidth=0)
    for f in route['features']:
        x,y=zip(*[c[:2] for c in f['geometry']['coordinates']])
        ax.plot(x,y,color='#386fa3',linewidth=1.7,zorder=2)
    points=[]
    for num,k in enumerate(ordered,1):
        x,y=plan['spots'][k]['landing_coordinate'];isnew=k in new
        ax.scatter(x,y,s=45 if isnew else 35,marker='D' if isnew else 'o',color='#c75b20' if isnew else '#17685d',edgecolor='white',linewidth=.8,zorder=4)
        points.append((num,k,x,y))
    # Spread neighbouring number labels vertically while keeping short leaders.
    for side in [-1,1]:
        group=sorted([p for p in points if (-1 if p[2]<8.95 else 1)==side],key=lambda p:p[3])
        last=38.76
        for num,k,x,y in group:
            labely=max(y,last+.062);last=labely
            ax.annotate(str(num),(x,y),xytext=(x+side*.14,labely),fontsize=8.5,ha='center',va='center',weight='bold',color='#263a44',bbox=dict(boxstyle='round,pad=.15',fc='white',ec='none',alpha=.93),arrowprops=dict(arrowstyle='-',color='#76868c',lw=.6),zorder=5)
    ax.set_xlim(7.95,10.12);ax.set_ylim(38.77,41.40);ax.set_aspect(1/.766)
    ax.set_xlabel('Länge Ost · WGS84',fontsize=9);ax.set_ylabel('Breite Nord · WGS84',fontsize=9)
    ax.tick_params(labelsize=8);ax.grid(alpha=.15)
    ax.annotate('N',xy=(8.08,41.29),xytext=(8.08,41.11),ha='center',weight='bold',arrowprops=dict(arrowstyle='-|>',color='#263a44'))
    fig.text(.055,.954,'Sardinien · Route und Hotelziele',fontsize=24,weight='bold',color='#163747')
    fig.text(.055,.922,'891 km  ·  33 Hotelorte  ·  beide Richtungen  ·  Sant’Antioco aussen',fontsize=13,color='#38545e')
    fig.text(.65,.872,'HOTELORTE ENTLANG DER RUNDE',fontsize=11,weight='bold',color='#163747')
    for num,k,x,y in points:
        label=plan['spots'][k]['name'];color='#a64816' if k in new else '#243e45'
        fig.text(.65,.845-(num-1)*.0204,f'{num:02d}  {label}'+('  +' if k in new else ''),fontsize=9.1,color=color)
    fig.text(.65,.145,'+  neu im erweiterten Hotelnetz\nNummern folgen der Route gegen den Uhrzeigersinn.\nJeder Hotelort wurde auch als Start/Ziel geprüft.',fontsize=9,color='#4d6269',linespacing=1.5)
    handles=[Line2D([0],[0],color='#386fa3',lw=2,label='Geometrische Route'),Line2D([0],[0],marker='o',color='none',markerfacecolor='#17685d',markeredgecolor='white',markersize=8,label='21 bisherige Hotelorte'),Line2D([0],[0],marker='D',color='none',markerfacecolor='#c75b20',markeredgecolor='white',markersize=8,label='12 ergänzte Hotelorte')]
    fig.legend(handles=handles,loc='lower left',bbox_to_anchor=(.055,.10),frameon=False,fontsize=10)
    fig.text(.055,.063,'Übersicht des Hotelnetzes, keine Tagesetappen oder tatsächlichen Kreuzkurse.\nWindmodell: 12–25 kn · maximal 5 h Wasserzeit · August–Oktober 2022–2025.',fontsize=10,color='#38545e',linespacing=1.5)
    fig.text(.055,.022,'Küste: Regione Autonoma della Sardegna, WFS DBGT · Route: eigene Berechnung · Hotelquellen: docs/24 · Stand 19.10.2026',fontsize=8,color='#61727a')
    for suffix in ['png','svg']:fig.savefig(ROOT/f'data/phase2/hotel-network-overview.{suffix}',dpi=170)
    plt.close(fig)

if __name__=='__main__':main()
