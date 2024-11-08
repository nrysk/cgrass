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
    subparsers = parser.add_subparsers(dest="subcommand")

    themefile_parser = subparsers.add_parser("themefile")
    themefile_parser.add_argument("themefile", type=str, help="Path to the theme file")

    theme_parser = subparsers.add_parser("theme")
    theme_parser.add_argument("theme", type=str, help="Name of the theme")

    parser.add_argument(
        "-b", "--blend-file", type=str, default="./assets/objects.blend"
    )
    parser.add_argument("-t", "--theme-dir", type=str, default="./themes")
    parser.add_argument("-o", "--output-path", type=str, default="./output/output.png")
    return parser.parse_args(sys.argv[sys.argv.index("--") + 1 :])


if __name__ == "__main__":
    # 引数の読み込み
    args = parse_args()

    # 環境変数の読み込み
    github_username = os.getenv("GITHUB_USERNAME")
    github_token = os.getenv("GITHUB_TOKEN")

    # TOML ファイルの読み込み
    if args.subcommand == "themefile":
        with open(args.themefile) as f:
            config = tomllib.loads(f.read())
    elif args.subcommand == "theme":
        with open(f"{os.path.join(args.theme_dir, args.theme)}.toml") as f:
            config = tomllib.loads(f.read())

    # GitHub のデータを取得
    data = fetch_github_contributions(github_username, github_token)

    # Image 生成
    generate(args.blend_file, data, config, args.output_path)
