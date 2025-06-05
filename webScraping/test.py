import urllib.parse

base_url = "https://www.anandtech.com/tag/mb"
current_link_idx = 2

page_link = urllib.parse.urljoin(base_url, str(current_link_idx))
page_link = base_url + r"/" + str(current_link_idx)
print(f"Next page link: {page_link}")