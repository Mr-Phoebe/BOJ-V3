'use strict';

/* App */
angular.module('boardApp', ['boardControllers', 'boardServices']);

/* Controllers */
var boardControllers = angular.module('boardControllers', []);

boardControllers.controller('DynamicScoreCtrl', ['$scope', 'Constants', 'Board',
  function($scope, Constants, Board) {
    var tmp = Board.get({
      cid: Constants.get('cid')
    }, function(board) {
      $scope.problems = board.board.problem_infos;
      $scope.users = board.board.user_infos;
    });
  }
]);

/* Services */

var boardServices = angular.module('boardServices', ['ngResource']);

boardServices.factory('Constants', function(DjangoConstants) {
  var constants = {};
  angular.extend(constants, DjangoConstants);
  return {
    get: function(key) {
      return constants[key];
    },
    all: function() {
      return constants;
    }
  };
});

boardServices.factory('Board', ['$resource',
  function($resource) {
    return $resource('/api/contest/:cid/board');
  }
]);
