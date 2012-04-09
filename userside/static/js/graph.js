$(function () {
    var chart;
    $(document).ready(function() {
        chart = new Highcharts.Chart({
            chart: {
                renderTo: 'graph_container',
                type: 'column',
								backgroundColor:'rgba(255, 255, 255, 0.1)'
            },
            title: {
                text: 'Average Wait Time'
            },
            xAxis: {
                categories: [
                    '9am',
                    '10am',
                    '11am',
                    '12pm',
                    '1pm',
                    '2pm',
                    '3pm',
                    '4pm',
                    '5pm',
                ]
            },
						legend: {
							enabled: false
						},
            yAxis: {
                min: 0,
                title: {
                    text: 'Minutes'
                }
            },
            tooltip: {
                formatter: function() {
                    return ''+
                        this.x +': '+ this.y +' min';
                }
            },
            plotOptions: {
                column: {
                    pointPadding: 0.2,
                    borderWidth: 0
                }
            },
                series: [{
                name: 'Company',
                data: [135, 148, 216, 49, 71, 144, 176, 106, 129]

            }]
        });
    });
    
});