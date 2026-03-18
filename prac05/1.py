import re
import json


with open("raw.txt", "r") as file:
    text = file.read()


prices = re.findall(r"\d+\.\d{2}", text)
prices = [float(p) for p in prices]


products = []
lines = text.split("\n")

for line in lines:
    match = re.match(r"([A-Za-z ]+)\s+(\d+\.\d{2})", line)
    if match:
        product = match.group(1).strip()
        products.append(product)


calculated_total = sum(prices)


date_match = re.search(r"\d{4}-\d{2}-\d{2}", text)
date = date_match.group() if date_match else None


time_match = re.search(r"\d{2}:\d{2}", text)
time = time_match.group() if time_match else None


payment = None
if "Card" in text:
    payment = "Card"
elif "Cash" in text:
    payment = "Cash"


data = {
    "products": products,
    "prices": prices,
    "total": calculated_total,
    "date": date,
    "time": time,
    "payment": payment
}


print(json.dumps(data, indent=4))