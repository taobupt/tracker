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
        $scope.progressbar = ngProgressFactory.createInstance();
        $scope.progressbar.start();
        $rootScope.queried_cases=[];
        $http({
            url:'https://arcane-temple-65655.herokuapp.com/query',
            //url: 'http://127.0.0.1:5000/query',
                method:'get',
                params:{'receipt_number':$('#receipt').val(), 'case_number':$('#case').val()}
            }).then(function (response) {
                $scope.progressbar.complete();
                console.log(response.data);
                var results = response.data;
                for(var i=0; i< results.length;++i){
                    results[i]= JSON.parse(results[i])
                    if(results[i]['type']=='mailed' || results[i]['type']=='produced'){
                        results[i]['type'] = '<p style="color:green;">'+ results[i]['type']+"</p>";
                    }else if(results[i]['type']=='received'){
                        results[i]['type'] = '<p style="color:blue;">'+ results[i]['type']+"</p>";
                    }else{
                        results[i]['type'] = '<p style="color:red;">'+ results[i]['type']+"</p>";
                    }
                    results[i]['type']=$sce.trustAsHtml(results[i]['type']);
                }
                $rootScope.queried_cases = results;
            })
    }
});
