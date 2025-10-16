import requests
q = {"query":"query{ reportsAnalytics { total byStatus { clave valor } } }"}
r = requests.post("http://localhost:4000/graphql", json=q, timeout=5)
print(r.status_code, r.text)
