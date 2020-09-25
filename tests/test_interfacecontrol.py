from unittest import TestCase

import RFXtrx


class InterfaceControlTestCase(TestCase):

    def setUp(self):

        self.data = bytearray(b'\x0D\x00\x00\x03\x02\x53\x12\x00\x0C'
                              b'\x2F\x01\x01\x00\x00')
        self.parser = RFXtrx.lowlevel.InterfaceControl()

    def test_parse_bytes(self):
        status = RFXtrx.lowlevel.parse(self.data)
        self.assertEqual(RFXtrx.lowlevel.InterfaceControl, type(status))
        self.assertEqual(status.devices, ['ac', 'arc', 'hideki', 'homeeasy', 'keeloq', 'lacrosse', 'oregon', 'x10'])
        self.assertEqual(status.type_string,'Mode')
        self.assertEqual(status.tranceiver_type,0x53)
        self.assertEqual(status.output_power,0x12)
        self.assertTrue(status.has_value('devices'))

    def test_validate_bytes_short(self):

        data = self.data[:1]
        status = RFXtrx.lowlevel.parse(data)
        self.assertEqual(status, None)
        
    def test_validate_unkown_packet_type(self):

        self.data[1] = 0xFF
        status = RFXtrx.lowlevel.parse(self.data)
        self.assertEqual(status, None)

        

