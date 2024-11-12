from no_1.service_a import ServiceA
from no_1.service_b import ServiceB

service_a = ServiceA()
for i in range(10):
    service_a.send_data(
        {"user_id": i, "user_data": f"Очень полезная информация № {i}"}
    )

service_b = ServiceB()
service_b.run_listening()
