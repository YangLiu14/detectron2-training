# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import unittest
from typing import List, Sequence, Tuple
import torch

from detectron2.structures import ImageList
from detectron2.utils.env import TORCH_VERSION


class TestImageList(unittest.TestCase):
    def test_imagelist_padding_tracing(self):
        # test that the trace does not contain hard-coded constant sizes
        def to_imagelist(tensors: Sequence[torch.Tensor]):
            image_list = ImageList.from_tensors(tensors, 4)
            return image_list.tensor, image_list.image_sizes

        def _tensor(*shape):
            return torch.ones(shape, dtype=torch.float32)

        # test CHW (inputs needs padding vs. no padding)
        for shape in [(3, 10, 10), (3, 12, 12)]:
            func = torch.jit.trace(to_imagelist, ([_tensor(*shape)],))
            tensor, image_sizes = func([_tensor(3, 15, 20)])
            self.assertEqual(tensor.shape, (1, 3, 16, 20), tensor.shape)
            self.assertEqual(image_sizes[0].tolist(), [15, 20], image_sizes[0])

        # test HW
        func = torch.jit.trace(to_imagelist, ([_tensor(10, 10)],))
        tensor, image_sizes = func([_tensor(15, 20)])
        self.assertEqual(tensor.shape, (1, 16, 20), tensor.shape)
        self.assertEqual(image_sizes[0].tolist(), [15, 20], image_sizes[0])

        # test 2x CHW
        func = torch.jit.trace(
            to_imagelist,
            ([_tensor(3, 16, 10), _tensor(3, 13, 11)],),
        )
        tensor, image_sizes = func([_tensor(3, 25, 20), _tensor(3, 10, 10)])
        self.assertEqual(tensor.shape, (2, 3, 28, 20), tensor.shape)
        self.assertEqual(image_sizes[0].tolist(), [25, 20], image_sizes[0])
        self.assertEqual(image_sizes[1].tolist(), [10, 10], image_sizes[1])
        # support calling with different spatial sizes, but not with different #images

    @unittest.skipIf(TORCH_VERSION < (1, 6), "Insufficient pytorch version")
    def test_imagelist_scriptability(self):
        image_nums = 2
        image_tensor = torch.randn((image_nums, 10, 20), dtype=torch.float32)
        image_shape = [(10, 20)] * image_nums

        def f(image_tensor, image_shape: List[Tuple[int, int]]):
            return ImageList(image_tensor, image_shape)

        ret = f(image_tensor, image_shape)
        ret_script = torch.jit.script(f)(image_tensor, image_shape)

        self.assertEqual(len(ret), len(ret_script))
        for i in range(image_nums):
            self.assertTrue(torch.equal(ret[i], ret_script[i]))


if __name__ == "__main__":
    unittest.main()