import reader
from datetime import datetime
from typing import List, Dict

def get_feed_content(rss_url: str) -> List[Dict[str, str]]:
    try:
        r = reader.make_reader()
        
        r.add_feed(rss_url)

        r.update_feeds()
        
        entries = list(r.get_entries())
        
        feed_content = []
        for entry in entries:
            if entry.published:
                date_str = entry.published.strftime("%Y-%m-%d")
            elif entry.updated:
                date_str = entry.updated.strftime("%Y-%m-%d")
            else:
                date_str = datetime.now().strftime("%Y-%m-%d")
            
            feed_content.append({
                "title": entry.title or "",
                "date": date_str,
                "url": entry.link or ""
            })
        
        return feed_content
        
    except Exception as e:
        print(f"Error parsing RSS feed {rss_url}: {str(e)}")
        return []