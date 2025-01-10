import unittest
from typing import List, Literal, Optional

from pydantic import Field

from aind_behavior_services.rig import (
    FFMPEG_INPUT,
    FFMPEG_OUTPUT_8BIT,
    FFMPEG_OUTPUT_16BIT,
    AindBehaviorRigModel,
    ConnectedClockOutput,
    HarpDevice,
    HarpDeviceGeneric,
    HarpWhiteRabbit,
    VideoWriterFfmpeg,
    VideoWriterFfmpegFactory,
    validate_harp_clock_output,
)


class TestVideoWriterFfmpegFactory(unittest.TestCase):
    def test_initialization(self):
        factory = VideoWriterFfmpegFactory(bit_depth=8)
        self.assertEqual(factory._bit_depth, 8)
        self.assertEqual(factory.video_writer_ffmpeg_kwargs, {})

        factory = VideoWriterFfmpegFactory(bit_depth=16, video_writer_ffmpeg_kwargs={"frame_rate": 60})
        self.assertEqual(factory._bit_depth, 16)
        self.assertEqual(factory.video_writer_ffmpeg_kwargs, {"frame_rate": 60})

    def test_solve_strings_8bit(self):
        factory = VideoWriterFfmpegFactory(bit_depth=8)
        self.assertEqual(factory._output_arguments, FFMPEG_OUTPUT_8BIT)
        self.assertEqual(factory._input_arguments, FFMPEG_INPUT)

    def test_solve_strings_16bit(self):
        factory = VideoWriterFfmpegFactory(bit_depth=16)
        self.assertEqual(factory._output_arguments, FFMPEG_OUTPUT_16BIT)
        self.assertEqual(factory._input_arguments, FFMPEG_INPUT)

    def test_construct_video_writer_ffmpeg(self):
        factory = VideoWriterFfmpegFactory(bit_depth=8)
        video_writer = factory.construct_video_writer_ffmpeg()
        self.assertIsInstance(video_writer, VideoWriterFfmpeg)
        self.assertEqual(video_writer.output_arguments, factory._output_arguments)
        self.assertEqual(video_writer.input_arguments, factory._input_arguments)

    def test_update_video_writer_ffmpeg_kwargs(self):
        factory = VideoWriterFfmpegFactory(bit_depth=8)
        video_writer = factory.construct_video_writer_ffmpeg()
        updated_video_writer = factory.update_video_writer_ffmpeg_kwargs(video_writer)
        self.assertEqual(updated_video_writer.output_arguments, factory._output_arguments)
        self.assertEqual(updated_video_writer.input_arguments, factory._input_arguments)

    def test_video_writer_ffmpeg_obj_equality(self):
        factory = VideoWriterFfmpegFactory(bit_depth=8)
        video_writer = VideoWriterFfmpeg(output_arguments=FFMPEG_OUTPUT_8BIT, input_arguments=FFMPEG_INPUT)
        video_writer_from_factory = factory.construct_video_writer_ffmpeg()
        self.assertEqual(video_writer, video_writer_from_factory)


class TestHarpClockOutput(unittest.TestCase):
    class ZeroHarpDevice(AindBehaviorRigModel):
        rig_name: str = "rig"
        computer_name: str = "computer"
        version: Literal["0.0.0"] = "0.0.0"

    class OneHarpDevice(AindBehaviorRigModel):
        rig_name: str = "rig"
        computer_name: str = "computer"
        version: Literal["0.0.0"] = "0.0.0"
        harp_device: Optional[HarpDevice]

    class NHarpDevice(AindBehaviorRigModel):
        rig_name: str = "rig"
        computer_name: str = "computer"
        version: Literal["0.0.0"] = "0.0.0"
        harp_device: Optional[HarpDevice] = None
        harp_white_rabbit: Optional[HarpWhiteRabbit] = None
        harp_device_array: List[HarpDevice] = Field(default_factory=list)

    def setUp(self):
        self.generic_harp = HarpDeviceGeneric(port_name="COM1")
        self.write_rabbit = HarpWhiteRabbit(port_name="COM2")

    @staticmethod
    def _add_clk_out(white_rabbit: HarpWhiteRabbit, n: int) -> HarpWhiteRabbit:
        white_rabbit.connected_clock_outputs = [ConnectedClockOutput(output_channel=i) for i in range(n)]
        return white_rabbit

    def test_zero_harp(self):
        validate_harp_clock_output(self.ZeroHarpDevice())

    def test_one_harp(self):
        validate_harp_clock_output(self.OneHarpDevice(harp_device=self.generic_harp))
        validate_harp_clock_output(self.OneHarpDevice(harp_device=None))

    def test_multiple_devices_no_synchronizer(self):
        validate_harp_clock_output(self.NHarpDevice(harp_device=self.generic_harp))
        validate_harp_clock_output(self.NHarpDevice(harp_device=None))
        validate_harp_clock_output(self.NHarpDevice(harp_device_array=[self.generic_harp]))
        validate_harp_clock_output(self.NHarpDevice(harp_device=None, harp_device_array=[self.generic_harp]))
        validate_harp_clock_output(
            self.NHarpDevice(
                harp_device=None, harp_white_rabbit=self._add_clk_out(self.write_rabbit, 0), harp_device_array=[]
            )
        )

    def test_multiple_devices_with_synchronizer(self):
        validate_harp_clock_output(
            self.NHarpDevice(
                harp_device=self.generic_harp,
                harp_white_rabbit=self._add_clk_out(self.write_rabbit, 3),
                harp_device_array=[self.generic_harp, self.generic_harp],
            )
        )

        with self.assertRaises(ValueError) as _:
            validate_harp_clock_output(
                self.NHarpDevice(
                    harp_device=self.generic_harp,
                    harp_white_rabbit=self._add_clk_out(self.write_rabbit, 4),
                    harp_device_array=[self.generic_harp, self.generic_harp],
                )
            )

        validate_harp_clock_output(
            self.NHarpDevice(
                harp_device=None,
                harp_white_rabbit=self._add_clk_out(self.write_rabbit, 2),
                harp_device_array=[self.generic_harp, self.generic_harp],
            )
        )

        with self.assertRaises(ValueError) as _:
            validate_harp_clock_output(
                self.NHarpDevice(
                    harp_device=None,
                    harp_white_rabbit=self._add_clk_out(self.write_rabbit, 1),
                    harp_device_array=[self.generic_harp, self.generic_harp],
                )
            )

        validate_harp_clock_output(
            self.NHarpDevice(
                harp_device=self.generic_harp,
                harp_white_rabbit=self._add_clk_out(self.write_rabbit, 3),
                harp_device_array=[self.generic_harp, self.generic_harp],
            )
        )

        validate_harp_clock_output(
            self.NHarpDevice(
                harp_device=None, harp_white_rabbit=self._add_clk_out(self.write_rabbit, 2), harp_device_array=[]
            )
        )

        with self.assertRaises(ValueError) as _:
            validate_harp_clock_output(
                self.NHarpDevice(harp_device=self.generic_harp, harp_device_array=[self.generic_harp])
            )
        with self.assertRaises(ValueError) as _:
            validate_harp_clock_output(
                self.NHarpDevice(harp_device=None, harp_device_array=[self.generic_harp, self.generic_harp])
            )


if __name__ == "__main__":
    unittest.main()
