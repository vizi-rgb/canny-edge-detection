import os
import tkinter as tk
import base64
from tkinter import filedialog, messagebox

import cv2 as cv


class CannyDemoApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Canny Edge Detection Demo")
        self.root.geometry("1000x620")

        self.original_bgr = None
        self.preview_size = (440, 440)
        self.original_photo = None
        self.edges_photo = None

        self._build_ui()
        self._load_default_image()

    def _build_ui(self) -> None:
        controls = tk.Frame(self.root, padx=10, pady=10)
        controls.pack(fill=tk.X)

        tk.Button(controls, text="Wczytaj obraz", command=self.load_image).pack(side=tk.LEFT)

        tk.Label(controls, text="Próg 1").pack(side=tk.LEFT, padx=(20, 5))
        self.threshold1 = tk.Scale(
            controls, from_=0, to=255, orient=tk.HORIZONTAL, command=lambda _v: self.update_edges()
        )
        self.threshold1.set(100)
        self.threshold1.pack(side=tk.LEFT)

        tk.Label(controls, text="Próg 2").pack(side=tk.LEFT, padx=(20, 5))
        self.threshold2 = tk.Scale(
            controls, from_=0, to=255, orient=tk.HORIZONTAL, command=lambda _v: self.update_edges()
        )
        self.threshold2.set(200)
        self.threshold2.pack(side=tk.LEFT)

        images = tk.Frame(self.root, padx=10, pady=10)
        images.pack(fill=tk.BOTH, expand=True)

        left = tk.Frame(images)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        right = tk.Frame(images)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(left, text="Oryginalny obraz").pack(pady=(0, 8))
        self.original_label = tk.Label(left, bg="#f0f0f0", width=440, height=440)
        self.original_label.pack(fill=tk.BOTH, expand=True)

        tk.Label(right, text="Krawędzie (Canny)").pack(pady=(0, 8))
        self.edges_label = tk.Label(right, bg="#f0f0f0", width=440, height=440)
        self.edges_label.pack(fill=tk.BOTH, expand=True)

    def _load_default_image(self) -> None:
        default_path = "./gui/ronaldo.jpg"
        if os.path.exists(default_path):
            self._set_image(default_path)

    def load_image(self) -> None:
        path = filedialog.askopenfilename(
            title="Wybierz obraz",
            filetypes=[
                ("Pliki obrazów", "*.jpg *.jpeg *.png *.bmp *.tiff"),
                ("Wszystkie pliki", "*.*"),
            ],
        )
        if not path:
            return
        self._set_image(path)

    def _set_image(self, path: str) -> None:
        image = cv.imread(path, cv.IMREAD_COLOR)
        if image is None:
            messagebox.showerror("Błąd", f"Nie udało się wczytać pliku:\n{path}")
            return
        self.original_bgr = image
        self._show_original()
        self.update_edges()

    def _to_photo(self, image_rgb) -> tk.PhotoImage:
        resized = cv.resize(image_rgb, self.preview_size, interpolation=cv.INTER_AREA)
        ok, png_buffer = cv.imencode(".png", cv.cvtColor(resized, cv.COLOR_RGB2BGR))
        if not ok:
            raise RuntimeError("Nie udało się zakodować obrazu do PNG.")
        png_b64 = base64.b64encode(png_buffer.tobytes()).decode("ascii")
        return tk.PhotoImage(data=png_b64)

    def _show_original(self) -> None:
        if self.original_bgr is None:
            return
        original_rgb = cv.cvtColor(self.original_bgr, cv.COLOR_BGR2RGB)
        self.original_photo = self._to_photo(original_rgb)
        self.original_label.config(image=self.original_photo)

    def update_edges(self) -> None:
        if self.original_bgr is None:
            return
        gray = cv.cvtColor(self.original_bgr, cv.COLOR_BGR2GRAY)
        edges = cv.Canny(gray, self.threshold1.get(), self.threshold2.get())
        edges_rgb = cv.cvtColor(edges, cv.COLOR_GRAY2RGB)
        self.edges_photo = self._to_photo(edges_rgb)
        self.edges_label.config(image=self.edges_photo)

    def run(self):
        self.root.mainloop()


def main() -> None:
    root = tk.Tk()
    app = CannyDemoApp(root)
    app.run()


if __name__ == "__main__":
    main()
