[English](https://github.com/nrysk/cgrass/blob/main/README.md) | [日本語](https://github.com/nrysk/cgrass/blob/main/README.ja.md)

![CGrass](https://raw.githubusercontent.com/nrysk/cgrass/refs/heads/main/img/github-expanded1.png)

_スターをして頂けると励みになります ⭐️_

# CGrass

CGrass は GitHub Actions 上で動作する GitHub Contribution 画像生成ツールです. 生成された 3D 画像をプロフィールの README に設定することができます.

## Getting Started

### GitHub Actions
あなたの Profile リポジトリの `.github/workflows/cgrass.yml` に以下のコードをコピーしてください。

```yaml
name: Generate Picture and Push to output branch

on:
    push:
        branches:
            - main
    schedule:
        - cron: '0 0 * * *' # any time you want
    
permissions:
    contents: write

jobs:
    generate:
        runs-on: ubuntu-24.04

        steps:
          - name: Checkout
            uses: actions/checkout@v4

          - name: Generate Picture
            uses: nrysk/cgrass@v1.0.0
            with:
                github_username: ${{ github.repository_owner }}
                github_token: ${{ secrets.GITHUB_TOKEN }}
                output_path: output/output.png
                command: "theme"
                argument: "github"

          - name: Push output image to output branch
            uses: crazy-max/ghaction-github-pages@v4
            with:
                target_branch: output
                build_dir: output
                commit_message: "Generate Output Image"
            env:
                GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

以下のコードで生成された画像を表示できます。`<username>` は GitHub のユーザ名で置き換えてください.
```
![Contribution to Grass](https://raw.githubusercontent.com/<username>/<username>/refs/heads/output/output.png)
```

## Themes
### ☘️ github theme

![github theme](https://raw.githubusercontent.com/nrysk/cgrass/refs/heads/main/img/github.png)

```yaml
command: "theme"
argument: "github" # change here
```

### ☘️ github-nograss theme
![github-nograss theme](https://raw.githubusercontent.com/nrysk/cgrass/refs/heads/main/img/github-nograss.png)

```yaml
command: "theme"
argument: "github-nograss" # change here
```

### 🪐 planet theme
![planet theme](https://raw.githubusercontent.com/nrysk/cgrass/refs/heads/main/img/planet.png)

```yaml
command: "theme"
argument: "planet" # change here
```

### 🪐 planet-nograss theme
![planet-nograss theme](https://raw.githubusercontent.com/nrysk/cgrass/refs/heads/main/img/planet-nograss.png)

```yaml
command: "theme"
argument: "planet-nograss" # change here
```

## Make your own theme

### 1. 設定ファイルを作成します
Profile リポジトリに設定ファイルを作成します. 例えば, `mytheme.toml` というファイルをリポジトリのルートに作成します.

コンフィグファイル例: [mytheme.toml](mytheme.toml)

### 2. 設定ファイルをリンクします
`.github/workflows/cgrass.yml` の `command` と `argument` を変更します.

```yaml
  - name: Generate Picture
    uses: nrysk/cgrass@v1.0.0
    with:
        github_username: ${{ github.repository_owner }}
        github_token: ${{ secrets.GITHUB_TOKEN }}
        output_path: output/output.png
        command: "themefile" # change here
        argument: ${{ github.workspace }}/mytheme.toml # change here
```

### 3. 後は好きなように設定ファイルを変更してください

- ground と grass の色は RGBA で指定します.
- sun の色は RGB で指定します.

### 4. 面白いテーマができるのを楽しみにしています！

---

_アイデアがあれば, 共有していただけると幸いです_
