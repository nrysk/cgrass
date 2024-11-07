import json
from dataclasses import dataclass
from enum import StrEnum

import requests


class ContributionLevel(StrEnum):
    NONE = "none"
    FIRST_QUARTILE = "first_quartile"
    SECOND_QUARTILE = "second_quartile"
    THIRD_QUARTILE = "third_quartile"
    FOURTH_QUARTILE = "fourth_quartile"

    @classmethod
    def from_str(cls, level: str) -> "ContributionLevel":
        return {
            "NONE": cls.NONE,
            "FIRST_QUARTILE": cls.FIRST_QUARTILE,
            "SECOND_QUARTILE": cls.SECOND_QUARTILE,
            "THIRD_QUARTILE": cls.THIRD_QUARTILE,
            "FOURTH_QUARTILE": cls.FOURTH_QUARTILE,
        }[level]


@dataclass
class ContributionData:
    total_contributions: int
    total_weeks: int
    count_matrix: list[list[int]]
    level_matrix: list[list[ContributionLevel]]


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
        [
            ContributionLevel.from_str(day.get("contributionLevel"))
            for day in week.get("contributionDays")
        ]
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
