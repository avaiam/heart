from pprinty import pprint
import requests 
import json 

# dic={"ava": {{"bmw": {2023, 2020}}, {"toyota"}},
#      "paria": "porche",
#      "ostad": "peraid"}


r = requests.get("https://api.github.com")
print(r.content)
# https://www.google.com/search?q=ava+mirzakhani&tbm=isch&ved=2ahUKEwjGsou--Z2AAxXxmCcCHZZnC7sQ2-cCegQIABAA&oq=ava+mirzakhani&gs_lcp=CgNpbWcQAzIECCMQJ1DdBliKCmCrDWgAcAB4AIAB0gGIAesEkgEDMi0zmAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=d4G5ZIabI_GxnsEPls-t2As&bih=757&biw=1440
# https://www.google.com/search?q=paria+mirapftab&tbm=isch

