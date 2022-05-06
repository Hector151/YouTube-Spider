import requests
import csv
YOUTUBE_API_KEY = "AIzaSyB3YPSZlqFklGLpMrzkixLxqKwkOYKOB50"
Max_Results = 30
def main():
    youtube_channel_id = "UCyGUGDvCeXapYlu8FYZHFag"
    youtube_spider = YoutubeSpider(YOUTUBE_API_KEY)
    uploads_id = youtube_spider.get_channel_uploads_id(youtube_channel_id)
    video_ids = youtube_spider.get_playlist(uploads_id, max_results = Max_Results )
    f = open('output.csv', 'w', newline='')
    col_0 = ['url',"video"]
    csvWriter = csv.DictWriter(f, fieldnames = col_0)
    csvWriter.writeheader()
    for id in video_ids:
        video_info = youtube_spider.get_video(id)
        csvWriter.writerow(video_info)
    f.close()
class YoutubeSpider():
    def __init__(self, api_key):
        self.base_url = "https://www.googleapis.com/youtube/v3/"
        self.api_key = api_key
    def get_html_to_json(self, path):
        """組合 URL 後 GET 網頁並轉換成 JSON"""
        api_url = f"{self.base_url}{path}&key={self.api_key}"
        r = requests.get(api_url)
        if r.status_code == requests.codes.ok:
            data = r.json()
        else:
            data = None
        return data
    def get_channel_uploads_id(self, channel_id, part='contentDetails'):
        """取得頻道上傳影片清單的ID"""
        path = f'channels?part={part}&id={channel_id}'
        data = self.get_html_to_json(path)
        try:
            uploads_id = data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        except KeyError:
            uploads_id = None
        return uploads_id
    def get_playlist(self, playlist_id, part='contentDetails', max_results = Max_Results  ):
        """取得影片清單ID中的影片"""
        path = f'playlistItems?part={part}&playlistId={playlist_id}&maxResults={max_results}'
        data = self.get_html_to_json(path)
        if not data:
            return []
        video_ids = []
        for data_item in data['items']:
            video_ids.append(data_item['contentDetails']['videoId'])
        return video_ids
    def get_video(self, video_id, part='snippet,statistics'):
        """取得影片資訊"""
        # part = 'contentDetails,id,liveStreamingDetails,localizations,player,recordingDetails,snippet,statistics,status,topicDetails'
        path = f'videos?part={part}&id={video_id}'
        data = self.get_html_to_json(path)
        if not data:
            return {}
        data_item = data['items'][0]
        url_ = f"https://www.youtube.com/watch?v={data_item['id']}"
        info = {
            "url": url_,
            "video": data_item['snippet']['title'],
        }
        return info
if __name__ == "__main__":
    main()
# , max_results=10
# &maxResults={max_results}
    