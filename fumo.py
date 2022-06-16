FUMO_DICT = {
  "Hakurei Reimu": "Reimu",
  "Kirisame Marisa": "Marisa",
  "Izayoi Sakuya": "Sakuya",
  "Remilia Scarlet": "Remilia",
  "Patchouli Knowledge": "Patchouli",
  "Alice Margatroid": "Alice",
  "Flandre Scarlet": "Flandre",
  "Kochiya Sanae": "Sanae",
  "Cirno": "Cirno",
  "Moriya Suwako": "Suwako",
  "Konpaku Youmu": "Youmu",
  "Saigyouji Yuyuko": "Yuyuko",
  "Hong Meiling": "Meiling", 
  "Chen": "Chen",
  "Yakumo Ran": "Ran",
  "Yakumo Yukari": "Yukari",
  "Houraisan Kaguya": "Kaguya",
  "Fujiwara no Mokou": "Mokou",
  "Komeiji Satori": "Satori",
  "Komeiji Koishi": "Koishi",
  "Reisen Udongein Inaba": "Reisen",
  "Inaba Tewi": "Tewi",
  "Hata no Kokoro": "Kokoro",
  "Ibaraki Kasen": "Kasen",
  "Shameimaru Aya": "Aya",
  "Himekaidou Hatate": "Hatate",
  "Hinanawi Tenshi": "Tenshi",
  "Yorigami Shion": "Shion",
  "Kazami Yuuka": "Yuuka",
  "Inubashiri Momiji": "Momiji",
  "Eirin Yagokoro": "Eirin",
  "Rumia": "Rumia",
  "Shiki Eiki Yamaxanadu": "Eiki",
  "Kawashiro Nitori": "Nitori",
  "Joon Yorigami": "Joon",
  "Usami Renko": "Renko",
  "Toyosatomimi no Miko": "Toyosatomimi"
}


def getFumoKey(fumoName):
    for name, key in FUMO_DICT.items():
        if fumoName.capitalize() in name.split():
            return key

    return ''