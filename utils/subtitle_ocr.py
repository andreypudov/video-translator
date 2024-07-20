import os
from srt import Subtitle, compose
from datetime import timedelta
from paddleocr import PaddleOCR


def generate_subtitle(frames_dir: str, language: str, subtitle_file: str):
    frame_imgs = os.listdir(frames_dir)
    frame_imgs.sort()

    ocr = PaddleOCR(use_angle_cls=True, lang=language)

    subs = []
    prev = ""
    for f in frame_imgs:
        img_path = os.path.join(frames_dir, f)
        print(img_path)
        result = ocr.ocr(img_path, cls=True)

        sub = ""
        start = None
        end = None

        if result and len(result) > 0 and result[0] is not None:
            for index in enumerate(result):
                res = result[index]

                for line in res:
                    print(line[1][0])
                    if sub == "":
                        sub = line[1][0]
                    else:
                        sub += f" {line[1][0]}"

        # Get hour, min, second from frame_h:m:s.jpg
        h = int(f.split("_")[1].split(":")[0])
        m = int(f.split("_")[1].split(":")[1])
        s = ".".join(f.split("_")[1].split(":")[2].split(".")[:-1])
        s = float(f"{s}")

        if sub == "" and prev != "":  # end of subtitle
            end = timedelta(hours=h, minutes=m, seconds=s)
            subtitle = Subtitle(index=1, start=start, end=end, content=prev)
            subs.append(subtitle)

        if sub != "" and prev == "":  # start of subtitle
            start = timedelta(hours=h, minutes=m, seconds=s)

        if sub != "" and prev != "" and sub != prev:  # change of subtitle
            end = timedelta(hours=h, minutes=m, seconds=s)
            subtitle = Subtitle(index=1, start=start, end=end, content=prev)
            subs.append(subtitle)
            start = timedelta(hours=h, minutes=m, seconds=s)

        prev = sub

    with open(subtitle_file, "w", encoding="utf-8") as fp:
        fp.write(compose(subs))
