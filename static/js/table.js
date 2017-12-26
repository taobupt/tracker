'use strict';
var animateApp = angular.module('animateApp', ['ui.router', 'ngAnimate','ngSanitize','ngProgress']);
animateApp.config(function ($stateProvider,$urlRouterProvider) {

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
animateApp.controller('mainController', function($rootScope,$scope,$http,$state,ngProgressFactory) {

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
                method:'get',
                params:{'receipt_number':$('#receipt').val(), 'case_number':$('#case').val()}
            }).then(function (response) {
                $scope.progressbar.complete();
                console.log(response.data);
                var results = response.data;
                for(var i=0; i< results.length;++i){
                    results[i]= JSON.parse(results[i])
                }
                $rootScope.queried_cases = results;
            })
    }
});
