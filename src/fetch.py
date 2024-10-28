import json

import requests


def fetch_github_contributions(username: str, token: str):
    url = "https://api.github.com/graphql"
    query = f"""
        query {{
            user(login: "{username}") {{
                contributionsCollection {{
                    contributionCalendar {{
                        totalContributions
                        weeks {{
                            contributionDays {{
                                contributionCount
                                contributionLevel
                                date
                            }}
                        }}
                    }}
                }}
            }}
        }}
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, json={"query": query})

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from GitHub: {response.text}")

    return json.loads(response.text)


if __name__ == "__main__":
    import os

    import dotenv

    username = os.getenv("GITHUB_USERNAME")
    token = os.getenv("GITHUB_TOKEN")

    data = fetch_github_contributions(username, token).get("data")

    total_contributions = (
        data.get("user")
        .get("contributionsCollection")
        .get("contributionCalendar")
        .get("totalContributions")
    )

    total_weeks = len(
        data.get("user")
        .get("contributionsCollection")
        .get("contributionCalendar")
        .get("weeks")
    )

    first = (
        data.get("user")
        .get("contributionsCollection")
        .get("contributionCalendar")
        .get("weeks")[0]
    )

    matrix = [
        [day.get("contributionLevel") for day in week.get("contributionDays")]
        for week in data.get("user")
        .get("contributionsCollection")
        .get("contributionCalendar")
        .get("weeks")
    ]

    print(f"Total contributions: {total_contributions}")
    print(f"Total weeks: {total_weeks}")
    print(f"First week: {first}")
    print(f"Matrix Size: {len(matrix)}x{len(matrix[0])}")
