
[English](https://github.com/nrysk/cgrass/blob/main/README.md) | [日本語](https://github.com/nrysk/cgrass/blob/main/README.ja.md)

![CGrass](https://raw.githubusercontent.com/nrysk/cgrass/refs/heads/main/img/github-expanded1.png)

_If you like this project, please give it a star ⭐️_


# CGrass

CGrass is a GitHub contribution image generator that can integrate with GitHub Actions. It allows you to generate a 3D image of your GitHub contributions and set it in your profile README.

## Getting Started

### GitHub Actions
Copy the following code to your `.github/workflows/cgrass.yml` file in your profile repository.

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

You can use the following code to display the generated image. Replace `<username>` with your GitHub username.
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

### 1. Create a new configuration file
Create a new configuration file in your repository. For example, create a file named `mytheme.toml` in the root of your repository.

Configuration file example: [mytheme.toml](mytheme.toml)

### 2. Link the configuration file
Link the configuration file in your workflow file by changing the `command` and `argument` values in the following code.

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

### 3. Now you can change the configuration file as you like

- The color of the ground and grass can be specified in RGBA.
- The color of the sun can be specified in RGB.

### 4. I am looking forward to your theme!

---

_If you have any idea, please share them_
