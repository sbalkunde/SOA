from django.shortcuts import render
import requests

def get_media(request):
    token = 'IGQWRNSUpCTUMtSnVJal92cFU0Tm9feGFFVExNZAHBvRnotbEFNZAEI3am0waU90czZAod0d4ZAHFHeGQwV3BCWGJyNnlnQzhsTUY5bnoxNEFuN1p5YjlEMjRRTHVFUjMwQ1B2NzNrdm9UcWF2RGVXX0ZAhUWhhdU92VmZADYWpKbUFvMjJSaWsZD'
    url = f'https://graph.instagram.com/me/media?fields=id,caption&access_token={token}'

    response = requests.get(url)
    data = response.json()
    
    # Check if 'data' key exists in response to avoid KeyError
    if 'data' in data:
        all_media = data['data']
        output = []

        for media in all_media:
            media_id = media["id"]
            media_uri = f'https://graph.instagram.com/{media_id}?fields=id,media_type,media_url,username,timestamp&access_token={token}'
            response = requests.get(media_uri)
            media_data = response.json()
            
            # Update media dictionary with new fields
            media["url"] = media_data.get("media_url")
            media["type"] = media_data.get("media_type")
            media["username"] = media_data.get("username")
            media["timestamp"] = media_data.get("timestamp")
        
        return render(request, 'instagram.html', { "all_media": all_media })
    
    
    



   