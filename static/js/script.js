// ==============================
// GLOBAL VARIABLES
// ==============================

let historyChart = null;
let forecastChart = null;

// ==============================
// PAGE LOAD
// ==============================

window.onload = function () {

    loadHistory();

    loadForecast();

};

// ==============================
// PREDICT STOCK
// ==============================

async function predictStock() {

    const predictionBox =
        document.getElementById("prediction");

    predictionBox.innerHTML = "Loading...";

    try {

        const response = await fetch("/predict");


        if(!response.ok){

            throw new Error(
                "Server returned " + response.status
            );

        }


        const data = await response.json();


        console.log(data);


        const predicted =
            parseFloat(data.prediction);


        const current =
            parseFloat(data.current_price);



        document.getElementById("currentPrice").innerHTML =
            "$" + current.toFixed(2);



        document.getElementById("confidence").innerHTML =
            data.confidence + "%";



        document.getElementById("summarySignal").innerHTML =
            data.signal;



        const reasonList =
            document.getElementById("reasonList");


        reasonList.innerHTML="";


        data.why.forEach(function(reason){

            let li=document.createElement("li");

            li.innerHTML=reason;

            reasonList.appendChild(li);

        });



        predictionBox.innerHTML =
            "$" + predicted.toFixed(2);



        document.getElementById("summaryPrice").innerHTML =
            "$" + predicted.toFixed(2);



        let diff =
            predicted-current;


        let percent =
            (diff/current)*100;


        let text =
            (diff>=0?"+":"")+
            percent.toFixed(2)+"%";



        document.getElementById("change").innerHTML =
            text;


        document.getElementById("summaryChange").innerHTML =
            text;


        document.getElementById("recommendation").innerHTML =
            data.signal;



        drawForecast(
            current,
            predicted
        );


    }


    catch(error){

        console.error(error);

        predictionBox.innerHTML =
            "Prediction Failed";

    }

}

// ==============================
// BUY / HOLD / SELL
// ==============================

function recommendation(percent){

    let signal = "";

    if(percent > 2){

        signal = "BUY";

    }

    else if(percent < -2){

        signal = "DON'T BUY";

    }

    else{

        signal = "HOLD";

    }

    document.getElementById("recommendation").innerHTML =
        signal;

    document.getElementById("summarySignal").innerHTML =
        signal;

}

// ==============================
// HISTORY CHART
// ==============================

async function loadHistory(){

    const response = await fetch("/history");

    const data = await response.json();

    const latest =
        data.close[data.close.length-1];

    document.getElementById("currentPrice").innerHTML =
        "$" + latest;

    if(historyChart){

        historyChart.destroy();

    }

    const ctx =
        document.getElementById("historyChart");

    historyChart = new Chart(ctx,{

        type:"line",

        data:{

            labels:data.dates,

            datasets:[{

                label:"Netflix Close Price",

                data:data.close,

                borderColor:"#E50914",

                borderWidth:3,

                tension:.3,

                fill:true,

                backgroundColor:"rgba(229,9,20,.1)"

            }]

        },

        options:{

            responsive:true,

            plugins:{

                legend:{

                    display:false

                }

            }

        }

    });

}

// ==============================
// RANDOM CONFIDENCE
// Replace later with backend value
// ==============================



// ==============================
// ANIMATED COUNTER
// ==============================

function animateValue(id,end){

    let obj =
        document.getElementById(id);

    let start = 0;

    let duration = 1200;

    let increment = end/100;

    let timer = setInterval(function(){

        start += increment;

        obj.innerHTML =
            "$"+start.toFixed(2);

        if(start>=end){

            obj.innerHTML =
                "$"+end.toFixed(2);

            clearInterval(timer);

        }

    },duration/100);

}

// ==============================
// WHY PREDICTION
// ==============================

function updateReason(percent){

    let list="";

    if(percent>2){

        list=`

<li>Positive recent momentum</li>

<li>Moving Average trending upward</li>

<li>Strong historical trend</li>

<li>Low volatility</li>

`;

    }

    else if(percent<-2){

        list=`

<li>Weak recent momentum</li>

<li>Price below Moving Average</li>

<li>Higher volatility</li>

<li>Downward trend detected</li>

`;

    }

    else{

        list=`

<li>Market moving sideways</li>

<li>No strong trend</li>

<li>Stable volatility</li>

<li>Mixed historical signals</li>

`;

    }

    document.getElementById("reasonList").innerHTML =
        list;

}

// ==============================
// FORECAST CHART
// ==============================

function drawForecast(current,prediction){

    let ctx =
        document.getElementById("forecastChart");

    if(!ctx)
        return;

    if(forecastChart){

        forecastChart.destroy();

    }

    forecastChart =
        new Chart(ctx,{

        type:"line",

        data:{

            labels:[
                "Today",
                "Tomorrow"
            ],

            datasets:[{

                label:"Prediction",

                data:[
                    current,
                    prediction
                ],

                borderColor:"#198754",

                borderWidth:3,

                tension:.3

            }]

        }

    });

}

// ==============================
// 7 DAY FORECAST
// ==============================

async function loadForecast(){

    try{

        const response = await fetch("/forecast");

        const data = await response.json();


        const forecast = data.forecast;


        const labels = forecast.map(
            item => "Day " + item.day
        );


        const prices = forecast.map(
            item => item.price
        );


        let ctx =
            document.getElementById("forecastChart");


        if(!ctx)
            return;


        if(forecastChart){

            forecastChart.destroy();

        }


        forecastChart = new Chart(ctx,{

            type:"line",

            data:{

                labels:labels,

                datasets:[{

                    label:"7 Day Netflix Forecast",

                    data:prices,

                    borderWidth:3,

                    tension:0.3,

                    fill:true

                }]

            },


            options:{

                responsive:true,

                plugins:{

                    legend:{

                        display:true

                    }

                }

            }

        });


    }


    catch(error){

        console.log(
            "Forecast error:",
            error
        );

    }

}

// ==============================
// DOWNLOAD CSV
// ==============================

async function downloadCSV(){

    window.location="/download";

}

// ==============================
// LOADING
// ==============================

function showLoader(){

    document.querySelector(".loader").style.display="block";

}

function hideLoader(){

    document.querySelector(".loader").style.display="none";

}