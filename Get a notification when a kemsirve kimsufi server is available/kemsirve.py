from __future__ import print_function

import requests
try:
    import Tkinter as tk
    import tkMessageBox as tkm
except Exception:
    import tkinter as tk
    from tkinter import messagebox as tkm


window = tk.Tk()
window.wm_withdraw()

resp = requests.get("https://ws.ovh.com/dedicated/r2/ws.dispatcher/getAvailability2")
for i in resp.json()["answer"]["availability"]:
    if i["reference"] in ["150sk10", "150sk20"]:
        for j in i["metaZones"]:
            if j["availability"] not in ["unavaible", "unknown"]:
                print(j["zone"], j["availability"])
                tkm.showinfo(title="Greetings",
                             message="%s: %s - %s!" % (i["reference"],
                                                       j["zone"],
                                                       j["availability"]))