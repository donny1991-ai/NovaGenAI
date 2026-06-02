import urllib.request, json, time

# API key
p1 = "821856b7d34f3877"
p2 = "0cce9b569079e7a3"
API_KEY = p1 + p2

task_ids = {
    "healthcare-ai": "42eb06611aae0541455bce81000e094d",
    "ai-agents": "187bda9666778d25bb34eb99a6312005",
    "ai-automation": "dfa633cea3d0793d29bb9bec4e5a43df",
    "ai-company": "17c7d2b588fa12c9fca400f11690a384"
}

results = {}
results["enterprise-ai"] = "https://tempfile.aiquickdraw.com/vnp/b54eec14b0247360f9647c1b7a31d875_1780317424.jpeg"

for attempt in range(6):
    pending = {k: v for k, v in task_ids.items() if k not in results}
    if not pending:
        break
    print(f"Attempt {attempt+1} - {len(pending)} pending...")
    time.sleep(12)
    for page, tid in list(pending.items()):
        url = f"https://api.kie.ai/api/v1/jobs/recordInfo?taskId={tid}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {API_KEY}"})
        try:
            data = json.loads(urllib.request.urlopen(req).read())
            state = data["data"]["state"]
            if state == "success":
                rj = json.loads(data["data"]["resultJson"])
                results[page] = rj["resultUrls"][0]
                print(f"  OK {page}")
            elif state == "fail":
                print(f"  FAIL {page}: {data['data'].get('failMsg','')}")
            else:
                print(f"  ... {page}: {state}")
        except Exception as e:
            print(f"  ERR {page}: {e}")

print("\n=== RESULTS ===")
for page, url in sorted(results.items()):
    print(f"{page}: {url}")
