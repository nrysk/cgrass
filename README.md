# cgrass (Contribution to Grass)

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

You can use the following code to display the generated image.
```
![Contribution to Grass](https://raw.githubusercontent.com/<username>/<username>/refs/heads/output/output.png)
```

## Themes
### github theme
![github theme](img/github.png)

```yaml
  - name: Generate Picture
    uses: nrysk/cgrass@v1.0.0
    with:
        github_username: ${{ github.repository_owner }}
        github_token: ${{ secrets.GITHUB_TOKEN }}
        output_path: output/output.png
        command: "theme"
        argument: "github" # change here
```

### github-nograss theme
![github-nograss theme](img/github-nograss.png)

```yaml
  - name: Generate Picture
    uses: nrysk/cgrass@v1.0.0
    with:
        github_username: ${{ github.repository_owner }}
        github_token: ${{ secrets.GITHUB_TOKEN }}
        output_path: output/output.png
        command: "theme"
        argument: "github-nograss" # change here
```

### planet theme
![planet theme](img/planet.png)

```yaml
  - name: Generate Picture
    uses: nrysk/cgrass@v1.0.0
    with:
        github_username: ${{ github.repository_owner }}
        github_token: ${{ secrets.GITHUB_TOKEN }}
        output_path: output/output.png
        command: "theme"
        argument: "planet" # change here
```

### planet-nograss theme
![planet-nograss theme](img/planet-nograss.png)

```yaml
  - name: Generate Picture
    uses: nrysk/cgrass@v1.0.0
    with:
        github_username: ${{ github.repository_owner }}
        github_token: ${{ secrets.GITHUB_TOKEN }}
        output_path: output/output.png
        command: "theme"
        argument: "planet-nograss" # change here
```

## Make your own theme

### 1. Create a new configuration file
Create a new configuration file in your repository. For example, create a file named `mytheme.toml` in the root of your repository.

Configuration file example: [config.toml](config.toml)

### 2. Link the configuration file
Link the configuration file in your workflow file.

```yaml
  - name: Generate Picture
    uses: nrysk/cgrass@main
    with:
        github_username: ${{ github.repository_owner }}
        github_token: ${{ secrets.GITHUB_TOKEN }}
        output_path: output/output.png
        command: "themefile" # change here
        argument: ${{ github.workspace }}/mytheme.toml # change here
```

### 3. Now you can change the configuration file as you like

### I am looking forward to your theme!
