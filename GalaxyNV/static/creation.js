/* eslint-disable no-unused-vars */
/* Uses Google TypeScript Style */

// Globals
let tabIndex = 0; // Current tab is set to be the first tab (0)
let nodeCounter = 0;
let baseCounter = 0;
let networkCounter = 0;

const commonPrebuilds = {
  'apt-get -q update': 'update',
  'apt-get -yq upgrade': 'upgrade',
  'apt-get install -yq curl': 'curl',
  'apt-get install -yq nmap': 'nmap',
  'apt-get install -yq ncat': 'ncat',
  'apt-get install -yq git': 'git',
};

const commonPostbuilds = {
  'pip install scapy': 'scapy',
};

// on document load
$(() => {
  showTab(tabIndex); // Display the current tab
  addCounter(networkCounter); // Display current range value
  $('.popoverData').popover(); // enable popover data on load

  // ensures there is always one row
  createEmptyRows('base');
  createEmptyRows('node');
  createEmptyRows('network');

  // Shows filename in upload input field
  $('.custom-file-input').on('change', function () {
    const fileName = $(this).val().split('\\').pop();
    $(this).siblings('.custom-file-label').addClass('selected').html(fileName);
  });

  // Show popup depending on result from python app
  const resultText = $('#result').text();
  if (resultText !== '') {
    const div = document.createElement('div');
    div.role = 'alert';
    div.id = 'result_alert';

    if (resultText === 'success') {
      div.className = 'alert alert-success';
      div.innerText = 'Configuration submitted successfully!';
    } else if (resultText === 'error') {
      div.className = 'alert alert-error';
      div.innerText = 'Error: Configuration not submitted successfully!';
    }

    $(div).insertBefore('#base_tab');
    $('#result_alert').delay(5000).fadeOut('slow');
  }
});

// on refresh load run this
$(window).bind('load', () => {
  // ensure counters are correct
  $('#baseCounter')[0].value = baseCounter;
  $('#nodeCounter')[0].value = nodeCounter;
  $('#networkCounter')[0].value = networkCounter;
});

// ############################################################ //
// ############################################################ //
// ####### Handles Loading Existing Config into WebApp ######## //
// ############################################################ //
// ############################################################ //

/**
 * Load existing configuration onto page.
 * Searches configuration/infrastructure/images/{base|node}
 *
 * @param {object} base All the base images to create
 * @param {object} node All the node images to create
 * @param {object} network All the network nodes to create
 */
function load(base, node, network) {
  // modify existing counters with loaded configs counters
  $('#baseCounter').val(base.length);
  $('#nodeCounter').val(node.length);
  $('#networkCounter').val(network.length);

  // create rows based on new counters
  updateRows('base');
  updateRows('node');
  updateRows('network');

  // load values in per tab
  loadTab('base', base);
  loadTab('node', node);
  loadTab('network', network);
}

/**
 * Load in the elements on the page with their correlating information.
 * Based on the type there are differing fields.
 *
 * @param {string} tab Relates to which tab the elements passed belong to.
 * @param {object} elements Contains the information to place on the current tab
 *
 */
function loadTab(tab, elements) {
  if (tab === 'network') {
    _loadNetworkTab(elements);
  } else {
    _loadBaseNodeTab(tab, elements);
  }
}

/**
 * Loads specifically the base and node tabs.
 * @param {string} tab Relates to which tab the elements passed belong to.
 * @param {object} elements Contains the information to place on the current tab
 */
function _loadBaseNodeTab(tab, elements) {
  for (let index = 0; index < elements.length; index++) {
    const currentElement = elements[index];

    // set text fields
    $('#' + tab + '_path' + index).val(currentElement.path);
    $('#' + tab + '_server' + index).val(currentElement.server);
    $('#' + tab + '_parent' + index).val(currentElement.parent);

    // if the current row has a prebuild set the row value
    setBuildFields(currentElement.prebuild, index, tab, 'pre');
    // if the current row has a postbuild set the row value
    setBuildFields(currentElement.postbuild, index, tab, 'post');

    // set overlay field
    const overlay = $('#' + tab + '_overlay' + index);
    const overlayContent = currentElement.overlay;
    if (overlayContent !== '') {
      overlay.val(overlayContent);
      // text area # of rows
      overlay.attr('rows', overlayContent.split('\n').length + 1);
    } else {
      overlay.attr('rows', 1);
    }
  }
}

/**
 * Loads specifically the network tab.
 * @param {object} elements Contains the information to place on the network tab
 */
function _loadNetworkTab(elements) {
  for (let index = 0; index < elements.length; index++) {
    $('#network_name' + index).val(elements[index].image);
    $('#network_links' + index).val(elements[index].links);
    $('#network_agents' + index).val(elements[index].agents);
    $('#network_agents' + index).attr(
      'rows',
      1 + elements[index].agents.split('\n').length,
    );
    $('#network_links' + index).attr(
      'rows',
      1 + elements[index].links.split('\n').length,
    );
    $('#network_range' + index).val(elements[index].priority);
    $('#range_value' + index).val(elements[index].priority);
    $('#network_replicas' + index).val(elements[index].replicas);
    $('#network_hostname' + index).val(elements[index].hostname);
  }
}

/**
 * Fills in the build checkboxes and the build text area. If applicable.
 *
 * @param {string} build String of build commands that are newline delimited
 * @param {number} index Current row index
 * @param {string} tab [base | node] Specific tab that these commands belong to
 * @param {string} buildType [post | pre] Specific type of build command
 */
function setBuildFields(build, index, tab, buildType) {
  if (build) {
    // set common checkboxes if any
    let commonBuilds;
    switch (buildType) {
      case 'pre':
        commonBuilds = commonPrebuilds;
        break;
      case 'post':
        commonBuilds = commonPostbuilds;
        break;
      default:
        const errorMessgae = {
          code: 554,
          message: "Only 'pre' or 'post' are acceptable build types.",
        };
        throw errorMessgae;
    }

    build = setCommonCheckboxes(build, index, commonBuilds);

    // now set text area
    const className = '#' + tab + '_' + buildType + 'build' + index;
    $(className).val(build); // text area content
    $(className).attr('rows', build.split('\n').length); // text area # of rows
  }
}

/**
 * Selects checkboxes on current row if they are contained within the buildInfo
 * string passed. If they are then they are removed from the string so that the
 * returning string only contains build commands that are NOT found in the
 * checkboxes.
 *
 * @param {string} buildInfo String of build commands that are newline delimited
 * @param {number} index Current row index
 * @param {object} commonBuild Object of common build selections correlates to
 * checkboxes on page.
 * @return {string} String containing build commands that were not apart of the
 * common listing.
 */
function setCommonCheckboxes(buildInfo, index, commonBuild) {
  for (const key in commonBuild) {
    if (buildInfo.includes(key)) {
      $('#' + commonBuild[key] + index).prop('checked', true);

      buildInfo = buildInfo.replace(key, '');
    }
  }
  return buildInfo.trim();
}

/**
 * Creates/Destroys rows for the specific tab depending on how the counter
 * on the page compares to the JS stored counter.
 *
 * @param {string}  tab [base | node | network] Specific tab that these
 * commands belong to
 */
function updateRows(tab) {
  let desiredCount = $('#' + tab + 'Counter').val();
  if (desiredCount) {
    desiredCount = parseInt(desiredCount);

    // determine which tab and set variables accordingly
    switch (tab) {
      case 'base':
        currentCount = baseCounter;
        add = addBase;
        break;
      case 'node':
        currentCount = nodeCounter;
        add = addNode;
        break;
      case 'network':
        currentCount = networkCounter;
        add = addNetwork;
        break;
      default:
        const errorMessgae = {
          code: 555,
          message: "Only 'network' 'base' or 'node' are acceptable tab values",
        };
        throw errorMessgae;
    }

    // either create or destroy rows depending on
    // desiredCount's relationship to currentCount
    while (desiredCount != currentCount) {
      if (desiredCount < currentCount) {
        $('#base' + currentCount).remove();
        currentCount--;
      } else if (desiredCount > currentCount) {
        currentCount = add();
      }
    }
  }
}

// ############################################################ //
// ############################################################ //
// ########### Handles Dynamically Adding Elements ############ //
// ############################################################ //
// ############################################################ //

/**
 * Creates an initial empty row for the specific tab
 * @param {string} tab String referring to which tab to create the rows on
 */
function createEmptyRows(tab) {
  if ($('#' + tab + 'Counter').val() === '0') {
    $('#' + tab + 'Counter').val(1);
    updateRows(tab);
  }
}

/**
 * Adds a number slider to passed parent element
 *
 * @param {string} labelText Label of the input field
 * @param {number} index Which row is currently being added.
 * @param {object } parent The parent element that the slider
 * is added to.
 * @param {string} popupText Text to appear when hovering over the field
 */
function addSlider(labelText, index, parent, popupText) {
  const div = createHoverLabel(labelText, popupText);
  div.children[0].className += ' control-label';
  const divFlex = document.createElement('div');
  divFlex.className = 'd-flex justify-content-center my-4';

  // setup range element which can be interacted with by the user
  const input = document.createElement('input');
  input.className = 'custom-range';
  input.type = 'range';
  input.min = '0';
  input.max = '100';
  input.step = '1';
  input.value = '0';
  input.id = 'network_range' + index;
  input.name = 'network_range' + index;

  divFlex.appendChild(input);

  // setup span which will be populated with the value of the range
  const span = document.createElement('span');
  span.className = 'font-weight-bold text-primary ml-2';
  span.id = 'range_value' + index;

  divFlex.appendChild(span);

  div.appendChild(divFlex);
  parent.appendChild(div);
}

/**
 * Adds checkboxes to passed parent element.
 *
 * @param {string} labelText The label for the overarching field.
 * @param {string} name The name of the checkbox used for data sent via Post.
 * @param {number} index Which row is currently being added.
 * @param {object} parent The parent element that the checkboxes
 * are added to.
 * @param {string} popupText Text to appear when hovering over the field.
 * @param {string[]} checkboxTexts Array of checkbox values.
 */
function addCheckbox(labelText, name, index, parent, popupText, checkboxTexts) {
  const div = createHoverLabel(labelText, popupText);
  let row;
  for (const [count, checkboxText] of checkboxTexts.entries()) {
    // groups checkboxes in pairs of 3
    if (count === 0 || count % 3 === 0) {
      row = document.createElement('div');
      row.className = 'row';
      div.appendChild(row);
    }

    const trimmedText = checkboxText.trim();
    const divCheck = document.createElement('div');
    divCheck.className = 'col-sm text-nowrap custom-control custom-checkbox';

    // creates checkbox
    const input = document.createElement('input');
    input.type = 'checkbox';
    input.className = 'custom-control-input';
    input.id = trimmedText.split(' ').slice(-1)[0] + index;
    input.name = name + index;
    input.value = trimmedText;

    // creates label for checkbox
    const label = document.createElement('label');
    label.className = 'custom-control-label';
    label.htmlFor = input.id;
    label.innerText = trimmedText;

    divCheck.append(input);
    divCheck.append(label);

    row.append(divCheck);
  }
  parent.appendChild(div);
}

/**
 * Adds radio to parent element.
 * @param {string} labelText The label for the overarching radio.
 * @param {number} index Which row is currently being added.
 * @param {object } parent The parent element that the radios
 * @param {string[]} radioTexts Array of radio values.
 * are added to.
 *
 * NOTE: not currently used
 */
function addRadio(labelText, index, parent, radioTexts) {
  const div = createHoverLabel(labelText);

  for (const radioText of radioTexts) {
    const divCheck = document.createElement('div');
    divCheck.className = 'form-check';

    const input = document.createElement('input');
    input.className = 'form-check-input';
    input.type = 'radio';
    input.name = 'type' + index;
    input.value = radioText;
    if (radioText === 'LXD') {
      input.checked = true;
    }

    const label = document.createElement('label');
    label.className = 'form-check-label';
    label.for = input.name;

    label.innerText = radioText;

    divCheck.append(input);
    divCheck.append(label);
    div.appendChild(divCheck);
  }

  parent.appendChild(div);
}

/**
 *
 * @param {*} labelText
 * @param {*} inputName
 * @param {*} index
 * @param {*} parent
 * @param {*} popupText
 */
function addFileUpload(labelText, inputName, index, parent, popupText) {
  const input = document.createElement('input');
  const div = createHoverLabel(labelText, popupText);

  const fileDiv = document.createElement('div');
  fileDiv.className = 'custom-file';
  const label = document.createElement('label');

  input.type = 'file';
  input.className = 'custom-file-input';

  // sets name and id of field
  input.name = inputName + index;
  input.id = inputName + index;

  label.className = 'custom-file-label';
  label.setAttribute('for', inputName + index);
  label.innerText = 'Choose file';

  fileDiv.appendChild(input);
  fileDiv.appendChild(label);

  div.appendChild(fileDiv);
  parent.appendChild(div);
}
/**
 * Adds two numbers together.
 * @param {string} labelText The label for the overarching field.
 * @param {number} inputName The name of the field used for data sent via Post.
 * @param {number} index Which row is currently being added.
 * @param {object } parent The parent element that the field is added to
 * @param {string} popupText popupText Text to appear when hovering over
 * the field.
 * @param {boolean} required If this field is required for verification.
 * @param {string} inputType The element type {text/textarea}.
 * @param {boolean} readOnly Makes the field readonly.
 */
function addField(
  labelText,
  inputName,
  index,
  parent,
  popupText,
  required = false,
  inputType = 'text',
  readOnly = false,
) {
  let input;
  const div = createHoverLabel(labelText, popupText);

  // creates field
  if (inputType === 'text') {
    input = document.createElement('input');
    input.type = inputType;
    input.className = 'form-control';
  } else if (inputType === 'textarea') {
    input = document.createElement('textarea');
    input.className = 'form-control';
    input.rows = '1';
  }

  // sets name and id of field
  input.name = inputName + index;
  input.id = inputName + index;

  // sets verification info
  if (required) {
    input.required = true;
    div.children[0].className += ' control-label';
  }

  input.readOnly = readOnly;
  div.appendChild(input);

  parent.appendChild(div);
}

/**
 * Adds ability for range bar to automatically populate
 * a counter field.
 * @param {number} rowTotal The total number of rows to check.
 */
function addCounter(rowTotal) {
  for (let counter = 0; counter <= rowTotal; counter++) {
    const valueSpan = $('#range_value' + counter);
    const value = $('#network_range' + counter);
    valueSpan.html(value.val());
    value.on('input change', () => {
      valueSpan.html(value.val());
    });
  }
}

/**
 * Generates a delete button and appends it to passed element.
 * @param {object} parent The element to add the delete button to.
 */
function addDeleteButton(parent) {
  const div = createHoverLabel('');

  const input = document.createElement('input');
  input.type = 'button';
  input.className = 'ibtnDel btn btn-md btn-danger ';
  input.value = 'Delete';

  div.appendChild(input);

  parent.appendChild(div);
}

/**
 * Creates a div containing a label that has popup text when hovered on
 *
 * @param {string} labelText The value of the label.
 * @param {string} popupContent Text to appear when hovering over
 * the field.
 * @param {string} className Value of class for div
 * @return {object } The div element that the input element will be
 * appended to.
 */
function createHoverLabel(labelText, popupContent, className = 'form-group') {
  const div = document.createElement('div');
  div.className = className;

  const label = document.createElement('label');
  label.innerText = labelText;
  label.className = 'popoverData';
  label.dataset.content = popupContent;
  label.dataset.html = 'true';
  label.dataset.placement = 'left';
  label.dataset.originalTitle = labelText;
  label.dataset.trigger = 'hover';
  div.appendChild(label);
  return div;
}

// ############################################################ //
// ############################################################ //
// ################# Handles Multiple Tabs #################### //
// ############################################################ //
// ############################################################ //

/**
 * Displays the specified tab of the form
 * @param {number} index The tab index to show.
 */
function showTab(index) {
  const currentTab = document.getElementsByClassName('tab');
  currentTab[index].style.display = 'block';
  // Updates the Previous/Next buttons depending on form progress
  if (index === 0) {
    document.getElementById('prevBtn').style.display = 'none';
  } else {
    document.getElementById('prevBtn').style.display = 'inline';
  }
  if (index === currentTab.length - 1) {
    document.getElementById('nextBtn').innerHTML = 'Submit';
  } else {
    document.getElementById('nextBtn').innerHTML = 'Next';
  }
  updateStepIndicator(index);
}

/**
 * Figures out which tab to display
 * @param {number} n Where to move from current tab
 * @return {boolean} True if at max tab, False if not
 */
function nextPrev(n) {
  const currentTab = document.getElementsByClassName('tab');
  // Exit the function if any field in the current tab is invalid:
  if (n === 1 && !validateForm()) return false;
  // Hide the current tab:
  currentTab[tabIndex].style.display = 'none';
  // Increase or decrease the current tab by 1:
  tabIndex = tabIndex + n;
  if (tabIndex >= currentTab.length) {
    // if you have reached the end of the form the form gets submitted:
    document.getElementById('regForm').submit();
    return false;
  }
  // Otherwise, display the correct tab:
  showTab(tabIndex);
}

/**
 * Ensures required fields are filled out and if so mark tab as finished.
 * @return {boolean} Flag that marks if current tab is finished.
 */
function validateForm() {
  const currentTab = document.getElementsByClassName('tab');
  const elementsOfTab = currentTab[tabIndex].getElementsByTagName('*');
  let valid = true;

  // A loop that checks every input field in the current tab:
  for (let i = 0; i < elementsOfTab.length; i++) {
    // If a field is empty...
    if (elementsOfTab[i].required && elementsOfTab[i].value === '') {
      // add an 'invalid' class to the field:
      elementsOfTab[i].className += ' invalid';
      // and set the current valid status to false
      valid = false;
    }
  }
  // If the valid status is true, mark the step as finished and valid:
  if (valid) {
    document.getElementsByClassName('step')[tabIndex].className += ' finish';
  }
  return valid; // return the valid status
}

/**
 * Updated tab so step indicator can mark it correctly
 * @param {number} n The first number.
 */
function updateStepIndicator(n) {
  const stepElements = document.getElementsByClassName('step');
  for (let i = 0; i < stepElements.length; i++) {
    stepElements[i].className = stepElements[i].className.replace(
      ' active',
      '',
    );
  }
  stepElements[n].className += ' active';
}

// ############################################################ //
// ############################################################ //
// ###################### Adds New Rows ####################### //
// ############################################################ //
// ############################################################ //

/**
 * Adds a new base image row. Generates all the elements needed for a user
 * to put a new base image on the page
 * @return {number} returns modified baseCounter
 */
function addBase() {
  const div = document.createElement('div');
  div.id = 'base' + baseCounter;

  // Add all fields needed for the row
  addField(
    'Path',
    'base_path',
    baseCounter,
    div,
    `This is relative to infrastructure/images/build <br /><br />For example if
     you want to create an agent base image stored in infrastructure/images/
     base/agent you would just enter <b>agent</b> in Path`,
    true,
  );
  addField(
    'Parent Server',
    'base_server',
    baseCounter,
    div,
    'URL to location to image. Usually only used for master image. <br/><br/>Example: https://images.linuxcontainers.org',
  );
  addField(
    'Parent',
    'base_parent',
    baseCounter,
    div,
    `Path to image to inherit information from. Like Path it is relative to
    infrastructure/image/base`,
    true,
  );
  addCheckbox(
    'Prebuild',
    'base_pre',
    baseCounter,
    div,
    'Common options that are usually selected for prebuild options',
    [
      'apt-get -q update',
      'apt-get -yq upgrade',
      'apt-get install -yq curl',
      'apt-get install -yq nmap',
      'apt-get install -yq ncat',
      'apt-get install -yq git',
    ],
  );
  addField(
    'Prebuild',
    'base_prebuild',
    baseCounter,
    div,
    `Field used to provide optional prebuild options. Field is treated as
    newline delimited.`,
    false,
    'textarea',
  );
  addCheckbox(
    'Postbuild',
    'base_post',
    baseCounter,
    div,
    'Common options that are usually selected for postbuild options',
    ['pip install scapy'],
  );
  addField(
    'Postbuild',
    'base_postbuild',
    baseCounter,
    div,
    `Field used to provide optional postbuild options. Field is treated as
    newline delimited.`,
    false,
    'textarea',
  );
  addField(
    'Overlay',
    'base_overlay',
    baseCounter,
    div,
    'Read-only field to show which files are located in overlay directory.',
    false,
    'textarea',
    true,
  );

  // Add delete button that can remove the current row if desired
  addDeleteButton(div);
  $(div).on('click', '.ibtnDel', function () {
    $(this).parent().parent().remove();
    baseCounter -= 1;
    $('#baseCounter').val(baseCounter);
  });

  div.appendChild(document.createElement('hr'));
  $(div).insertBefore('#addBase');

  // increment row counter for base
  baseCounter++;
  $('#baseCounter').val(baseCounter);

  // allows new fields to have popup animation
  $('.popoverData').popover();

  return baseCounter;
}

/**
 * Adds a new node image row. Generates all the elements needed for a user
 * to put a new node image on the page
 * @return {number} returns modified nodeCounter
 */
function addNode() {
  const div = document.createElement('div');
  div.id = 'node' + nodeCounter;

  // Add all fields needed for the row
  addField(
    'Path',
    'node_path',
    nodeCounter,
    div,
    `This is relative to infrastructure/images/node <br /><br />For example if
    you want to create an agent base image stored in infrastructure/images/base/
    agent you would just enter <b>agent</b> in Path`,
    true,
  );
  addField(
    'Parent Server',
    'node_server',
    nodeCounter,
    div,
    'URL to location to image. Usually only used for master image. <br/><br/>Example: https://images.linuxcontainers.org',
  );
  addField(
    'Parent',
    'node_parent',
    nodeCounter,
    div,
    `Path to image to inherit information from. Like Path it is relative to
    infrastructure/image/node`,
    true,
  );
  addField(
    'Prebuild',
    'node_prebuild',
    nodeCounter,
    div,
    `Field used to provide optional prebuild options. Field is treated as
    newline delimited.`,
    false,
    'textarea',
  );
  addField(
    'Postbuild',
    'node_postbuild',
    nodeCounter,
    div,
    `Field used to provide optional postbuild options. Field is treated as
    newline delimited.`,
    false,
    'textarea',
  );
  addField(
    'Overlay',
    'node_overlay',
    nodeCounter,
    div,
    'TODO',
    false,
    'textarea',
    true,
  );

  // Add delete button that can remove the current row if desired
  addDeleteButton(div);
  $(div).on('click', '.ibtnDel', function () {
    $(this).parent().parent().remove();
    nodeCounter -= 1;
    $('#nodeCounter').val(nodeCounter);
  });

  div.appendChild(document.createElement('hr'));
  $(div).insertBefore('#addNode');

  // increment row counter for node
  nodeCounter++;
  $('#nodeCounter').val(nodeCounter);

  // allows new fields to have popup animation
  $('.popoverData').popover();

  return nodeCounter;
}

/**
 * Adds a new network instance row. Generates all the elements needed for a user
 * to put a new network instance on the page
 * @return {number} returns modified networkCounter
 */
function addNetwork() {
  const div = document.createElement('div');
  div.id = 'network' + networkCounter;

  // Add all fields needed for the row
  addField(
    'Name',
    'network_name',
    networkCounter,
    div,
    "Field used to define a new node's network information.",
    true,
  );
  addSlider(
    'Priority',
    networkCounter,
    div,
    'Field used to define nodes priority. Lower is a higher priority.',
  );
  addField(
    'Links',
    'network_links',
    networkCounter,
    div,
    'Field used to define which networks this node can communicate with.',
    true,
    'textarea',
  );
  addField(
    'Agents',
    'network_agents',
    networkCounter,
    div,
    'Field used to define which agents should be loaded on this node.',
    true,
    'textarea',
  );
  addField('Replicas', 'network_replicas', networkCounter, div, 'TODO', false);
  addField('Hostname', 'network_hostname', networkCounter, div, 'TODO', false);

  // Add delete button that can remove the current row if desired
  addDeleteButton(div);
  $(div).on('click', '.ibtnDel', function () {
    $(this).parent().parent().remove();
    networkCounter -= 1;
    $('#networkCounter').val(networkCounter);
  });

  div.appendChild(document.createElement('hr'));
  $(div).insertBefore('#addNetwork');

  addCounter(networkCounter);

  // increment row counter for network
  networkCounter++;
  $('#networkCounter').val(networkCounter);

  // Enable popup animation
  $('.popoverData').popover();

  return networkCounter;
}
