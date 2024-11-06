import argparse
import math
import os
import random
import sys
import tomllib

sys.path.append(os.path.dirname(__file__))
from blend import generate
from fetch import fetch_github_contributions


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b", "--blend-file", type=str, default="./assets/objects.blend"
    )
    parser.add_argument("-c", "--config-file", type=str, default="./config.toml")
    return parser.parse_args(sys.argv[sys.argv.index("--") + 1 :])


if __name__ == "__main__":
    # 引数の読み込み
    args = parse_args()

    # 環境変数の読み込み
    github_username = os.getenv("GITHUB_USERNAME")
    github_token = os.getenv("GITHUB_TOKEN")

    # TOML ファイルの読み込み
    with open(args.config_file, mode="rb") as f:
        config = tomllib.load(f)

    # GitHub のデータを取得
    data = fetch_github_contributions(github_username, github_token)

    # Image 生成
    generate(args.blend_file, data, config)
