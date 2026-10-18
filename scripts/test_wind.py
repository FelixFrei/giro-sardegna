"""Tests for direction convention, time interpolation and route accounting."""
import json
from pathlib import Path
import unittest
from zoneinfo import ZoneInfo
from datetime import datetime,timezone

from simulate_wind import components,compatible,attempt,route_actions

ROOT=Path(__file__).resolve().parents[1]
CFG=json.loads((ROOT/'data/phase2/simulation-config.json').read_text())


class WindTests(unittest.TestCase):
    def test_from_direction_and_reverse_course(self):
        u,v=components(20,0)  # north wind moves south
        self.assertTrue(compatible(u,v,180,CFG)[0])
        self.assertFalse(compatible(u,v,0,CFG)[0])
        self.assertTrue(compatible(u,v,90,CFG)[0])
        self.assertTrue(compatible(u,v,270,CFG)[0])

    def test_speed_boundaries(self):
        for speed,result in [(14.9,False),(15,True),(25,True),(25.1,False)]:
            self.assertEqual(compatible(*components(speed,270),90,CFG)[0],result)

    def test_direction_wrap(self):
        a,b=components(20,359),components(20,1)
        u,v=(a[0]+b[0])/2,(a[1]+b[1])/2
        self.assertTrue(compatible(u,v,180,CFG)[0])
        self.assertFalse(compatible(u,v,0,CFG)[0])

    def test_weather_changes_during_passage(self):
        action=[dict(seconds=3600,weather_id='W',bearing=90)]
        weather={'W':[components(20,270),components(10,270),components(20,270)]}
        self.assertEqual(attempt(action,0,0,weather,CFG)[1],'too_light')

    def test_missing_is_not_calm_or_success(self):
        self.assertEqual(attempt([dict(seconds=60,weather_id='W',bearing=90)],0,0,{'W':[None,None]},CFG)[1],'missing')

    def test_pauses_advance_weather_clock(self):
        a=[dict(seconds=1500),dict(seconds=60,weather_id='W',bearing=90)]
        w={'W':[components(20,270)]*3}
        self.assertEqual(attempt(a,0,0,w,CFG),(1560,'ok'))

    def test_dst_conversion(self):
        zone=ZoneInfo('Europe/Rome')
        self.assertEqual(datetime(2025,10,25,9,tzinfo=zone).astimezone(timezone.utc).hour,7)
        self.assertEqual(datetime(2025,10,27,9,tzinfo=zone).astimezone(timezone.utc).hour,8)

    def test_variant_distance_and_pause_accounting(self):
        sampling=json.loads((ROOT/'data/phase2/sampling.json').read_text())
        plan=json.loads((ROOT/'data/phase1/route-plan.json').read_text())
        variants=json.loads((ROOT/'data/phase1/variants.json').read_text())
        for name,rows in variants.items():
            for row in rows:
                actions=route_actions(row,sampling,plan,CFG)
                self.assertAlmostEqual(sum(a['seconds'] for a in actions if 'weather_id' in a),row['km']/25*3600,places=5)
                self.assertEqual(sum('weather_id' not in a for a in actions),len(row['stops'])-2)
                self.assertTrue(all(0<=a['bearing']<360 for a in actions if 'weather_id' in a))


if __name__=='__main__':unittest.main()
