import json

import folium
from flask import Flask, send_from_directory
from geopy import distance
from yandex_geocoder import Client


app = Flask(__name__)


def collect_bars(bars, customer):
    bars_collection = []
    for bar in bars:
        customer_distance = distance.distance(
            customer, (bar["Latitude_WGS84"], bar["Longitude_WGS84"])
        ).km
        bars_collection.append(
            {
                "title": bar["Name"],
                "longitude": bar["Longitude_WGS84"],
                "latitude": bar["Latitude_WGS84"],
                "distance": customer_distance,
            }
        )
    return bars_collection


def get_bar_distance(bars):
    return bars["distance"]


def draw_map(bars, customer):
    bar_map = folium.Map(location=customer, zoom_start=16)
    folium.Marker(
        location=customer, popup="You", icon=folium.Icon(color="red", icon="user")
    ).add_to(bar_map)

    for bar in bars:
        folium.Marker(
            location=[bar["latitude"], bar["longitude"]],
            popup=f"{bar['title']}",
            icon=folium.Icon(icon="glass"),
        ).add_to(bar_map)

    bar_map.save("index.html")
    return None


@app.route("/")
def show_map():
    return send_from_directory("", "index.html")


if __name__ == "__main__":

    with open("data-2897-2019-07-10.json", encoding="cp1251") as fh:
        bars_data = json.load(fh)

    customer_location = input("Enter your location: ")
    customer_coord = Client.coordinates(customer_location)[::-1]

    bars_collection = collect_bars(bars_data, customer_coord)
    closest_bars = sorted(bars_collection, key=get_bar_distance)[:5]

    draw_map(closest_bars, customer_coord)

    app.run()
