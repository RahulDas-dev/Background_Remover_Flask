from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
from PIL.Image import Image as PILImage


def show_output_pil(
    input_img: PILImage, mask_img: PILImage, output_img: Optional[PILImage] = None
) -> None:
    # print(f'input_img.shape {input_img.shape}, output.shape {output_img.shape}')

    figure, (axes1, axes2, axes3) = plt.subplots(1, 3)
    if input_img:
        axes1.imshow(input_img)
        axes1.set_title("Input Image")
    axes1.axis("off")

    if mask_img:
        axes2.imshow(mask_img)
        axes2.set_title("Mask Image")
    axes2.axis("off")

    if output_img:
        axes3.imshow(output_img)
        axes3.set_title("Output Image")
    axes3.axis("off")

    plt.show()


def show_output_cv2(
    input_img: np.ndarray, mask_img: np.ndarray, output_img: Optional[np.ndarray] = None
) -> None:
    # print(f'input_img.shape {input_img.shape}, output.shape {output_img.shape}')

    figure, (axes1, axes2, axes3) = plt.subplots(1, 3)
    if input_img is not None:
        axes1.imshow(input_img[:, :, ::-1])
        axes1.set_title("Input Image")
    axes1.axis("off")

    if mask_img is not None:
        axes2.imshow(mask_img)
        axes2.set_title("Mask Image")
    axes2.axis("off")

    if output_img is not None:
        axes3.imshow(output_img)
        axes3.set_title("Output Image")
    axes3.axis("off")

    plt.show()
