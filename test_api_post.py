import pytest
from constants import BASE_URL

class TestBookings:
    def test_create_booking(self, auth_session, booking_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data["totalprice"], "Заданная стоимость не совпадает"

        # Проверяем, что бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"

        # Удаляем бронирование
        deleted_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не удалилась"

        # Проверяем, что бронирование больше недоступно
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 404, "Бронь не удалилась"

    #PUT
    def test_booking_update(self, auth_session, booking_data):
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ресурс не обновлён"
        booking_id = create_booking.json().get("bookingid")

        updated_data = {
            "firstname": "Updated",
            "lastname": "User",
            "totalprice": 999,
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2025-06-01",
                "checkout": "2025-06-10"
            },
            "additionalneeds": "Lunch"
        }

        put_response = auth_session.put(
            f"{BASE_URL}/booking/{booking_id}",
            json=updated_data
        )
        assert put_response.status_code == 200

        get_response = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_response.json()["firstname"] == updated_data["firstname"]
        assert get_response.json()["lastname"] == updated_data["lastname"]


    # PATCH
    def test_booking_patch(self, auth_session, booking_data):
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Изменения не внесены"
        booking_id = create_booking.json().get("bookingid")

        updated_data = {
            "additionalneeds": "Brunch"
        }

        patch_response = auth_session.patch(f"{BASE_URL}/booking/{booking_id}", json=updated_data)
        assert patch_response.status_code == 200
        get_response = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_response.json()["additionalneeds"] == updated_data["additionalneeds"]
        assert get_response.json()["firstname"] == booking_data["firstname"]

    # Negative cases
    def test_negative_cases(selfself, auth_session, booking_data):
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        