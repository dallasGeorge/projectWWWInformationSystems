import requests
import json

# Define the data for the new product
data = {
  "_id": {
    "$oid": "665bf412d8f7b1074e2b03c1"
  },
  "name": "test",
  "production_Year": 212,
  "price": 21,
  "color": 3,
  "size": 4
}
# Make a POST request to your Flask endpoint
response = requests.post("http://127.0.0.1:5000/content-based-filtering", json=data)

# Print the response
print(response.json())
