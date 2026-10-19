"""Checks for the August extension and the UTC month boundary."""
import gzip
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from datetime import datetime,timezone
from simulate_wind import load_weather


class AugustTests(unittest.TestCase):
    def write_batch(self,root,folder,times,ids=('W001',)):
        path=Path(root)/folder;path.mkdir()
        stem=path/'ifs-2022-000'
        Path(str(stem)+'.request.json').write_text(json.dumps({'point_ids':ids}))
        rows=[{'hourly':{'time':times,'wind_speed_10m':[16]*len(times),'wind_direction_10m':[180]*len(times)}} for _ in ids]
        Path(str(stem)+'.json.gz').write_bytes(gzip.compress(json.dumps(rows).encode()))

    def test_contiguous_months_concatenated_once(self):
        sep=int(datetime(2022,9,1,tzinfo=timezone.utc).timestamp())
        with TemporaryDirectory() as tmp:
            self.write_batch(tmp,'raw',[sep,sep+3600])
            self.write_batch(tmp,'raw-august',[sep-7200,sep-3600])
            with patch('simulate_wind.DATA',Path(tmp)):
                base,weather=load_weather(2022,august=True)
                self.assertEqual(base,sep-7200)
                self.assertEqual(len(weather['W001']),4)
                old_base,old=load_weather(2022)
                self.assertEqual(old_base,sep)
                self.assertEqual(len(old['W001']),2)

    def test_gap_rejected(self):
        sep=int(datetime(2022,9,1,tzinfo=timezone.utc).timestamp())
        with TemporaryDirectory() as tmp:
            self.write_batch(tmp,'raw',[sep,sep+3600])
            self.write_batch(tmp,'raw-august',[sep-7200])
            with patch('simulate_wind.DATA',Path(tmp)),self.assertRaisesRegex(AssertionError,'discontinuity'):
                load_weather(2022,august=True)

    def test_missing_location_rejected(self):
        sep=int(datetime(2022,9,1,tzinfo=timezone.utc).timestamp())
        with TemporaryDirectory() as tmp:
            self.write_batch(tmp,'raw',[sep],('W001','W002'))
            self.write_batch(tmp,'raw-august',[sep-3600])
            with patch('simulate_wind.DATA',Path(tmp)),self.assertRaisesRegex(AssertionError,'Incomplete'):
                load_weather(2022,august=True)

if __name__=='__main__':unittest.main()
