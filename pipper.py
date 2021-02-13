import requests as req

def main():
    res = req.get("https://pypi.org/simple/", stream = True)

    for content in res.iter_content(chunk_size = 1024):
        print(content)

if __name__ == "__main__":
    main()