"""A different starting hotel must still complete the entire circular route."""
import unittest
from analyze_start_locations import evaluate

class StartingHotelTests(unittest.TestCase):
    def test_complete_loop_from_each_hotel(self):
        nodes=['a','b','c','d','a'];options={i:{i+1:{'route_km':10}} for i in range(4)}
        for origin in range(4):
            progress,history,last=evaluate(nodes,range(4),[options]*4,origin,0)
            self.assertEqual(progress,4);self.assertEqual(last,3)
            self.assertEqual(sum(t['route_km'] for t in history),40)

    def test_cannot_skip_blocked_gap_by_starting_after_it(self):
        nodes=['a','b','c','d','a'];options={0:{1:{'route_km':10}},1:{},2:{3:{'route_km':10}},3:{4:{'route_km':10}}}
        for origin in range(4):
            progress,history,last=evaluate(nodes,range(4),[options]*10,origin,0)
            self.assertLess(progress,4)

    def test_reject_overshoot_past_finish(self):
        nodes=['a','b','c','a'];days=[{0:{2:{'route_km':20}}},{2:{4:{'route_km':20}}}]
        self.assertEqual(evaluate(nodes,range(3),days,0,0)[0],2)

    def test_wait_for_later_window(self):
        nodes=['a','b','a'];days=[{0:{1:{'route_km':10}}},{1:{}},{1:{2:{'route_km':10}}}]
        progress,history,last=evaluate(nodes,range(2),days,0,0)
        self.assertEqual(progress,2);self.assertEqual(last,2)
        self.assertEqual([t['day'] for t in history],[0,2])

if __name__=='__main__':unittest.main()
