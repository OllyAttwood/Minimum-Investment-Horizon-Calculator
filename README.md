## Introduction
A Python program to view the probabilities of making a profit investing in various stock market indices over different timescales, based on historical data. It allows the user to specify what profit percentage they are aiming for and adjust for inflation. The software is built using Pandas, NumPy and Matplotlib, as well as unit testing with Pytest.

## Demo Gifs

### Ability To Compare Different Stock Market Indices
![Indices Demo Gif](https://d8o2c393pu2d1.cloudfront.net/a24kml%2Fpreview%2F68193652%2Fmain_large.gif?response-content-disposition=inline%3Bfilename%3D%22main_large.gif%22%3B&response-content-type=image%2Fgif&Expires=1750199868&Signature=KXTewdU2PsqeHRXjeGd7snBrpph4bxWf3PfEHQ4D2hNsbqND444jDeU3zeJ9HwcRv1GJkseNehzZw05xp~9lTkFk~Ip3Xr1Kl7k-~y5lxLy36rkZAmS4KLwRRlC18eMP-~PmL-BO1YPUpT6kaVhrJlS0ZS3mOFvIS6ofBiD-CaKX3fZ5zLKtvYB2jl0H49dFwOvUVRtRcZNeyI9QFaXRzkxhhvXS3r5YT434UehOiSN0g6tkuZwZPViadHy2j8D155DCBHKkPndhLLxp7HVq4qwvn2UEpIIm2skrVXKTTpWsQtaGr2ujcJqk1IH0Nb2TN6qkw5UCCS82pWgTBYnB1w__&Key-Pair-Id=APKAJT5WQLLEOADKLHBQ)

### Graph Changes Animation
When changes are made to the graph via the minimum profit threshold textbox or the inflation textbox, the lines are smoothly updated to aid interpretability.
![Animation Demo Gif](https://d33ob2al3ysfjw.cloudfront.net/m1piml%2Fpreview%2F68193601%2Fmain_large.gif?response-content-disposition=inline%3Bfilename%3D%22main_large.gif%22%3B&response-content-type=image%2Fgif&Expires=1750199906&Signature=MsoMp19WGbl9PC8jhKa9CQZtfiUsGRu5P-a~Tw19XE~FGA0REu2LD2FbP4TKDTPCKYF-sr43bIM1YN2UPqx~-rVpdICgQCo651SRP11E2e556VC3MNivCUe-9PKKW5Ctb0RMQmcYh~mLyyAIF5derUL~l785KTu-AtCMlZhpAF09o5hJJmGv4ZMdcQUQ9CwbCAbQzMsLwklvCHgfSA-UEwqNDlgIE-sFFRte2K9kopyQ~pX4wgc~y3lo48AEEhbHx5G84qmtoJE8XuLsgwsVeW46dBTOAKx9rGs7ctgO379yQTaIzczsyv2vAPFg8u7j1k3MubVprg0lo9xGfmxI3Q__&Key-Pair-Id=APKAJT5WQLLEOADKLHBQ)

### Index Data Popups
These popups show the best-performing, worst-performing, and median periods of the selected period size and index (values are adjusted for the provided inflation value). The popups are colour-coded for easy recognition with the corresponding index.
![Popup Demo Gif](https://dgqh380xariug.cloudfront.net/f46kml%2Fpreview%2F68193654%2Fmain_large.gif?response-content-disposition=inline%3Bfilename%3D%22main_large.gif%22%3B&response-content-type=image%2Fgif&Expires=1750199874&Signature=bNNMrd2vOjGpwLdl7Z1HzQfN-tbvX88ibL3enzAcZH5M8Un5HtJ1lF7NmXDI8~urhtFlGrtM8kQm8FlN-FfC-X98D-uddmmuaUIADUT3w3tJ~64JTo4r2MpwfVa83oblSoDF~tYZ7ZX6S-X5F2O7kJm9RswKuIAs786jdoPHmow45D~Hc1YiY-UEDm6Mlp4NnUu6xLpfr88GT746O4fIssVmIYpPrwCMIxuEd7umb05dtgrEhUl7Z-ZWmCoLeOxre6AgJ6kqQ1MR0nq3eRjpVHszYHxSp4q5uv0yU5n664lIBaUNpbdxXLd~k2F8kU2Ki2RHSTQB2qZLJaATzSHGMg__&Key-Pair-Id=APKAJT5WQLLEOADKLHBQ)
