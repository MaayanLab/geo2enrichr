var SERVER = "https://amp.pharm.mssm.edu/g2e/";

/**
 * A url encode serializer, it works at most depth 2 because I can't be bothered to get a real library for this.
 */
var serialize = function(obj) {
  var str = [];
  for (var p in obj)
    if (obj.hasOwnProperty(p)) {
      if (typeof obj[p] === 'object') {
        if (Array.isArray(obj[p])) {
          for (var pp in obj[p]) {
            str.push(encodeURIComponent(p + '[]') + "=" + encodeURIComponent(obj[p][pp]));
          }
        } else {
          for (var pp in obj[p]) {
            str.push(encodeURIComponent(p + '[' + pp + ']') + "=" + encodeURIComponent(obj[p][pp]));
          }
        }
      } else {
        str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
      }
    }
  return str.join("&");
}

// Watch for content_script requests, make them and return them to get around CORB
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if (request.query === 'api/extract/geo') {
      fetch(SERVER + 'api/extract/geo', {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow',
        referrer: 'no-referrer',
        body: serialize(request.body),
      })
        .then((response) => response.text())
        .then(sendResponse)
        .catch((error) => sendResponse(JSON.stringify({ error })));
    } else if (request.query === 'crowdsourcing/check_geo') {
      fetch('https://maayanlab.net/crowdsourcing/check_geo.php', {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow',
        referrer: 'no-referrer',
        body: JSON.stringify(request.body),
      })
        .then((response) => response.text())
        .then(sendResponse)
        .catch((error) => sendResponse(JSON.stringify({ error })));
    } else if (request.query === 'api/check_duplicate') {
      fetch(SERVER + 'api/check_duplicate?' + serialize(request.body), {
        method: 'GET',
        mode: 'cors',
        cache: 'no-cache',
        redirect: 'follow',
        referrer: 'no-referrer',
      })
        .then((response) => response.text())
        .then(sendResponse)
        .catch((error) => sendResponse(JSON.stringify({ error })));
    } else if (request.query === 'Enrichr/json/genemap.json') {
      fetch('https://amp.pharm.mssm.edu/Enrichr/json/genemap.json', {
        method: 'GET',
        mode: 'cors',
        cache: 'no-cache',
        redirect: 'follow',
        referrer: 'no-referrer',
      })
        .then((response) => response.text())
        .then(sendResponse)
        .catch((error) => {
          console.error(error);
          sendResponse(JSON.stringify({ error }))
        });
    } else {
      return false
    }
    return true
  }
)