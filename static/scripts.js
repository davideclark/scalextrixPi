
function init (){

    // // Setup red Slider
    // var redSlider = document.getElementById('redSpeed');
    // var redOutput = document.getElementById('redSpeedLabel');
    // redOutput.innerHTML = redSlider.value; // Display the default slider value

    // // Update the current slider value (each time you drag the slider handle)
    // redSlider.oninput = function() {
    //   redOutput.innerHTML = this.value;
    //   //speed?car={red|yellow}&speed={40-100}
    //   aj('get', 'http://localhost:5000/speed?car=red&speed=' + this.value, '', null)
    // }
    
    // // Setup Yellow slider
    // var yellowSlider = document.getElementById('yellowSpeed');
    // var yellowOutput = document.getElementById('yellowSpeedLabel');
    // yellowOutput.innerHTML = yellowSpeed.value; // Display the default slider value

    // // Update the current slider value (each time you drag the slider handle)
    // yellowSpeed.oninput = function() {
    //   yellowOutput.innerHTML = this.value;
    //   aj('get', 'http://localhost:5000/speed?car=yellow&speed=' + this.value, '', null)
    // }
    
    startLed('red');
    
}

function startCarsAndSetSpeed(redSpeed, yellowSpeed) {
    aj('get', `http://localhost:5000/speed?car=yellow&speed=${yellowSpeed}`, '', null)
    aj('get', `http://localhost:5000/speed?car=red&speed=${redSpeed}`, '', null)
}

function startLed(colour) {
    aj('get', `http://localhost:5000/ledrbg?colour=${colour}`, '', null)
}

function startCar(car){
    aj('get', 'http://localhost:5000/start?car=' + car, '', null)
    }

function stopCar(car){
    aj('get', 'http://localhost:5000/stop?car=' + car, '', null)
    }

function stopCars(){
    aj('get', 'http://localhost:5000/stop?car=red', '', null)
    aj('get', 'http://localhost:5000/stop?car=yellow', '', null)
}

function aj(method, url, data, cb){

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = readystatechange;
    xhr.open(method, url);
    //xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(data && JSON.stringify(data));

    function readystatechange(){
        if(this.readyState === this.DONE) {

            switch(this.status){
                case 200:
                //if(this.getResponseHeader('Content-Type').split(';')[0] !== 'application/json'){
                //    return cb("unexpected Content-Type: '" + this.getResponseHeader('Content-Type') + "'", null);
                //}
                //return cb(null, JSON.parse(this.response));
                break;

                default:
                //alert(this.status + " status returned by api.");
                break;
            }
        }
    }//readystatechange
}


