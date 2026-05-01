from typing import Dict


def reverse_image_search(image_url: str) -> Dict:
    # Configurable public endpoints.
    return {
        "image_url": image_url,
        "providers": [
            {"name": "Google Lens", "query_url": f"https://lens.google.com/uploadbyurl?url={image_url}"},
            {"name": "Bing Visual Search", "query_url": f"https://www.bing.com/images/search?q=imgurl:{image_url}&view=detailv2&iss=sbi"},
            {"name": "TinEye", "query_url": f"https://tineye.com/search?url={image_url}"},
        ],
        "note": "Open query URLs in browser or integrate provider APIs if keys are available.",
    }
