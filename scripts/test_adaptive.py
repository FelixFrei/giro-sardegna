"""Behavioral checks for hotel-only nights and land-wait reachability."""
import unittest
from simulate_adaptive import reachable,solve

class AdaptiveTests(unittest.TestCase):
    def test_wait_at_land_unlocks_next_leg(self):
        trips=reachable(0,[([0],10),([5,30],10)],[2,2],{0,2},0,50,10,5)
        self.assertEqual(trips[2]['arrival'],40)
        self.assertEqual(trips[2]['legs'][1]['departure'],30)
        self.assertNotIn(1,trips) # no hotel, no overnight

    def test_no_feasible_hotel_means_no_day_trip(self):
        self.assertEqual(reachable(0,[([0],10),([],10)],[2,2],{0,2},0,50,10,5),{})

    def test_distance_and_daylight_limits(self):
        paths=[([0],10),([15],10)]
        self.assertEqual(set(reachable(0,paths,[2,2],{0,1,2},0,50,3,5)),{1})
        self.assertEqual(set(reachable(0,paths,[2,2],{0,1,2},0,20,10,5)),{1})

    def test_keep_shorter_hotel_option_and_wait_day(self):
        days=[{0:{1:{'km':2},2:{'km':4}}},{},{1:{3:{'km':4}},2:{}}]
        dest,history,last=solve(0,days,3)
        self.assertEqual(dest,3)
        self.assertEqual([t['end'] for t in history],[1,3])
        self.assertEqual(last,2)

    def test_no_double_travel_day(self):
        dest,history,last=solve(0,[{0:{1:{'km':2}},1:{2:{'km':2}}}],2)
        self.assertEqual(dest,1)

if __name__=='__main__':unittest.main()
