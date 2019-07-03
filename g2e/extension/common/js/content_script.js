// Use this to forward requests through the background script
function post_through_background(params) {
  var query = params.query;
  var body = params.body;
  return new Promise(function (resolve, reject) {
    chrome.runtime.sendMessage(
      { query: query, body: body },
      function (response) {
        if (response && response.error) reject(JSON.stringify(response || '{"message": "An unknown error occured"}'));
        else resolve(JSON.parse(response));
      }
    );
  });
}
