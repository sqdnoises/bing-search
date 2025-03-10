> [!WARNING]
> This code no longer gives you points and is no longer maintained, however it is still available for anyone to view and learn something.

---

# Bing auto-search queries
Ever wanted to automatically search on Bing? Maybe you did, because you want the points for Bing Rewards automatically.

Well this program is the perfect showcase of how you can automatically search random keywords on a search engine easily!

**This is a POC (proof of concept) to demonstrate how easy it is to automate browsers.**

## Requirements
- **Python 3.10.x** or above (haven't tested on earlier versions)

### Steps to setup
1. Download or clone this repository to a folder
    - If you have `git` installed:
        ```
        git clone https://github.com/sqdnoises/bing-search.git
        ```
    - If you don't have `git` installed:
      1. Click the <kbd>Code</kbd> button above the Commits history, then click [<kbd>Download ZIP</kbd>](https://github.com/sqdnoises/bing-search/archive/refs/heads/main.zip) (👈 or you can just click this to download the ZIP).
      2. Extract the ZIP file into a folder.

> [!IMPORTANT]
> Make sure to run the command in Step **2.** and commands in section [**How to run & use**](#how-to-run--use) in a terminal opened in the same folder where the files you downloaded/cloned are at.

2. Once you have installed Python, you need to install the dependencies from `requirements.txt` using:
    ```sh
    pip install -r requirements.txt
    ```

3. Now install the playwright browsers using:
    ```sh
    playwright install
    ```

Now everything is set-up.

## How to run & use
> [!IMPORTANT]
> If you are on Windows, use `python` instead of `python3` as used in the commands below.

### Signing into Bing
Run the command:
```sh
python3 bing-search.py signin
```

This will launch a chromium browser with an open tab with [bing.com](https://bing.com/) open, sign into Bing from there and come back to the terminal and press enter to save the cookies.

If successfully done, the output will be something like this:
```
Please sign in to your Microsoft account.
Once signed in, press Enter to save cookies and exit.

Cookies saved successfully!
```

### Running
To start searching automatically use:
```sh
python3 bing-search.py start
```

This opens up the browser, loads up 5 empty tabs, and starts searching random keywords one by one in each tab and closes them.

Basically, it searches 5 times by default.\
If you want to make it search more than 5 times, use:
```sh
python3 bing-search.py start amount
```
> *Where amount is an integer.*

Here `amount` can be any number greater than 0 and it will open that many tabs and start searching.

The successful output may look like this:
```
$ python3 bing-search.py start
Performing searches: 100%|███████████████████████████████████████████████████████| 5/5 [00:27<00:00,  5.52s/search]
Search session complete!
Attempted queries:
- point government newspaper interface encryption fire allow
- house development privacy
- cryptocurrency argue earth number
- bake digital mountain
- library office watch planet allow application
Browser session closed.
```

## LICENSE
[![](https://img.shields.io/badge/LICENSE-MIT-red?style=for-the-badge&labelColor=black)](LICENSE)\
Click **[<kbd>MIT License</kbd>](LICENSE)** to view the license that comes with this program.
