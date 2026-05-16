import requests

data = {
    "firstname": "Jim",
    "lastname": "Brown",
    "totalprice": 111,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2025-01-04",
        "checkout": "2025-01-15"
    },
    "additionalneeds": "Breakfast"
}
URL = 'https://restful-booker.herokuapp.com/booking'


def test_create_booking():

    response = requests.post(URL, json=data)
    assert response.status_code == 200
    assert "bookingid" in response.json()
    assert isinstance(response.json()["bookingid"], int)

    booking_id = response.json()["bookingid"]
    get_response = requests.get(f"{URL}/{booking_id}")

    assert response.status_code == 200
    assert get_response.json()["firstname"] == data["firstname"]