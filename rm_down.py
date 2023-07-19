import os
import requests

repo_owner = "Fndroid"
repo_name = "clash_for_windows_pkg"
download_directory = "/root/data/本地存储/科学上网/Clash"

def get_latest_release_download_urls():
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        release_info = response.json()
        assets = release_info.get("assets")
        if assets:
            download_urls = []
            for asset in assets:
                download_url = asset.get("browser_download_url")
                if download_url.endswith(".exe"):
                    download_urls.append(download_url)
            return download_urls
    return None

def download_latest_release():
    download_urls = get_latest_release_download_urls()
    if download_urls:
        # 删除目标文件夹下的所有文件
        for file_name in os.listdir(download_directory):
            file_path = os.path.join(download_directory, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        
        # 下载最新发布的文件到指定路径
        for download_url in download_urls:
            response = requests.get(download_url)
            if response.status_code == 200:
                file_name = download_url.split("/")[-1]
                file_path = os.path.join(download_directory, file_name)
                with open(file_path, "wb") as file:
                    file.write(response.content)
                print(f"已下载文件: {file_name}")
            else:
                print(f"无法下载文件: {download_url}")
        print("所有文件下载完成")
    else:
        print("无法获取最新发布的下载链接或下载失败")

download_latest_release()
