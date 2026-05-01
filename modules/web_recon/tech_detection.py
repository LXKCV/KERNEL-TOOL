from .common import fetch_url

SIGNATURES = {
    "WordPress": ["wp-content", "wp-includes"],
    "Drupal": ["/sites/default/", "drupal-settings-json"],
    "Joomla": ["/media/system/js/", "Joomla!"],
    "React": ["react", "__REACT_DEVTOOLS_GLOBAL_HOOK__"],
    "Vue.js": ["vue", "data-v-"],
    "Angular": ["ng-version", "angular.js"],
    "jQuery": ["jquery"],
    "Bootstrap": ["bootstrap"],
}


def detect_technologies(url: str) -> dict:
    result = fetch_url(url)
    haystack = (result.body + "\n" + "\n".join(f"{k}:{v}" for k, v in result.headers.items())).lower()
    found = [name for name, markers in SIGNATURES.items() if any(m.lower() in haystack for m in markers)]
    return {
        "final_url": result.url,
        "status_code": result.status_code,
        "technologies": sorted(found),
    }
