import os.path
import xml.etree.ElementTree as ET

import jinja2

STATIC_ROOT = ""


def video(ok, msg, video):
    video_subclass = "good_video" if ok else "bad_video"
    path = STATIC_ROOT + video + ".mp4"
    xml = ET.Element("div", attrib={"class": "video_container " + video_subclass})
    if not ok:
        label_cont = ET.SubElement(xml, "div", attrib={"class": "video_label_container"})
        label=ET.SubElement(label_cont, "div", attrib={"class": "video_label"})
        label.text = msg
    vid = ET.SubElement(
        xml, "video", {"muted": "", "loop": "", "autoplay": "", "class": "video_frame"}
    )
    src = ET.SubElement(vid, "source", {"src": path, "type": "video/mp4"})
    src.text = "Your browser does not support the video tag."
    out = ET.tostring(xml, encoding="unicode", method="html")
    return out


if __name__ == "__main__":
    d = os.path.dirname(__file__)
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(d),
        lstrip_blocks=True,
        autoescape=False,
        keep_trailing_newline=True,
    )

    with open(os.path.join(d, "merged.out.html"), "w") as f:
        f.write(env.get_template("merged.in.html").render(video=video))
