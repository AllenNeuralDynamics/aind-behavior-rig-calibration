import unittest

from aind_behavior_services.rig import (
    _FFMPEG_INPUT,
    _FFMPEG_OUTPUT_8BIT,
    _FFMPEG_OUTPUT_16BIT,
    VideoWriterFfmpeg,
    VideoWriterFfmpegFactory,
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
        self.assertEqual(factory._output_arguments, _FFMPEG_OUTPUT_8BIT)
        self.assertEqual(factory._input_arguments, _FFMPEG_INPUT)

    def test_solve_strings_16bit(self):
        factory = VideoWriterFfmpegFactory(bit_depth=16)
        self.assertEqual(factory._output_arguments, _FFMPEG_OUTPUT_16BIT)
        self.assertEqual(factory._input_arguments, _FFMPEG_INPUT)

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
        video_writer = VideoWriterFfmpeg(output_arguments=_FFMPEG_OUTPUT_8BIT, input_arguments=_FFMPEG_INPUT)
        video_writer_from_factory = factory.construct_video_writer_ffmpeg()
        self.assertEqual(video_writer, video_writer_from_factory)


if __name__ == "__main__":
    unittest.main()
