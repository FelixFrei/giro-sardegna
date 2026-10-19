"""Physical and planning invariants for the tacking model."""
import math
import unittest
from simulate_tacking import polar,tack_paths,pareto,Engine,day_reachable
from shapely.geometry import box,LineString
from shapely.prepared import prep
from collections import Counter

class TackingTests(unittest.TestCase):
    def test_documented_upwind_progress(self):
        self.assertAlmostEqual(polar(18,0,'base')[0],20*math.cos(math.radians(55))*.85)
        self.assertAlmostEqual(polar(18,0,'cautious')[0],17*.5*.80)
        self.assertAlmostEqual(polar(13,0,'base')[0],6.8)

    def test_downwind_and_beam(self):
        self.assertAlmostEqual(polar(18,180,'base')[0],22*math.cos(math.radians(35))*.90)
        self.assertEqual(polar(18,90,'base')[0],25)
        self.assertEqual(polar(18,90,'cautious')[0],25*.85)

    def test_mirror_and_lower_cautious_progress(self):
        for wind in [12,14.9,15,19.9,20,25]:
            for angle in range(181):
                self.assertEqual(polar(wind,angle,'base'),polar(wind,-angle,'base'))
                self.assertLessEqual(polar(wind,angle,'cautious')[0],polar(wind,angle,'base')[0]+1e-9)

    def test_triangles_close_and_distance_matches_projection(self):
        for relative in [-40,0,40,160,180,-160]:
            speed,factor,efficiency,theta,mode=polar(18,relative,'base')
            paths=tack_paths((0,0),(1000,0),relative,theta,mode)
            for path in paths:
                self.assertEqual(path[0],(0,0));self.assertEqual(path[-1],(1000,0))
                self.assertAlmostEqual(sum(math.dist(a,b) for a,b in zip(path,path[1:])),1000*factor)
        paths=tack_paths((0,0),(1000,0),0,55,'upwind')
        self.assertAlmostEqual(paths[0][1][1],-paths[1][1][1])

    def synthetic_engine(self,land):
        engine=Engine.__new__(Engine);engine.scenario='base';engine.step_seconds=120
        engine.barrier=prep(land)
        engine.route=lambda a,b:([dict(a=(0,0),b=(1000,0),bearing=0)],1,1)
        engine.nearest=lambda xy:'W'
        engine.wind=lambda ident,t:(18,0)
        return engine

    def test_tack_chooses_water_side(self):
        land=box(100,-2000,900,-1)
        engine=self.synthetic_engine(land)
        result,reason=engine.voyage('a','b',0,3600,trace=True)
        self.assertEqual(reason,'ok')
        self.assertAlmostEqual(result['physical_km'],1/math.cos(math.radians(55)))
        # Geometry is checked in projected metres by the engine on every step.
        self.assertGreater(result['water_seconds'],3600/20)

    def test_route_through_land_rejected(self):
        engine=self.synthetic_engine(box(400,-2000,600,2000))
        self.assertEqual(engine.voyage('a','b',0,3600)[1],'coast')

    def test_wind_loss_during_passage_rejected(self):
        engine=self.synthetic_engine(box(-100,-100,-50,-50))
        engine.wind=lambda ident,t:(18,0) if t<200 else None
        self.assertEqual(engine.voyage('a','b',0,3600)[1],'wind')

    def test_daily_water_budget_and_hotel_requirement(self):
        class FakeEngine:
            failures=Counter()
            def route(self,a,b):return [],1,20
            def voyage(self,a,b,dep,closing):
                if dep+10000>closing:return None,'time'
                return dict(departure=dep,arrival=dep+10000,water_seconds=10000,physical_km=25), 'ok'
        self.assertEqual(set(day_reachable(0,['a','b','c'],{0,1,2},0,28800,FakeEngine(),{})),{1})
        self.assertEqual(day_reachable(0,['a','b','c'],{0,2},0,28800,FakeEngine(),{}),{})

    def test_keep_later_arrival_with_less_water(self):
        rows=[dict(ready=10,water=8),dict(ready=12,water=5),dict(ready=13,water=7),dict(ready=9,water=9)]
        self.assertEqual(pareto(rows),[rows[3],rows[0],rows[1]])

if __name__=='__main__':unittest.main()
