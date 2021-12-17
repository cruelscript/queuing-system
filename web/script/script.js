let flag = true;
let mode = true

$(document).ready(function() {

  $('#next-btn').click(function() {
    if (flag) {
      setValues();
      flag = false;
    }

    let state = nextStep();

    $('#state-buff-body-table').html('');
    $('#state-device-body-table').html('');
    $('#state-system-body-table').html('');
    $('#state-source-body-table').html('');

    state.then(function(state) {
      state['buffers'].forEach((element, index, array) => {
        $('#state-buff-body-table').append(`
            <tr>
               <td>Б${element['number_buffer']}</td>
               <td>${element['number_source']}</td>
               <td>${element['number_task']}</td>
            </tr>`);
      });

      state['devices'].forEach((element, index, array) => {
        $('#state-device-body-table').append(`
            <tr>
               <td>П${element['number_device']}</td>
               <td>${element['device_state']}</td>
               <td>${element['start_time']}</td>
               <td>${element['duration']}</td>
               <td>${element['number_task']}</td>
            </tr>`);
      });

      state['sources'].forEach((element, index, array) => {
        $('#state-source-body-table').append(`
            <tr>
               <td>И${index}</td>
               <td>${element['state']}</td>
               <td>${element['countTasks']}</td>
               <td>${element['time']}</td>
               <td>${element['step']}</td>
            </tr>`);
      });

      state['system'].forEach((element, index, array) => {
        if(index === 0)
        {
          $('#state-system-body-table').append(`
               <tr>
                  <td rowspan="${state['system'].length}" style="text-align: center;">${element['time']}</td>
                  <td>${element['action']}</td>
                  <td>${element['designated_device']}</td>
               </tr>`);
        }
        else {
          $('#state-system-body-table').append(`
               <tr>
                  <td>${element['action']}</td>
                  <td>${element['designated_device']}</td>
               </tr>`);
        }
      });
    });
  });

  $('#start-btn').click(function() {
    if (flag) {
      setValues();
      flag = false;
    }

    autoMode();

    if (mode) {
      $('#state-state-body-table').html('');
      $('#state-auto-body-table').append(`
        <tr>
          <td><img src="../images/1.png" width=500px height="250" alt="1"/></td>
          <td><img src="../images/2.png" width=500px height="250" alt="2"/></td>
          <td><img src="../images/3.png" width=500px height="250" alt="3"/></td>
        </tr>
        <tr>
          <td><img src="../images/4.png" width=500px height="250" alt="4"/></td>
          <td><img src="../images/5.png" width=500px height="250" alt="5"/></td>
          <td><img src="../images/6.png" width=500px height="250" alt="6"/></td>
        </tr>
        <tr>
          <td><img src="../images/7.png" width=500px height="250" alt="7"/></td>
          <td><img src="../images/8.png" width=500px height="250" alt="8"/></td>
          <td><img src="../images/9.png" width=500px height="250" alt="9"/></td>
        </tr>
      `)
      mode = false
    }
  })
})

async function nextStep() {
  let state = await eel.nextStep()();
  return state
}

async function autoMode() {
  await eel.autoMode()();
}

async function getBuffersState() {
  let controller = await eel.getBuffersState()();
  return controller;
}

async function getDevicesState() {
  let device = await eel.getDevicesState()();
  return device;
}

async function setValues(isAuto) {
  await eel.initController($('#SourceNumber').val(), $('#BufferNumber').val(), $('#DeviceNumber').val(), $('#Lambda').val(), $('#par-a').val(), $('#par-b').val(), $('#TaskNumber').val())()

  $('#TaskNumber').attr('readonly', 'true');
  $('#SourceNumber').attr('readonly', 'true');
  $('#BufferNumber').attr('readonly', 'true');
  $('#DeviceNumber').attr('readonly', 'true');
  $('#Lambda').attr('readonly', 'true');
  $('#par-a').attr('readonly', 'true');
  $('#par-b').attr('readonly', 'true');
}
