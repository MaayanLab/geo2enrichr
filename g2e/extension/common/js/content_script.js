// Use this to forward requests through the background script
function post_through_background(params) {
  var query = params.query;
  var body = params.body;
  return new Promise(function (resolve, reject) {
    BROWSER.runtime.sendMessage(
      { query: query, body: body },
      function (response) {
        if (response && response.error) reject(JSON.stringify(response || '{"message": "An unknown error occured"}'));
        else {
          try {
            resolve(JSON.parse(response));
          } catch (e) {
            reject(JSON.stringify({ message: e }));
          }
        }
      }
    );
  });
}
