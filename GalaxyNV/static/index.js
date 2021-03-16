/**
 * Creates an alert box if the path provided by the user does not exist
 */
function invalidPath() {
  error = findGetParameter('error');
  if (error == 'path_not_found') {
    const div = document.createElement('div');
    div.className = 'alert alert-danger';
    div.role = 'alert';
    div.innerText = 'Error: This is not a valid path';

    $(div).insertBefore('#load_in');
  }
}

$(document).ready(() => {
  if ($(location).attr('pathname') === '/') {
    invalidPath();
  }

  // hide input section by default
  // $('#load_in').hide();

  // // if user toggles checkbox unhide
  // $('#slider').change(() => {
  //   $('#load_in').toggle();
  // });
});

/**
 * Searches for given parameter in GET request
 * @param {string} parameterName Name of the GET request parameter
 *
 * @return {string} Contents of GET request parameter, null if it does not exist
 */
function findGetParameter(parameterName) {
  let result = null;
  let tmp = [];
  const items = location.search.substr(1).split('&');
  for (let index = 0; index < items.length; index++) {
    tmp = items[index].split('=');
    if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
  }
  return result;
}
