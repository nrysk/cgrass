import argparse
import math
import os
import random
import sys

sys.path.append(os.path.dirname(__file__))
from blend import generate
from fetch import fetch_github_contributions


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b", "--blend-file", type=str, default="./assets/objects.blend"
    )
    return parser.parse_args(sys.argv[sys.argv.index("--") + 1 :])


if __name__ == "__main__":
    # 引数の読み込み
    args = parse_args()
    blend_file = args.blend_file

    # 環境変数の読み込み
    github_username = os.getenv("GITHUB_USERNAME")
    github_token = os.getenv("GITHUB_TOKEN")

    # GitHubのデータを取得
    data = fetch_github_contributions(github_username, github_token)

    # Image 生成
    generate(blend_file, data)
