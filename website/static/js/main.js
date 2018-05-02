/**
 * Created by Administrator on 2018/4/26.
 */

function show_cahrts(data) {
    // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('weight-chart'));
        var weights = data.weights;
        var cls = Object.keys(weights);
        var values = [];
        $.each(cls, function (item) {
            values.push(weights[item]);
        });
        // 指定图表的配置项和数据
        var option = {
            title: {
                text: 'weights to groups'
            },
            tooltip: {},
            legend: {
                data:['weights']
            },
            xAxis: {
                data: cls
            },
            yAxis: {},
            series: [{
                name: 'weights',
                type: 'bar',
                data: values
            }]
        };
        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
}

function tag_classify() {
    var tag = $('.search-input').val();
    $.getJSON('/api/tag/' + tag + '/classify', function (data) {
        show_cahrts(data);
    });
}