from typing import List

import matplotlib.pyplot as plt

from droplet import Droplet


def calc_drag_coefficient_list(droplet: Droplet, func_name: str,
                               list_Rep: List):
    list_Cd = []
    for Rep in list_Rep:
        droplet.Rep = Rep
        method_to_call = getattr(droplet, func_name)
        list_Cd.append(method_to_call())
    return list_Cd


drop = Droplet()

list_Rep = list(range(1, 51))
list_Cd_SN = calc_drag_coefficient_list(
    drop, "schiller_and_naumann_1935", list_Rep
)
list_Cd_FM = calc_drag_coefficient_list(
    drop, "feng_and_michaelides_2001", list_Rep
)

plt.style.use("fivethirtyeight")
fig, ax = plt.subplots()
ax.plot(list_Rep, list_Cd_SN, label="Schiller e Naumman")
ax.plot(list_Rep, list_Cd_FM, label="Feng e Michaelides")
ax.legend()
