from bs4 import BeautifulSoup
import json
import logging
import os


SNAPSHOT_PATH = 'data/website/www.ufc.com/rankings'
# snapshots = list(map(lambda x: os.path.join(SNAPSHOT_PATH, x), os.listdir(SNAPSHOT_PATH)))
DATA_PATH = 'data/json'


def main():
  filenames = os.listdir(SNAPSHOT_PATH)
  for filename in filenames:
    logging.warn("Processing: %s" % filename)
    html_data = load(filename)
    document = BeautifulSoup(html_data, "html5lib")
    all_lists = document.find_all("div", class_="ranking-list")
    json_data = extract(all_lists)
    json_data['filename'] = filename
    json_data['rankings-date'] = document.find(id="rankings-date").text.strip()
    save(json_data)


def save(data):
  file_path = "%s/%s.json" % (DATA_PATH, data['filename'].split('.')[0])
  if not data:
    return

  with open(file_path, 'w+') as output:
    raw_data = json.dump(data, output, indent=2)
    if raw_data:
      output.write(raw_data)


def load(filename):
  file_path = "%s/%s" % (SNAPSHOT_PATH, filename)
  with open(file_path, 'r') as in_data:
    html_data = in_data.read()
  return html_data


def get_weight_class(data):
  weight_class = data.find(id="weight-class-name") or data.find(class_="weight-class-name")
  return weight_class.text.strip()


def get_champ(data):
  champ_name = ""
  champ = data.find(id="champion-fighter-name")
  if champ:
    champ_name = champ.a.text.strip()
  return champ_name


def extract(data):
  res = {}

  for ranking_list in data:
    ranks = []
    weight_class = get_weight_class(ranking_list)
    ranks.append(get_champ(ranking_list))
    rows = ranking_list.find_all("td", class_="name-column")
    for row in rows:
      ranks.append(row.contents[1].text.strip())

    if 1 < len(ranks) < 15:
      logging.warn(weight_class)

    res[weight_class] = ranks
  return res


main()
