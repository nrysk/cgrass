import json
from dataclasses import dataclass

import requests


@dataclass
class ContributionData:
    total_contributions: int
    total_weeks: int
    count_matrix: list[list[int]]
    level_matrix: list[list[str]]


def fetch_github_contributions(username: str, token: str) -> ContributionData:
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

    calender = (
        response.json()
        .get("data")
        .get("user")
        .get("contributionsCollection")
        .get("contributionCalendar")
    )
    total_contributions = calender.get("totalContributions")
    total_weeks = len(calender.get("weeks"))
    count_matrix = [
        [day.get("contributionCount") for day in week.get("contributionDays")]
        for week in calender.get("weeks")
    ]
    level_matrix = [
        [day.get("contributionLevel") for day in week.get("contributionDays")]
        for week in calender.get("weeks")
    ]

    return ContributionData(
        total_contributions, total_weeks, count_matrix, level_matrix
    )


if __name__ == "__main__":
    import os

    import dotenv

    username = os.getenv("GITHUB_USERNAME")
    token = os.getenv("GITHUB_TOKEN")

    data = fetch_github_contributions(username, token)

    print(data.total_contributions)
    print(data.total_weeks)
    print(data.count_matrix)
    print(data.level_matrix)
