import cv2 as cv  # pyright: ignore[reportMissingImports]
from cv2.typing import MatLike as Image  # pyright: ignore[reportMissingImports]
import matplotlib.pyplot as plt
from typing import Callable


def _default_preprocessing(image: Image) -> Image:
    return image

class Experiment:
    def __init__(
            self,
            image_path: str,
            threshold1: float,
            threshold2: float,
            use_accurate_gradient: bool = False,
            aperture_size: int=3,
            preprocessing_function: Callable[[Image], Image] = _default_preprocessing,
    ):
        if image_path is None:
            raise ValueError("Image path cannot be None")

        self.image = cv.imread(image_path, cv.IMREAD_GRAYSCALE)

        if self.image is None:
            raise ValueError(f"Could not read the image at path: {image_path}")

        self.threshold1 = threshold1
        self.threshold2 = threshold2
        self.use_accurate_gradient = use_accurate_gradient
        self.aperture_size = aperture_size
        self.preprocessing_function = preprocessing_function
        self.edges = None


    def run(self) -> Image:
        if self.edges is not None:
            return self.edges

        preprocessed = self.preprocessing_function(self.image)
        edges = cv.Canny(
            preprocessed,
            self.threshold1,
            self.threshold2,
            apertureSize=self.aperture_size,
            L2gradient=self.use_accurate_gradient,
        )
        self.edges = edges
        return edges

class ExperimentPlotter:

    @staticmethod
    def plot_edges(exp: Experiment | list[Experiment]):
        if isinstance(exp, list):
            for e in exp:
                plt.figure()
                ExperimentPlotter._plot_edges_single(e)
        else:
            ExperimentPlotter._plot_edges_single(exp)


    @staticmethod
    def _plot_edges_single(exp: Experiment):
        if exp.edges is None:
            exp.run()

        plt.subplot(121)
        plt.imshow(exp.image, cmap='gray')
        plt.title('Original Image')
        plt.xticks([])
        plt.yticks([])
        plt.subplot(122)
        plt.imshow(exp.edges, cmap = 'gray')
        plt.title('Edge Image')
        plt.xticks([])
        plt.yticks([])
        plt.show()
