import requests, scratchapi2

def featured_japan():
    req = requests.get("https://api.scratch.mit.edu/proxy/featured")
    json = req.json()
    returns = []
    for key in ("community_featured_projects","community_most_loved_projects","community_most_remixed_projects"):
        for project in json[key]:
            user = scratchapi2.User(project["creator"], getinfo=True)
            if user.country == "Japan":
                returns.append((
                    key,
                    project["title"],
                    project["id"],
                    project["creator"]
                ))
    return returns
