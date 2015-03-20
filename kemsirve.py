from __future__ import print_function

import requests
import Tkinter
import tkMessageBox

window = Tkinter.Tk()
window.wm_withdraw()

resp = requests.get("https://ws.ovh.com/dedicated/r2/ws.dispatcher/getAvailability2")
for i in resp.json()["answer"]["availability"]:
    if i["reference"] in ["150sk10", "150sk20"]:
        for j in i["metaZones"]:
            if j["availability"] not in ["unavaible", "unknown"]:
                print(j["zone"], j["availability"])
                tkMessageBox.showinfo(title="Greetings", message="%s - %s!" % (j["zone"], j["availability"]))
