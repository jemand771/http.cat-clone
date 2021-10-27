import pathlib

import bs4
import requests


URL_BASE = "https://http.cat"
DATA_OUT_DIR = pathlib.Path("./data")


def make_url(path):
    return f"{URL_BASE}/{path.lstrip('/')}"


def scrape_all():
    html = requests.get(make_url("/"))
    soup = bs4.BeautifulSoup(html.content, "html.parser")
    elements = soup.ul.find_all("li")
    print(f"found {len(elements)} elements")
    for elem in elements:
        process_li(elem)


def process_li(soup):
    path_div, content_div, title_div = (
        soup.select(f"div[class*='Thumbnail_{class_}__']")
        for class_ in ("image", "content", "title")
    )
    for div in path_div, content_div, title_div:
        assert len(div) == 1
    image_url = make_url(
        path_div[0]["style"].split("background-image:url(")[1].split(")")[0]
    )
    status_code = int(title_div[0].text)
    status_text = content_div[0].p.text
    download_image(status_code, image_url, status_text)


def download_image(status_code, image_url, status_text=""):
    # I know this is hacky, don't judge me - better than using **kwargs :b
    data_dict = locals()
    out_dir = DATA_OUT_DIR / "images"
    out_dir.mkdir(parents=True, exist_ok=True)
    ext = image_url.rsplit(".", 1)[-1]
    r = requests.get(image_url)
    assert 200 <= r.status_code < 300
    with open(out_dir / f"{status_code}.{ext}", "wb") as f:
        f.write(r.content)
    print("downloaded", status_code)
    # TODO shelve/pickle/json list of known data_dicts


if __name__ == "__main__":
    scrape_all()
