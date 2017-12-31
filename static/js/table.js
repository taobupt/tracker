'use strict';
var animateApp = angular.module('animateApp', ['ui.router', 'ngAnimate','ngSanitize','ngProgress']);
animateApp.config(function ($stateProvider,$urlRouterProvider,$sceProvider) {

    $urlRouterProvider.otherwise('/home');
    $stateProvider
        .state('home',{
            url: '/home',
            templateUrl:'static/views/home.html',
            controller:'mainController'
        })
});


// CONTROLLERS ============================================
// home page controller
animateApp.controller('mainController', function($rootScope,$scope,$sce,$http,$state,ngProgressFactory) {

    $scope.receipt_number = 'YSC1890006200';
    $scope.cases = '1';
    $scope.images = [
        'static/images/background/1.jpg',
        'static/images/background/2.jpg',
        'static/images/background/3.jpg',
        'static/images/background/4.jpg'
    ];
    $rootScope.queried_cases=[];
    $scope.submitCard = function(){
        $(".chart").empty();
        $scope.progressbar = ngProgressFactory.createInstance();
        $scope.progressbar.start();
        $rootScope.queried_cases=[];
        $http({
            //url:'https://arcane-temple-65655.herokuapp.com/query',
            url: 'http://127.0.0.1:5000/query',
                method:'get',
                params:{'receipt_number':$('#receipt').val(), 'case_number':$('#case').val()}
            }).then(function (response) {
                $scope.progressbar.complete();
                console.log(response.data);
                var results = response.data;
                var case_data = [
                    {letter: "approved", frequency: 0, color: "#7FFF00"},
                    {letter: "received", frequency: 0,color:"#0000FF"},
                    {letter: "abnormal", frequency: 0,color:"#FF0000"},
                    {letter: "invalid", frequency: 0,color:"#808080"}
                ];
                for(var i=0; i< results.length;++i){
                    results[i]= JSON.parse(results[i])
                    if(results[i]['type']=='mailed' || results[i]['type']=='produced'){
                        results[i]['type'] = '<p style="color:green;">'+ results[i]['type']+"</p>";
                        case_data[0]["frequency"] += 1;
                    }else if(results[i]['type']=='received'){
                        case_data[1]["frequency"] += 1;
                        results[i]['type'] = '<p style="color:blue;">'+ results[i]['type']+"</p>";
                    }else{
                        if(results[i]['type']=='abnormal'){
                            case_data[2]["frequency"] += 1;
                        }else{
                            case_data[3]["frequency"] += 1;
                        }
                        results[i]['type'] = '<p style="color:red;">'+ results[i]['type']+"</p>";
                    }
                    results[i]['type']=$sce.trustAsHtml(results[i]['type']);
                }
                $rootScope.queried_cases = results;
                $rootScope.draw_histogram(case_data);
            })
    };


    $rootScope.draw_histogram = function (data) {
        var margin = {top: 20, right: 20, bottom: 30, left: 40},
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    var x = d3.scale.ordinal()
        .rangeRoundBands([0, width], .1);

    var y = d3.scale.linear()
        .range([height, 0]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")
        .ticks(10, "%");

    var svg = d3.select(".chart").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    x.domain(data.map(function(d) { return d.letter; }));
    y.domain([0, d3.max(data, function(d) { return d.frequency; })]);

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Frequency");

    var bars = svg.selectAll(".bar")
        .data(data)
        .enter();
    bars.append("rect")
        .attr("class", "bar")
        .attr("x", function(d) { return x(d.letter); })
        .attr("width", x.rangeBand())
        .attr("y", function(d) { return y(d.frequency); })
        .attr("height", function(d) { return height - y(d.frequency); })
        .style({fill: function (d) { //randomColor
            //return "#fff0f0";
            return d.color;
        }});
    bars.append("text")
        .attr("dy", ".75em")
        .attr("y", function(d){return y(d.frequency)-16;})
        .attr("x", function(d) { return x(d.letter)+x.rangeBand()/2;})
        .attr("text-anchor", "middle")
        .text(function(d) { return d.frequency; });

    function type(d) {
        d.frequency = +d.frequency;
        return d;
    }
    }
});
