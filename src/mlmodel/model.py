from typing import Dict, Tuple, Union

import cv2
import numpy as np
import onnxruntime
from PIL import Image
from PIL.Image import Image as PILImage


def add_background_2_img(input_img, mask_img, background_img):
    input_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB)
    bg_img = cv2.cvtColor(background_img, cv2.COLOR_BGR2RGB)

    dim = (input_img.shape[1], input_img.shape[0])
    bg_img = cv2.resize(bg_img, dim, interpolation=cv2.INTER_LANCZOS4)

    input_img_fg = cv2.bitwise_or(input_img, input_img, mask=mask_img)

    (_, mask_bin) = cv2.threshold(mask_img, 127, 255, cv2.THRESH_BINARY)
    mask_bin_not = cv2.bitwise_not(mask_bin)

    bg_img_bg = cv2.bitwise_or(bg_img, bg_img, mask=mask_bin_not)

    final = cv2.bitwise_or(bg_img_bg, input_img_fg)

    return cv2.cvtColor(final, cv2.COLOR_RGB2BGR)


def post_processing_pil(image: PILImage, mask: PILImage) -> PILImage:
    empty = Image.new("RGBA", (image.size), 0)
    return Image.composite(image, empty, mask)


def post_processing_cv2(image: np.ndarray, mask: np.ndarray) -> np.ndarray:
    rgba = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
    rgba[:, :, 3] = mask
    return cv2.cvtColor(rgba, cv2.COLOR_RGBA2BGRA)


class ModelExtension:
    __mean: Tuple[float, float, float] = (0.485, 0.456, 0.406)
    __stdv: Tuple[float, float, float] = (0.229, 0.224, 0.225)
    __size: Tuple[int, int] = (320, 320)

    def __init__(self, app=None):
        # print(f"Model Path {model_path}")
        self.__onxx_session = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        model_path = app.config["MODEL_PATH"]
        print(f"Model Path {model_path}")
        self.__onxx_session = onnxruntime.InferenceSession(
            str(model_path),
            providers=onnxruntime.get_available_providers(),
            sess_options=onnxruntime.SessionOptions(),
        )

    def __preprocess_pil(self, img: PILImage) -> Dict[str, np.ndarray]:

        image = img.convert("RGB").resize(self.__size, Image.LANCZOS)

        im_ary = np.array(image)
        im_ary = im_ary / np.max(im_ary)

        tmp_image = np.zeros((im_ary.shape[0], im_ary.shape[1], 3))
        tmp_image[:, :, 0] = (im_ary[:, :, 0] - self.__mean[0]) / self.__stdv[0]
        tmp_image[:, :, 1] = (im_ary[:, :, 1] - self.__mean[1]) / self.__stdv[1]
        tmp_image[:, :, 2] = (im_ary[:, :, 2] - self.__mean[2]) / self.__stdv[2]

        tmp_image = tmp_image.transpose((2, 0, 1))

        return {
            self.__onxx_session.get_inputs()[0]
            .name: np.expand_dims(tmp_image, 0)
            .astype(np.float32)
        }

    def __run_pil(self, img: PILImage) -> PILImage:
        onxx_session_output = self.__onxx_session.run(None, self.__preprocess_pil(img))

        pred = onxx_session_output[0][:, 0, :, :]

        ma = np.max(pred)
        mi = np.min(pred)

        pred = (pred - mi) / (ma - mi)
        pred = np.squeeze(pred)

        mask = Image.fromarray((pred * 255).astype("uint8"), mode="L")

        return mask.resize(img.size, Image.LANCZOS)

    def __preprocess_cv2(self, img: np.ndarray) -> Dict[str, np.ndarray]:

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_rgb = cv2.resize(img_rgb, self.__size, interpolation=cv2.INTER_LANCZOS4)

        img_rgb = img_rgb.astype("float32")

        img_rgb = img_rgb / np.max(img_rgb)

        tmp_image = np.zeros((img_rgb.shape[0], img_rgb.shape[1], 3))
        tmp_image[:, :, 0] = (img_rgb[:, :, 0] - self.__mean[0]) / self.__stdv[0]
        tmp_image[:, :, 1] = (img_rgb[:, :, 1] - self.__mean[1]) / self.__stdv[1]
        tmp_image[:, :, 2] = (img_rgb[:, :, 2] - self.__mean[2]) / self.__stdv[2]

        tmp_image = tmp_image.transpose((2, 0, 1))

        return {
            self.__onxx_session.get_inputs()[0]
            .name: np.expand_dims(tmp_image, 0)
            .astype(np.float32)
        }

    def __run_cv2(self, img: np.ndarray) -> np.ndarray:
        onxx_session_output = self.__onxx_session.run(None, self.__preprocess_cv2(img))

        pred = onxx_session_output[0][:, 0, :, :]

        ma = np.max(pred)
        mi = np.min(pred)

        pred = (pred - mi) / (ma - mi)
        pred = np.squeeze(pred)

        mask = (pred * 255).astype("uint8")
        dim = (img.shape[1], img.shape[0])
        mask = cv2.resize(mask, dim, interpolation=cv2.INTER_LANCZOS4)

        return mask

    def predict(self, img: Union[PILImage, np.ndarray]) -> Union[PILImage, np.ndarray]:
        if isinstance(img, PILImage):
            return self.__run_pil(img)
        if isinstance(img, np.ndarray):
            return self.__run_cv2(img)
